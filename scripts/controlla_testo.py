#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Segnala riga per riga i punti sospetti di un testo italiano.

Fa parte della skill italiano-scrittura-anti-ai. Cerca nel testo le stringhe
e le strutture che le regole della skill vietano o chiedono di giustificare,
e per ciascuna stampa riga, colonna, regola e un estratto. Non corregge
niente: ogni segnalazione va guardata da chi rivede, perché alcune (la
virgola prima di «e», il gerundio in coda) sono legittime in certi casi.
Scritto da Renato Romano nel suo fork, rivisto per la versione 1.7.0.

    python controlla_testo.py FILE [FILE ...]
    python controlla_testo.py -          (legge il testo da stdin)
    python controlla_testo.py --prova    (lancia le autoprove)

Codici di uscita: 0 nessuna violazione certa; 1 almeno una violazione certa;
2 uso sbagliato o file che non si può leggere come UTF-8.
Non usa librerie esterne, non accede alla rete e non scrive nessun file.
"""

import contextlib
import io
import re
import sys

# L'apostrofo è sia quello dritto sia quello tipografico (’) dei file esportati da Word.
LETTERA = r"A-Za-zÀ-ÿ'’"
# Ogni controllo: (nome, livello, regola, espressione, nota).
# «certo» indica una violazione da correggere sempre; «verifica» un punto
# che può essere legittimo e va giustificato da chi rivede.
CONTROLLI = [
    ("em-dash", "certo", "regola 1", r"—", "sostituire con virgole, parentesi o due punti"),
    ("virgolette inglesi", "certo", "regola 3", r"[\"“”]", "usare le caporali « »"),
    ("incipit formulaico", "certo", "regola 4",
     r"(?i)\b(?:nel mondo di oggi|nel panorama attuale|nell['’]era digitale|ti sei mai chiesto|"
     r"hai mai pensato|immagina un mondo|scopri il potere)", "aprire con un fatto o una tesi"),
    ("chiusura formulaica", "certo", "regola 5",
     r"(?i)\b(?:in conclusione|in definitiva|per tirare le somme|spero che questo articolo)",
     "chiudere con una conseguenza o un'immagine"),
    ("meta-annuncio", "certo", "regola 6",
     r"(?i)\b(?:è importante sottolineare|vale la pena notare|non si può non menzionare|degno di nota)",
     "dire la cosa invece di annunciarla"),
    # La regola 7 vieta il tic ricorrente, non la parola: una sola occorrenza va guardata.
    ("lessico AI", "verifica", "regola 7",
     r"(?i)\b(?:delinea\w*|approfondi\w*|navigare il panorama|esplorare insieme)",
     "lecito una volta; come tic ricorrente va sostituito da una parola semplice"),
    ("non solo… ma anche", "certo", "regola 8", r"(?i)\bnon solo\b[^.]{0,80}\bma\b", "congiunzione semplice"),
    ("errore ortografico", "certo", "regola 9",
     r"(?i)\b(?:un['’]altro|qual['’]è|un pò|perchè|nè)(?![{L}])".format(L=LETTERA),
     "forma corretta: un altro, qual è, un po', perché, né"),
    ("piuttosto che", "verifica", "regola 10", r"(?i)\bpiuttosto che\b",
     "ammesso solo in senso comparativo, mai per «oppure»"),
    # Nel testo finale va tolto; in un dialogo o in una lettera vera può restare.
    ("artefatto da chatbot", "verifica", "regola 11",
     r"(?i)(?:\bcerto!|ottima domanda|ecco un articolo|spero che ti sia utile|fammi sapere se)",
     "eliminare se è la voce del modello; lecito in un dialogo o in una lettera"),
    ("knowledge cutoff", "certo", "regola 12",
     r"(?i)\b(?:sulla base delle informazioni disponibili|fino al mio ultimo aggiornamento)",
     "verificare o attribuire la fonte"),
    ("contrasto fittizio", "certo", "regola 16",
     r"(?i)\bnon (?:è|si tratta di)\b[^.;]{1,60}[,:;] (?:è|ma di)\b", "affermare direttamente il positivo"),
    ("contrasto fittizio su due frasi", "verifica", "regola 16",
     r"(?i)\bnon (?:è|si tratta di)\b[^.;:!?]{1,60}\.\s+(?:è|si tratta di)\b",
     "se la negazione non corregge un equivoco reale, affermare direttamente il positivo"),
    ("virgola di Oxford", "certo", "grammatica §8",
     r"(?<![{L}])[{L}]+, [{L}]+, e (?=[{L}«\"“*_])".format(L=LETTERA), "in un elenco mai la virgola prima di «e»"),
    ("virgola prima di e", "verifica", "regola 17", r",\s+e(?![{L}])".format(L=LETTERA),
     "con lo stesso soggetto si toglie; resta per cambio di soggetto, «e» avversativa, inciso o stacco voluto"),
    ("titoletto in grassetto", "certo", "regola 20", r"^\s*(?:[-*]\s+|\d+\.\s+)?\*\*[^*\n]{1,60}\*\*\s*\S",
     "togliere il grassetto: un titolo vero, una frase che introduce il concetto o la prosa"),
    ("riga tutta in grassetto", "verifica", "regola 20", r"^\s*\*\*[^*\n]{1,60}\*\*\s*$",
     "se fa da titolo, usare un titolo vero"),
    ("gerundio in coda", "verifica", "pattern 2 e 21", r", [a-zàèéìòù]+(?:ando|endo)\b",
     "controllare che non sia parassita o irrelato"),
    ("suspense", "verifica", "leak conversazionale",
     r"(?i)\b(?:qui sta il punto|ecco la cosa|la verità è che|il fatto è che|è (?:un altro|un['’]altra|questo|questa)[.:])",
     "dire subito la cosa"),
]
MAX_SEGNAPOSTO = 3
# Un segnaposto è fra parentesi quadre; non lo sono i collegamenti Markdown
# «[testo](indirizzo)» o «[testo][rif]», le definizioni «[1]: indirizzo», le
# note «[^1]», le caselle «[ ]» e «[x]» né le omissioni «[…]» delle citazioni.
RX_SEGNAPOSTO = re.compile(r"(?<!\])\[(?![ xX]\]|\^|…\]|\.\.\.\])[^\]\n]{1,80}\](?![(\[])")
# L'elenco «Da completare» della regola 18 è una riga che contiene solo il suo
# titolo, con eventuali segni di Markdown: «## Da completare», «**Da completare:**»,
# «_Da completare_» (il trattino basso conta come lettera per \W, quindi va a parte).
RX_DA_COMPLETARE = re.compile(r"^[\W_]*da completare[\W_]*$", re.IGNORECASE)
# Una riga dell'elenco: una voce («- », «* », «+ », «1. », «1) ») o la sua
# continuazione rientrata.
RX_VOCE_DI_ELENCO = re.compile(r"^\s*(?:[-*+]|\d+[.)])\s")
RX_CONTINUAZIONE = re.compile(r"^\s+\S")
# Le definizioni dei collegamenti, «[1]: indirizzo», stanno a inizio riga.
RX_DEFINIZIONE = re.compile(r"^\s{0,3}\[[^\]\n]+\]:")
# Righe che non sono prosa: elenchi e titoli, a ogni livello («#» fino a «######»).
RX_NON_PROSA = re.compile(r"^\s*(?:[-*+]|#{1,6}|\d+[.)])\s")
# Le regole di frequenza danno una misura, non una quota: lo script segnala
# come certo solo l'eccesso evidente, circa il triplo del valore umano.
# Nei blog umani di PAISÀ la virgola prima di «e» compare circa una volta ogni
# 550 parole e il punto e virgola circa una volta ogni 600: il triplo vale
# per entrambi una volta ogni 200 parole.
PAROLE_PER_VIRGOLA_E = 200
PAROLE_PER_PUNTO_E_VIRGOLA = 200
# Sotto le 400 parole due virgole lecite basterebbero a superare la soglia.
MIN_PAROLE_SOGLIA_VIRGOLE = 400
# Oltre questa lunghezza, una prosa senza nessun punto e virgola va guardata.
MIN_PAROLE_SENZA_PUNTO_E_VIRGOLA = 900
# Nei blog umani di PAISÀ, contando come qui e in extras/misura_campione.py le
# frasi di almeno tre parole, la frase media è di 26,5 parole e più di una su
# cinque supera le 35; nei blog generati la media era di 15 e quasi nessuna
# arrivava a 35. Lo stesso numero sta nella regola 15 di SKILL.md.
MEDIA_FRASE_UMANA = 26.5
MEDIA_FRASE_MINIMA = 17
SOGLIA_PERIODO_LUNGO = 30
QUOTA_PERIODI_LUNGHI = 0.05


def taglia(testo):
    """Restituisce le righe del testo prima dell'elenco «Da completare».

    L'elenco sta in fondo al testo (regola 18): si taglia all'ultimo titolo
    «Da completare» solo se dopo viene un elenco vero, cioè almeno una voce,
    e ogni riga piena è una voce o la continuazione rientrata di una voce già
    vista. Un titolo seguito da prosa, o da sole righe rientrate, non taglia
    niente, così il testo che viene dopo resta controllato.
    """
    righe = testo.splitlines()
    for indice in range(len(righe) - 1, -1, -1):
        if RX_DA_COMPLETARE.match(righe[indice]):
            if solo_elenco(righe[indice + 1:]):
                return righe[:indice]
            break
    return righe


def solo_elenco(righe):
    """Vero se le righe sono un elenco: almeno una voce, poi solo voci, continuazioni o righe vuote."""
    voce_vista = False
    for riga in righe:
        if not riga.strip():
            continue
        if RX_VOCE_DI_ELENCO.match(riga):
            voce_vista = True
        elif not (voce_vista and RX_CONTINUAZIONE.match(riga)):
            return False
    return voce_vista


def controlla(testo):
    """Restituisce l'elenco delle segnalazioni come tuple (riga, colonna, nome, livello, regola, estratto, nota)."""
    if testo.startswith("\ufeff"):
        testo = testo[1:]  # il BOM del vecchio Blocco note toglierebbe la prima riga ai controlli con «^»
    trovati = []
    oxford = []
    righe = taglia(testo)
    for indice, riga in enumerate(righe):
        numero = indice + 1
        # Un paragrafo spezzato a mano può avere un'occorrenza a cavallo di due
        # righe: si cerca nella riga unita alla seguente, se questa non è vuota,
        # e si tiene ciò che comincia in questa riga. Ciò che comincia nella
        # seguente si trova quando tocca a lei.
        seguente = righe[indice + 1] if indice + 1 < len(righe) else ""
        giunta = riga + " " + seguente if seguente.strip() else riga
        for nome, livello, regola, rx, nota in CONTROLLI:
            for m in re.finditer(rx, giunta):
                if m.start() >= len(riga):
                    continue
                if nome == "virgola prima di e" and any(
                        r == numero and inizio <= m.start() < fine for r, inizio, fine in oxford):
                    continue  # la virgola di Oxford, più grave, la copre già
                if nome == "virgola di Oxford":
                    oxford.append((numero, m.start(), m.end()))
                inizio = max(0, m.start() - 25)
                estratto = giunta[inizio:m.end() + 25].strip()
                trovati.append((numero, m.start() + 1, nome, livello, regola, estratto, nota))
    segnaposto = [s for riga in righe if not RX_DEFINIZIONE.match(riga) for s in RX_SEGNAPOSTO.findall(riga)]
    if len(segnaposto) > MAX_SEGNAPOSTO:
        trovati.append((0, 0, "troppi segnaposto", "certo", "regola 18",
                        f"{len(segnaposto)} segnaposto",
                        f"al massimo {MAX_SEGNAPOSTO}: i dati mancanti vanno tutti nell'elenco «Da completare»"))
    # Le soglie di frequenza contano parole e virgole sulla stessa prosa:
    # elenchi e titoli restano fuori da entrambi i conti.
    non_prosa = {i + 1 for i, r in enumerate(righe) if RX_NON_PROSA.match(r)}
    prosa = "\n".join(r for i, r in enumerate(righe) if i + 1 not in non_prosa)
    parole = len(prosa.split())
    virgole_e = sum(1 for t in trovati
                    if t[2] in ("virgola prima di e", "virgola di Oxford") and t[0] not in non_prosa)
    if parole >= MIN_PAROLE_SOGLIA_VIRGOLE and virgole_e >= 3 and virgole_e * PAROLE_PER_VIRGOLA_E > parole:
        trovati.append((0, 0, "troppe virgole prima di e", "certo", "regola 17",
                        f"{virgole_e} in {parole} parole",
                        f"più di una ogni {PAROLE_PER_VIRGOLA_E} parole, circa il triplo della prosa umana: "
                        "tenere solo quelle dei casi ammessi"))
    punti_e_virgola = prosa.count(";")
    if punti_e_virgola >= 2 and punti_e_virgola * PAROLE_PER_PUNTO_E_VIRGOLA > parole:
        trovati.append((0, 0, "troppi punti e virgola", "certo", "regola 19",
                        f"{punti_e_virgola} in {parole} parole",
                        f"più di uno ogni {PAROLE_PER_PUNTO_E_VIRGOLA} parole: tenere solo quelli che la sintassi chiede"))
    frasi = [len(s.split()) for s in re.split(r"(?<=[.!?])\s+", " ".join(prosa.split())) if len(s.split()) > 2]
    if len(frasi) >= 15:
        media = sum(frasi) / len(frasi)
        lunghi = sum(1 for n in frasi if n > SOGLIA_PERIODO_LUNGO) / len(frasi)
        if media < MEDIA_FRASE_MINIMA and lunghi < QUOTA_PERIODI_LUNGHI:
            umana = f"{MEDIA_FRASE_UMANA:.1f}".replace(".", ",")
            trovati.append((0, 0, "frasi corte e uniformi", "verifica", "regola 15",
                            f"media {media:.0f} parole, {100 * lunghi:.0f}% oltre le {SOGLIA_PERIODO_LUNGO}",
                            f"nei blog umani la media è di {umana} parole: "
                            "unire in periodi lunghi i ragionamenti spezzati"))
    if parole > MIN_PAROLE_SENZA_PUNTO_E_VIRGOLA and ";" not in prosa:
        trovati.append((0, 0, "nessun punto e virgola", "verifica", "regola 19",
                        f"{parole} parole di prosa",
                        f"oltre le {MIN_PAROLE_SENZA_PUNTO_E_VIRGOLA} parole guardare se due proposizioni legate "
                        "lo chiedono; nessuno è lecito se nessuna lo chiede"))
    return sorted(trovati)


def stampa(nome_file, trovati):
    certi = sum(1 for t in trovati if t[3] == "certo")
    print(f"== {nome_file}: {certi} da correggere, {len(trovati) - certi} da verificare")
    for riga, col, nome, livello, regola, estratto, nota in trovati:
        dove = f"{riga}:{col}" if riga else "testo"
        segno = "!!" if livello == "certo" else "??"
        print(f"  {segno} {dove:>7}  {nome} ({regola}): …{estratto}…")
        print(f"             {nota}")
    return certi


def decodifica(dati, nome):
    """Decodifica i byte in UTF-8, o esce con codice 2 e un messaggio chiaro."""
    try:
        return dati.decode("utf-8-sig")
    except UnicodeDecodeError:
        print(f"Errore: {nome} non è un testo in UTF-8.", file=sys.stderr)
        sys.exit(2)


def leggi(nome):
    if nome == "-":
        return decodifica(sys.stdin.buffer.read(), "lo standard input")
    try:
        with open(nome, "rb") as f:
            dati = f.read()
    except OSError as errore:
        print(f"Errore: non riesco a leggere {nome} ({errore.strerror}).", file=sys.stderr)
        sys.exit(2)
    return decodifica(dati, nome)


def esce_con(funzione, *argomenti):
    """Esegue una funzione che chiude con sys.exit e restituisce il codice.

    I messaggi d'errore attesi vanno in un buffer, così il registro della
    continua mostra solo l'esito delle autoprove.
    """
    try:
        with contextlib.redirect_stderr(io.StringIO()):
            funzione(*argomenti)
    except SystemExit as uscita:
        return uscita.code
    except Exception as errore:  # un'eccezione non gestita è proprio il difetto da cogliere
        return type(errore).__name__
    return None


def prova():
    # (testo, controllo, atteso, livello atteso o None)
    casi = [
        ("Il fenomeno si chiama retrogradazione, e spiega tutto.", "virgola prima di e", True, "verifica"),
        ("Il fenomeno si chiama retrogradazione e spiega tutto.", "virgola prima di e", False, None),
        ("Sono lente, costose, e lasciano strascichi.", "virgola di Oxford", True, "certo"),
        ("Sono lente, costose, e lasciano strascichi.", "virgola prima di e", False, None),
        ("La soluzione — che pareva impossibile — funziona.", "em-dash", True, "certo"),
        ("Non è un problema tecnico, è un problema di soldi.", "contrasto fittizio", True, "certo"),
        ("Non è un problema tecnico. È un problema di soldi.", "contrasto fittizio su due frasi", True, "verifica"),
        ("Non è un problema tecnico e lo sappiamo.", "contrasto fittizio su due frasi", False, None),
        ("Non solo veloce ma anche economico.", "non solo… ma anche", True, "certo"),
        ("Qual'è il punto?", "errore ortografico", True, "certo"),
        ("Perché no?", "errore ortografico", False, None),
        ("La strada più frequente è un'altra.", "suspense", True, "verifica"),
        ("Il motivo preciso è questo. Poi il resto.", "suspense", True, "verifica"),
        ("Ha firmato il decreto, confermando la linea.", "gerundio in coda", True, "verifica"),
        ("Un approfondimento utile sul tema.", "lessico AI", True, "verifica"),
        ("«Certo!» rispose lei, e uscì.", "artefatto da chatbot", True, "verifica"),
        ("Prezzo [prezzo], data [data], ora [ora], luogo [luogo].", "troppi segnaposto", True, "certo"),
        ("Prezzo [prezzo].\n\nDa completare\n- [a] [b] [c] [d]", "troppi segnaposto", False, None),
        ("Prezzo [prezzo].\n\n**DA COMPLETARE:**\n- [a] [b] [c] [d]", "troppi segnaposto", False, None),
        ("Vedi [la guida](https://a.it), [il modulo](https://b.it), [il listino](https://c.it) "
         "e [le date][1].", "troppi segnaposto", False, None),
        ("- [ ] uno\n- [x] due\n- [ ] tre\n- [X] quattro\n- [ ] cinque", "troppi segnaposto", False, None),
        ("Vedi [a][1], [b][2], [c][3], [d][4] e [e][5].", "troppi segnaposto", False, None),
        ("Vedi [a][1].\n\n[1]: https://a.it\n[2]: https://b.it\n[3]: https://c.it\n[4]: https://d.it",
         "troppi segnaposto", False, None),
        ("Nota[^1], nota[^2], nota[^3] e nota[^4].", "troppi segnaposto", False, None),
        ("«Disse […] che sarebbe venuto [...] e poi […] se ne andò […].»", "troppi segnaposto", False, None),
        ("[inserire qui il nome e cognome del cliente] [b] [c] [d]", "troppi segnaposto", True, "certo"),
        ("Prezzo [prezzo].\n\n_Da completare_\n- [a] [b] [c] [d]", "troppi segnaposto", False, None),
        ("Prezzo [prezzo].\n\n## Da completare\n- [a] [b] [c] [d]", "troppi segnaposto", False, None),
        ("Un’altro esempio.", "errore ortografico", True, "certo"),
        ("Nell’era digitale tutto cambia.", "incipit formulaico", True, "certo"),
        ("Non è un problema tecnico.\nÈ un problema di soldi.", "contrasto fittizio su due frasi", True, "verifica"),
        ("Non è un problema tecnico,\nè un problema di soldi.", "contrasto fittizio", True, "certo"),
        ("**Margine**\n\nIl margine scende.", "riga tutta in grassetto", True, "verifica"),
        ("Il margine è **molto** basso.", "riga tutta in grassetto", False, None),
        ("\ufeff**Margine.** Il margine scende.", "titoletto in grassetto", True, "certo"),
        ("Sono lente, costose, e «definitive».", "virgola di Oxford", True, "certo"),
        ("parola " * 400 + "fine.\n- a, e b\n- c, e d\n- f, e g", "troppe virgole prima di e", False, None),
        ("parola " * 400 + "fine.\n+ a, e b\n1) c, e d\n2) f, e g", "troppe virgole prima di e", False, None),
        ("Da completare entro lunedì il modulo.\nLa soluzione — impossibile — funziona.", "em-dash", True, "certo"),
        # L'elenco «Da completare» si taglia solo se sta in fondo: un elenco in
        # testa, un titolo seguito da prosa o un primo titolo fra due non
        # tolgono il testo che viene dopo; la voce che va a capo rientrata sì.
        ("## Da completare\n- prezzo\n\nLa soluzione — impossibile — funziona.", "em-dash", True, "certo"),
        ("Prima parte.\n\n**Da completare**\n\nLa soluzione — impossibile — funziona.", "em-dash", True, "certo"),
        ("## Da completare\n\nLa soluzione — impossibile — funziona.\n\n## Da completare\n- prezzo",
         "em-dash", True, "certo"),
        ("Testo.\n\nDa completare:\n- prezzo del corso,\n  da chiedere — subito", "em-dash", False, None),
        # Senza una voce non c'è elenco: righe solo rientrate, o rientrate prima
        # della prima voce, non tagliano.
        ("Prima parte.\n\n## Da completare\n    La soluzione — impossibile — funziona.", "em-dash", True, "certo"),
        ("Testo.\n\n## Da completare\n  riga rientrata — prima\n- prezzo", "em-dash", True, "certo"),
        ("Testo.\n\n**Da completare**\n\n", "riga tutta in grassetto", True, "verifica"),
        # I due punti dopo un segnaposto a metà riga non lo nascondono: solo le
        # definizioni a inizio riga («[1]: indirizzo») restano fuori dal conto.
        ("Prezzo [prezzo]: x. Scadenza [scadenza]: y. Luogo [luogo]: z. Nome [nome]: w.",
         "troppi segnaposto", True, "certo"),
        # I titoli di ogni livello restano fuori dal conto delle parole: con «##»
        # le loro parole non devono diluire la soglia del punto e virgola.
        ("\n".join(["## Titolo" + " lungo" * 20] * 10) + "\n\nUna frase; un'altra frase; " + "parola " * 380 + "fine.",
         "troppi punti e virgola", True, "certo"),
        ("\n".join(["###### Titolo" + " lungo" * 20] * 10) + "\n\nUna frase; un'altra frase; " + "parola " * 380 + "fine.",
         "troppi punti e virgola", True, "certo"),
        ("Ho scritto \"ciao\".", "virgolette inglesi", True, "certo"),
        ("Ho scritto «ciao».", "virgolette inglesi", False, None),
        ("Una frase qualsiasi. " * 350, "nessun punto e virgola", True, "verifica"),
        ("Una frase qualsiasi; " * 350, "nessun punto e virgola", False, None),
        ("Breve testo senza punto e virgola.", "nessun punto e virgola", False, None),
        ("**Margine.** Il margine lordo scende.", "titoletto in grassetto", True, "certo"),
        ("- **Sicurezza:** la sicurezza è rafforzata.", "titoletto in grassetto", True, "certo"),
        ("Il margine è **molto** basso.", "titoletto in grassetto", False, None),
        ("Testo." + chr(10) * 2 + "**Da completare**" + chr(10) + "- prezzo", "titoletto in grassetto", False, None),
        ("Piove, e noi usciamo. " + "parola " * 400 + "Sole, e loro restano. Vento, e lei parte.",
         "troppe virgole prima di e", True, "certo"),
        ("Piove, e noi usciamo. " + "parola " * 900 + "Sole, e loro restano.", "troppe virgole prima di e", False, None),
        ("Piove, e noi usciamo. " + "parola " * 250 + "Sole, e loro restano.", "troppe virgole prima di e", False, None),
        ("Uno; " + "parola " * 150 + "due; " + "parola " * 100 + "tre; quattro.", "troppi punti e virgola", True, "certo"),
        ("Uno; " + "parola " * 650 + "due.", "troppi punti e virgola", False, None),
        ("Breve frase qui. " * 20, "frasi corte e uniformi", True, "verifica"),
        (("Un periodo lungo che tiene insieme cause condizioni e conseguenze senza spezzarsi in frasi corte "
          "tutte uguali fra loro e che continua ancora un poco perché deve superare con margine la soglia "
          "delle trenta parole. " + "Breve frase qui. ") * 10, "frasi corte e uniformi", False, None),
    ]
    falliti = 0
    for testo, nome, atteso, livello in casi:
        trovati = [t for t in controlla(testo) if t[2] == nome]
        if bool(trovati) != atteso or (atteso and livello and trovati[0][3] != livello):
            falliti += 1
            print(f"FALLITA: {nome!r} su {testo[:60]!r}: atteso {atteso} {livello or ''}, "
                  f"trovato {[t[3] for t in trovati]}")
    def primo(nome):
        """Il primo testo dell'elenco che deve far scattare il controllo indicato."""
        return next(testo for testo, n, atteso, _ in casi if n == nome and atteso)

    # Le note delle soglie dicono gli stessi numeri del codice.
    attese = {"troppe virgole prima di e": str(PAROLE_PER_VIRGOLA_E),
              "troppi punti e virgola": str(PAROLE_PER_PUNTO_E_VIRGOLA),
              "nessun punto e virgola": str(MIN_PAROLE_SENZA_PUNTO_E_VIRGOLA)}
    for nome, numero in attese.items():
        nota = next((t[6] for t in controlla(primo(nome)) if t[2] == nome), "")
        if numero not in nota:
            falliti += 1
            print(f"FALLITA: la nota di {nome!r} non dice {numero}: {nota!r}")
    # La virgola di Oxford porta l'etichetta della grammatica, non di una regola del fork.
    oxford = [t for t in controlla(primo("virgola di Oxford")) if t[2] == "virgola di Oxford"]
    if not oxford or oxford[0][4] != "grammatica §8":
        falliti += 1
        print(f"FALLITA: etichetta della virgola di Oxford: {oxford}")
    # Un file che non si legge, o che non è UTF-8, chiude con 2 e non con 1.
    codici = (esce_con(leggi, "file-che-non-esiste-davvero.md"), esce_con(decodifica, b"\xff\xfe\xfa", "prova"),
              esce_con(main, []))
    if codici != (2, 2, 2):
        falliti += 1
        print(f"FALLITA: codici di uscita per file assente, non UTF-8 e uso sbagliato: {codici}")
    # Un file con il BOM si legge senza il carattere invisibile in testa.
    if decodifica("\ufeffciao".encode("utf-8"), "prova") != "ciao":
        falliti += 1
        print("FALLITA: il BOM resta nel testo letto da file")
    # Il riepilogo concorda con il numero: \u00ab1 fallito\u00bb, \u00ab0 falliti\u00bb.
    if (riepilogo(64, 1), riepilogo(1, 0)) != ("64 casi, 1 fallito.", "1 caso, 0 falliti."):
        falliti += 1
        print(f"FALLITA: riepilogo non concordato: {riepilogo(64, 1)!r}, {riepilogo(1, 0)!r}")
    totale = len(casi) + len(attese) + 4
    print(riepilogo(totale, falliti))
    return 1 if falliti else 0


def riepilogo(totale, falliti):
    """La riga finale dell'autoprova, con il nome concordato al numero."""
    casi = "caso" if totale == 1 else "casi"
    esito = "fallito" if falliti == 1 else "falliti"
    return f"{totale} {casi}, {falliti} {esito}."


def main(argomenti):
    if not argomenti:
        print(__doc__, file=sys.stderr)
        sys.exit(2)
    if argomenti == ["--prova"]:
        sys.exit(prova())
    totale_certi = 0
    for nome in argomenti:
        totale_certi += stampa(nome, controlla(leggi(nome)))
    sys.exit(1 if totale_certi else 0)


if __name__ == "__main__":
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    main(sys.argv[1:])

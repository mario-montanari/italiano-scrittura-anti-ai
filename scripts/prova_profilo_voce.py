#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Prove automatiche di `profilo_voce.py`.

Si lancia senza installare niente:

    python scripts/prova_profilo_voce.py

Sola libreria standard, nessuna rete, nessuna scrittura fuori da una
cartella temporanea che viene rimossa alla fine.

Ogni prova qui dentro nasce da un difetto trovato davvero, in un audit o in
un collaudo, e serve a impedire che torni. È la memoria degli errori già
fatti. La copertura del codice resta un'altra cosa, e questo file non la
insegue.
"""
from __future__ import annotations

import json
import os
import re
import sys
import tempfile
import textwrap
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import profilo_voce as pv  # noqa: E402

NL = chr(10)

# Ogni riga chiude con punteggiatura forte: una riga che non lo fa, e che sta
# sotto le quindici parole, lo strumento la tratta da titolo e non la conta.
TESTO_ACCENTATO = (
    "Perché scrivo così? Perché la voce è mia, ed è quello che conta." + NL
    + "Non è più una questione di gusto, poiché è già diventata mestiere." + NL
    + "Benché il metodo sia semplice, il risultato non è affatto scontato." + NL
    + "Però affinché la misura serva davvero va letta con i suoi limiti." + NL
)

TESTO_A_CAPO_SINGOLO = (
    "Primo paragrafo, scritto su una riga sola." + NL
    + "Secondo paragrafo, anche lui su una riga sola." + NL
    + "Terzo paragrafo isolato, che sta in piedi da solo." + NL
    + "Quarto e ultimo paragrafo del file, con il ritorno a capo finale." + NL
)

# I segni che la skill vieta si costruiscono per codice invece di scriverli:
# il controllo anti-pattern del workspace legge anche questo file.
TRATTINO_LUNGO = chr(8212)
VIRGOLETTA_INGLESE_APERTA = chr(8220)
VIRGOLETTA_INGLESE_CHIUSA = chr(8221)

# Serve a far scattare l'avviso sui segni fuori norma, che stampa numeri
# fuori dalle tabelle: è uno dei rami in cui i decimali possono sfuggire.
TESTO_FUORI_NORMA = (
    "La voce si riconosce dal passo " + TRATTINO_LUNGO + " e non dal lessico."
    + NL
    + "Chi legge lo sente subito, e dice "
    + VIRGOLETTA_INGLESE_APERTA
    + "questo l'ha scritto lui"
    + VIRGOLETTA_INGLESE_CHIUSA
    + " senza pensarci."
    + NL
    + "Un testo pulito " + TRATTINO_LUNGO + " ma senza voce " + TRATTINO_LUNGO
    + " resta comunque muto." + NL
)

esiti: list = []
saltate: list = []


def verifica(nome: str, condizione: bool, dettaglio: str = "") -> None:
    esiti.append((nome, condizione, dettaglio))
    segno = "ok  " if condizione else "FALLITA"
    print("{} {}{}".format(segno, nome, (" -> " + dettaglio) if dettaglio else ""))


def accorda(quantita: int, singolare: str, plurale: str) -> str:
    """Concorda il nome con il numero. Lo zero in italiano vuole il plurale."""
    return "{} {}".format(quantita, singolare if quantita == 1 else plurale)


def salta(nome: str, motivo: str) -> None:
    """Registra una prova che il sistema non ha permesso di eseguire.

    Serve a distinguere un controllo superato da un controllo mai messo alla
    prova. Senza questo, il riepilogo diceva «0 fallite» in tutti e due i
    casi, e la prova di sicurezza che salta sempre su Windows passava per
    una prova andata bene.
    """
    saltate.append((nome, motivo))
    print("SALTATA {} -> {}".format(nome, motivo))


def prova_accenti_riconosciuti(radice: Path) -> None:
    """Un connettivo scritto con l'accento deve contare come connettivo.

    Il difetto originale: le liste chiuse contenevano solo forme senza
    accento, e nessuna funzione toglieva gli accenti dal testo. Risultato,
    un italiano scritto bene veniva misurato peggio di uno scritto male.
    """
    corpus = radice / "accenti"
    corpus.mkdir()
    (corpus / "testo.txt").write_text(TESTO_ACCENTATO, encoding="utf-8")
    profilo = pv.calcola_profilo(corpus, "Prova")
    ricorrenze = profilo["ricorrenze"]
    connettivi = dict(ricorrenze["connettivi_frequenti"])
    for parola in ("perché", "poiché", "benché", "affinché"):
        verifica(
            "connettivo accentato riconosciuto: {}".format(parola),
            parola in connettivi,
            "trovati: {}".format(sorted(connettivi)),
        )
    piene = dict(ricorrenze["parole_piene_frequenti"])
    for vuota in ("più", "già", "però", "è"):
        verifica(
            "parola vuota accentata esclusa dalle piene: {}".format(vuota),
            vuota not in piene,
        )


def prova_paragrafi_a_capo_singolo(radice: Path) -> None:
    """Quattro righe senza righe vuote sono quattro paragrafi, non uno.

    Il difetto originale: il ritorno a capo finale, che quasi ogni editor
    lascia, veniva contato come riga vuota e faceva scattare la regola dello
    stile Markdown su un file che non lo era.
    """
    esclusioni: pv.Counter = pv.Counter()
    righe = pv.classifica_righe(TESTO_A_CAPO_SINGOLO, esclusioni)
    stile = pv.righe_vuote_separano_i_paragrafi(righe)
    verifica("stile riconosciuto come ritorno a capo singolo", stile is False)
    paragrafi = pv.costruisci_paragrafi(righe, stile)
    verifica(
        "quattro righe danno quattro paragrafi",
        len(paragrafi) == 4,
        "ottenuti: {}".format(len(paragrafi)),
    )


def prova_uscita_esclusa_dal_corpus(radice: Path) -> None:
    """Il secondo lancio non deve leggere la scheda del primo.

    Il difetto originale: senza l'opzione di uscita la scheda finiva accanto
    ai testi, e al rilancio veniva analizzata come prosa dell'autore.
    """
    corpus = radice / "rilancio"
    corpus.mkdir()
    (corpus / "testo.md").write_text(TESTO_ACCENTATO, encoding="utf-8")
    codice = pv.main([str(corpus), "--nome", "Prova"])
    verifica(
        "il lancio dello strumento esce con codice zero",
        codice == 0,
        "codice di uscita: {}".format(codice),
    )
    verifica(
        "la scheda è stata scritta accanto al corpus",
        (corpus / "scheda-voce.md").exists(),
    )
    letti = [percorso.name for percorso in pv.raccogli_file(corpus)]
    verifica(
        "il secondo lancio non legge le proprie uscite",
        letti == ["testo.md"],
        "letti: {}".format(letti),
    )


def prova_accenti_nel_sorgente(radice: Path) -> None:
    """Il sorgente dello strumento scrive l'italiano con gli accenti.

    Il difetto originale: commenti e docstring dicevano *piu*, *perche*,
    *e* al posto di *è*, in una skill che vende ortografia italiana. Il
    `CHANGELOG.md` dichiarava per giunta che le sole forme senza accento
    fossero le chiavi del JSON, e non era vero.

    Le forme dentro `ABBREVIAZIONI`, `PAROLE_VUOTE` e `CONNETTIVI` sono
    escluse apposta: lì la mancanza di accento è il dato, perché quegli
    elenchi servono a riconoscere anche chi scrive senza accenti.

    Limite dichiarato: questa prova trova le forme che esistono solo
    accentate. La *e* che dovrebbe essere *è* non è cercabile così, perché
    *e* è anche una congiunzione legittima, e resta materia di lettura.
    """
    sorgente = Path(pv.__file__).read_text(encoding="utf-8").splitlines()

    chiusi = []
    for nome in ("ABBREVIAZIONI", "PAROLE_VUOTE", "CONNETTIVI"):
        inizio = None
        for numero, riga in enumerate(sorgente, 1):
            if riga.startswith(nome + " ="):
                inizio = numero
            elif inizio and riga.strip() == ")":
                chiusi.append((inizio, numero))
                break
    verifica(
        "i tre elenchi chiusi sono stati individuati",
        len(chiusi) == 3,
        "trovati: {}".format(chiusi),
    )

    forme = (
        "piu perche poiche gia pero cioe puo sara avra andra benche affinche "
        "altresi nonche finche cosi citta universita qualita attivita meta "
        "verita liberta identita novita unita"
    ).split()
    residui = []
    for numero, riga in enumerate(sorgente, 1):
        if any(da <= numero <= a for da, a in chiusi):
            continue
        for forma in forme:
            if re.search(r"(?<![\w'])" + forma + r"(?![\w'])", riga):
                residui.append("{}: {}".format(numero, riga.strip()[:60]))
                break
    verifica(
        "nessuna forma senza accento fuori dagli elenchi chiusi",
        not residui,
        "residui: {}".format(residui[:3]),
    )


def prova_a_capo_rigido_non_fa_sparire_la_prosa(radice: Path) -> None:
    """Un paragrafo mandato a capo a larghezza fissa resta prosa.

    Il difetto originale: ogni riga che non finiva con punteggiatura forte e
    stava sotto le quindici parole veniva presa per titolo ed esclusa dai
    conteggi. Su un file con a capo rigido, che è il formato comune dei .txt
    scritti a mano o esportati senza reflow, quasi tutta la prosa spariva in
    silenzio: settantanove parole reali, ventuno contate a settanta colonne.

    L'invariante provata qui: mandare a capo lo stesso testo non deve
    cambiare la misura. Il confronto è con il file senza a capo rigido, non
    con un numero scritto a mano, così la prova regge anche se un giorno
    cambia il modo di contare le parole.
    """
    paragrafo = (
        "La città si sveglia presto, e chi ci abita lo sa da sempre. Le "
        "saracinesche salgono una dopo l'altra, il caffè scivola nelle tazze, "
        "qualcuno legge il giornale appoggiato al bancone. Non c'è niente di "
        "straordinario in questo, eppure ogni mattina somiglia a un piccolo "
        "spettacolo che si ripete uguale. Chi arriva da fuori lo nota subito, "
        "e chi ci vive non ci fa più caso, e forse è proprio questo il segno "
        "che un luogo è diventato casa."
    )

    def misura(nome: str, contenuto: str, estensione: str = "txt") -> int:
        corpus = radice / nome
        corpus.mkdir()
        (corpus / ("testo." + estensione)).write_text(contenuto, encoding="utf-8")
        return pv.calcola_profilo(corpus, "Prova")["corpus"]["parole_totali"]

    # Caso di controllo: il file senza a capo rigido, che oggi funziona e non
    # va rotto dalla correzione. È lui a dare la misura attesa.
    atteso = misura("acapo-nessuno", paragrafo + NL)
    verifica(
        "il file senza a capo rigido conta tutte le parole",
        atteso == len(paragrafo.split()),
        "attese {}, contate {}".format(len(paragrafo.split()), atteso),
    )

    for colonne in (60, 70, 80, 90):
        contate = misura(
            "acapo-{}".format(colonne), textwrap.fill(paragrafo, colonne) + NL
        )
        verifica(
            "a capo a {} colonne: la prosa resta contata".format(colonne),
            contate == atteso,
            "attese {}, contate {}".format(atteso, contate),
        )

    contate_md = misura("acapo-md", textwrap.fill(paragrafo, 70) + NL, "md")
    verifica(
        "a capo rigido in un file .md: la prosa resta contata",
        contate_md == atteso,
        "attese {}, contate {}".format(atteso, contate_md),
    )

    # L'altro lato della correzione: un titolo vero, isolato fra righe vuote,
    # deve restare fuori dai conteggi come prima.
    prosa = (
        "Si impara cadendo, e non lo si dimentica più. Chi pretende di "
        "insegnarlo in tre lezioni vende qualcosa che non possiede."
    )
    con_titolo = misura(
        "titolo-vero", "Il mestiere di scrivere" + NL + NL + prosa + NL
    )
    verifica(
        "un titolo isolato fra righe vuote resta escluso",
        con_titolo == len(prosa.split()),
        "attese {}, contate {}".format(len(prosa.split()), con_titolo),
    )


def prova_decimali_allitaliana(radice: Path) -> None:
    """La scheda scrive i decimali con la virgola, il JSON li lascia col punto.

    Il difetto originale: ogni numero della scheda consegnata all'utente
    usava il punto anglosassone, mentre la repo e le stringhe di confronto
    dello stesso script usano la virgola. La correzione sta in una funzione
    applicata al valore prima che diventi testo: una sostituzione sul
    documento finito avrebbe preso anche i numeri di versione.
    """
    verifica("il decimale prende la virgola", pv.numero(0.246) == "0,246",
             "ottenuto: {}".format(pv.numero(0.246)))
    verifica("il decimale intero tiene la virgola", pv.numero(8.0) == "8,0",
             "ottenuto: {}".format(pv.numero(8.0)))
    verifica("l'intero resta intero", pv.numero(12) == "12")
    verifica("il numero di versione non si tocca", pv.numero("1.0.0") == "1.0.0")

    corpus = radice / "decimali"
    corpus.mkdir()
    (corpus / "uno.txt").write_text(TESTO_ACCENTATO, encoding="utf-8")
    # Il secondo file fa scattare l'avviso sui segni fuori norma, che stampa
    # numeri in prosa e non dentro una tabella.
    (corpus / "due.txt").write_text(TESTO_FUORI_NORMA, encoding="utf-8")
    profilo = pv.calcola_profilo(corpus, "Prova")
    scheda = pv.scrivi_scheda(profilo)

    residui = [
        riga.strip()
        for riga in scheda.splitlines()
        if re.search(r"\d+\.\d+", riga) and "versione" not in riga
    ]
    verifica(
        "nessun decimale col punto resta nella scheda",
        not residui,
        "righe: {}".format(residui[:3]),
    )
    verifica(
        "l'avviso sui segni fuori norma usa la virgola",
        any(
            riga.startswith("**Avviso.**") and re.search(r"\d+,\d+", riga)
            for riga in scheda.splitlines()
        ),
    )
    verifica(
        "la riga della versione resta col punto",
        any("versione 1.4.0" in riga for riga in scheda.splitlines()),
    )
    verifica(
        "nel profilo il numero resta un numero, e il JSON tiene il punto",
        isinstance(profilo["leggibilita"]["gulpease_corpus"], float),
    )


def prova_file_illeggibile_non_ferma_il_corpus(radice: Path) -> None:
    """Un file indecifrabile viene escluso, e gli altri si elaborano lo stesso.

    Il difetto originale: `leggi_file` solleva `ErroreCorpus`, che discende da
    `Exception` e non da `OSError`, mentre il ciclo di lettura catturava il
    solo `OSError`. Un file con un byte che nessuna delle codifiche tentate
    accetta fermava tutta l'esecuzione, e faceva perdere anche il lavoro già
    fatto sui file sani, mentre il `CHANGELOG.md` prometteva il contrario.
    """
    # I cinque byte che cp1252 lascia indefiniti: sono l'unico modo di
    # costruire un file che non decodifica in nessuna delle tre codifiche.
    for byte_indefinito in (0x81, 0x8D, 0x8F, 0x90, 0x9D):
        corpus = radice / "illeggibile-{:02x}".format(byte_indefinito)
        corpus.mkdir()
        (corpus / "aaa_buono.txt").write_text(TESTO_ACCENTATO, encoding="utf-8")
        (corpus / "zzz_rotto.txt").write_bytes(bytes([0x41, byte_indefinito, 0x42]))
        try:
            profilo = pv.calcola_profilo(corpus, "Prova")
        except pv.ErroreCorpus as errore:
            verifica(
                "il byte 0x{:02X} non ferma il corpus".format(byte_indefinito),
                False,
                "sollevata ErroreCorpus: {}".format(errore),
            )
            continue
        corpo = profilo["corpus"]
        verifica(
            "il byte 0x{:02X} non ferma il corpus".format(byte_indefinito),
            corpo["file_letti"] == 1 and corpo["parole_totali"] > 0,
            "file letti: {}, parole: {}".format(
                corpo["file_letti"], corpo["parole_totali"]
            ),
        )
        verifica(
            "il file 0x{:02X} è dichiarato fra le esclusioni".format(byte_indefinito),
            corpo["esclusioni_in_pulizia"].get("file_illeggibili") == 1,
            "esclusioni: {}".format(corpo["esclusioni_in_pulizia"]),
        )

    # Il caso opposto: se non resta niente di leggibile, l'errore deve dirlo.
    tutto_rotto = radice / "illeggibile-tutto"
    tutto_rotto.mkdir()
    (tutto_rotto / "a.txt").write_bytes(bytes([0x41, 0x81, 0x42]))
    (tutto_rotto / "b.txt").write_bytes(bytes([0x8D, 0x41]))
    try:
        pv.calcola_profilo(tutto_rotto, "Prova")
        verifica("un corpus tutto illeggibile solleva un errore", False)
    except pv.ErroreCorpus as errore:
        verifica(
            "un corpus tutto illeggibile lo dichiara nel messaggio",
            "illeggibili" in str(errore),
            "messaggio: {}".format(errore),
        )


def prova_contenimento(radice: Path) -> None:
    """Un file fuori dalla cartella non entra nel corpus.

    Su Windows la giunzione richiede privilegi, quindi la prova salta da sé
    quando il sistema non permette di creare il collegamento.
    """
    corpus = radice / "contenimento"
    corpus.mkdir()
    (corpus / "dentro.txt").write_text(TESTO_ACCENTATO, encoding="utf-8")
    fuori = radice / "fuori"
    fuori.mkdir()
    (fuori / "esterno.txt").write_text("Testo che non deve entrare." + NL, encoding="utf-8")
    try:
        (corpus / "collegamento").symlink_to(fuori, target_is_directory=True)
    except (OSError, NotImplementedError) as errore:
        salta(
            "contenimento del corpus",
            "il sistema non permette di creare il collegamento ({})".format(
                type(errore).__name__
            ),
        )
        return
    letti = [percorso.name for percorso in pv.raccogli_file(corpus)]
    verifica(
        "il file oltre il collegamento resta fuori",
        "esterno.txt" not in letti,
        "letti: {}".format(letti),
    )
    # Senza questa seconda asserzione la prova passerebbe anche con una
    # raccolta rotta che restituisce una lista vuota: «non c'è il file di
    # fuori» sarebbe vero per il motivo sbagliato.
    verifica(
        "il file di dentro è stato raccolto davvero",
        "dentro.txt" in letti,
        "letti: {}".format(letti),
    )


def prova_cartelle_collegate_non_rompono_la_scansione(radice: Path) -> None:
    """La discesa nelle cartelle non segue i collegamenti e non gira a vuoto.

    Il difetto originale: la discesa era affidata a `rglob`, che fino a
    Python 3.12 segue le directory raggiunte per collegamento simbolico senza
    riconoscere i cicli (una catena che torna su sé stessa faceva morire il
    processo per ricorsione, con traceback e corpus perso) e dal 3.13 non le
    scende affatto, facendo sparire i loro file senza che comparissero fra le
    esclusioni dichiarate.

    La decisione sta ora in `cartella_da_scendere`, provata qui su percorsi
    costruiti: è l'unico modo di coprire tutti e tre i rami su una macchina
    dove i collegamenti simbolici non si creano senza privilegi. La prova con
    un collegamento vero, sotto, salta da sé quando il sistema non lo permette.
    """
    corpus = radice / "cartelle-collegate"
    corpus.mkdir()
    (corpus / "dentro").mkdir()
    (corpus / "dentro" / "testo.txt").write_text(TESTO_ACCENTATO, encoding="utf-8")
    fuori = radice / "cartelle-collegate-fuori"
    fuori.mkdir()
    radice_risolta = corpus.resolve()

    viste = {radice_risolta}
    scendere, motivo = pv.cartella_da_scendere(corpus / "dentro", radice_risolta, viste)
    verifica(
        "in una sottocartella normale si scende",
        scendere and motivo == "",
        "ottenuto ({}, {!r})".format(scendere, motivo),
    )
    scendere, motivo = pv.cartella_da_scendere(corpus / "dentro", radice_risolta, viste)
    verifica(
        "una cartella già percorsa non si ripercorre: è così che nasce il ciclo",
        not scendere and motivo == "cartelle_gia_percorse",
        "ottenuto ({}, {!r})".format(scendere, motivo),
    )
    scendere, motivo = pv.cartella_da_scendere(fuori, radice_risolta, viste)
    verifica(
        "una cartella che porta fuori dal corpus resta fuori, e lo dichiara",
        not scendere and motivo == "cartelle_fuori_dalla_cartella",
        "ottenuto ({}, {!r})".format(scendere, motivo),
    )

    # Il ramo che il primo fix aveva aperto: un collegamento simbolico a una
    # cartella interna, con un nome che viene prima in ordine alfabetico,
    # faceva prendere nota della cartella vera senza percorrerla mai. Quando
    # la scansione la raggiungeva, risultava già percorsa e spariva dal corpus
    # con tutti i suoi file. Il collegamento va quindi riconosciuto per primo
    # e non deve toccare l'insieme delle cartelle viste. Il caso si costruisce
    # con un oggetto che si dichiara collegamento, perché su Windows i
    # collegamenti simbolici richiedono privilegi e la giunzione non è la
    # stessa cosa: os.walk nella giunzione ci scende.
    bersaglio = (corpus / "dentro").resolve()

    class Collegamento:
        def is_symlink(self) -> bool:
            return True

        def resolve(self) -> Path:
            return bersaglio

    viste_prima = {radice_risolta}
    scendere, motivo = pv.cartella_da_scendere(Collegamento(), radice_risolta, viste_prima)
    verifica(
        "un collegamento a una cartella non si percorre, e lo dichiara",
        not scendere and motivo == "cartelle_collegate",
        "ottenuto ({}, {!r})".format(scendere, motivo),
    )
    verifica(
        "il collegamento non fa sparire la cartella vera a cui rimanda",
        pv.cartella_da_scendere(corpus / "dentro", radice_risolta, viste_prima) == (True, ""),
        "cartelle viste dopo il collegamento: {}".format(sorted(map(str, viste_prima))),
    )

    esclusioni = pv.Counter()
    letti = [percorso.name for percorso in pv.raccogli_file(corpus, esclusioni)]
    verifica(
        "senza collegamenti la scansione raccoglie tutto",
        letti == ["testo.txt"],
        "letti: {}".format(letti),
    )

    # Il ciclo vero, quando il sistema lo concede: una cartella che rimanda
    # alla propria antenata. Prima faceva morire il processo per ricorsione.
    ciclo = corpus / "dentro" / "giro"
    try:
        ciclo.symlink_to(corpus, target_is_directory=True)
    except (OSError, NotImplementedError) as errore:
        salta(
            "ciclo di collegamenti fra cartelle",
            "il sistema non permette di creare il collegamento ({})".format(
                type(errore).__name__
            ),
        )
        return
    esclusioni = pv.Counter()
    letti = [percorso.name for percorso in pv.raccogli_file(corpus, esclusioni)]
    verifica(
        "un ciclo di collegamenti non ferma la scansione né duplica i file",
        letti == ["testo.txt"],
        "letti: {}".format(letti),
    )


def prova_estensioni_maiuscole_raccolte(radice: Path) -> None:
    """Un file con estensione maiuscola entra nel corpus.

    Il difetto originale: il glob cercava `*.txt`, `*.md` e `*.markdown` in
    minuscolo. Su Windows non si vedeva, perché lì il confronto ignora le
    maiuscole; su Linux e macOS, dove gira anche la CI, un `appunti.TXT` o un
    `DIARIO.MD` restava fuori dal corpus e da ogni voce di esclusione, quindi
    il profilo misurava una parte del materiale senza dirlo.

    La prova guarda il criterio, non il glob del sistema: così vale su ogni
    filesystem, anche su quello che non distingue le maiuscole.
    """
    for nome, atteso in (
        ("appunti.txt", True),
        ("appunti.TXT", True),
        ("DIARIO.MD", True),
        ("note.Markdown", True),
        ("foglio.docx", False),
        ("archivio.txt.zip", False),
        ("senza-estensione", False),
    ):
        verifica(
            "estensione riconosciuta come attesa: {}".format(nome),
            nome.lower().endswith(pv.ESTENSIONI_DEL_CORPUS) is atteso,
            "atteso {}".format(atteso),
        )

    corpus = radice / "estensioni-maiuscole"
    corpus.mkdir()
    (corpus / "MAIUSCOLO.TXT").write_text(TESTO_ACCENTATO, encoding="utf-8")
    letti = [percorso.name for percorso in pv.raccogli_file(corpus)]
    verifica(
        "il file con estensione maiuscola viene raccolto",
        letti == ["MAIUSCOLO.TXT"],
        "letti: {}".format(letti),
    )


def prova_codifica_riconosciuta_dal_contrassegno(radice: Path) -> None:
    """La codifica dichiarata deve essere quella vera, e l'UTF-16 non esplode.

    Due difetti originali in `leggi_file`. Un file senza BOM veniva etichettato
    `utf-8-sig`, perché era il primo codec tentato e decodifica comunque. Un
    file UTF-16 con BOM, che `utf-8-sig` e `utf-8` rifiutano, scivolava su
    cp1252: i byte nulli spezzavano ogni parola, il conteggio si moltiplicava
    di oltre quattro volte e nessun avviso lo diceva.

    Il riconoscimento si fonda sul contrassegno iniziale, non sui byte nulli,
    per non prendere per UTF-16 un testo latino con molti spazi (ultimo caso).
    L'UTF-16 senza contrassegno resta fuori: riconoscerlo vorrebbe dire l'euristica
    dei byte nulli, che è proprio la causa dei falsi positivi.
    """
    frase = "Mario Montanari scrive bene, e la sua voce si sente subito."
    parole_attese = len(frase.replace(",", "").split())
    cp1252_testo = "Città e società, perché è così e non altro."

    casi = [
        ("utf-8 senza BOM", frase.encode("utf-8"), "utf-8", frase),
        ("utf-8 con BOM", b"\xef\xbb\xbf" + frase.encode("utf-8"), "utf-8-sig", frase),
        ("UTF-16 con BOM (LE)", frase.encode("utf-16"), "utf-16", frase),
        ("UTF-16 con BOM (BE)", b"\xfe\xff" + frase.encode("utf-16-be"), "utf-16", frase),
        ("UTF-32 con BOM (LE)", frase.encode("utf-32"), "utf-32", frase),
        ("UTF-32 con BOM (BE)", b"\x00\x00\xfe\xff" + frase.encode("utf-32-be"), "utf-32", frase),
        ("cp1252 vero", cp1252_testo.encode("cp1252"), "cp1252", cp1252_testo),
        ("latino con molti spazi", ("parola " * 20).encode("utf-8"), "utf-8", "parola " * 20),
    ]
    corpus = radice / "codifiche"
    corpus.mkdir()
    for etichetta, byte, codifica_attesa, contenuto_atteso in casi:
        percorso = corpus / (etichetta.replace(" ", "_") + ".txt")
        percorso.write_bytes(byte)
        contenuto, codifica = pv.leggi_file(percorso)
        verifica(
            "codifica giusta ({})".format(etichetta),
            codifica == codifica_attesa,
            "attesa {}, ottenuta {}".format(codifica_attesa, codifica),
        )
        verifica(
            "testo intatto ({})".format(etichetta),
            contenuto == contenuto_atteso,
            "primi 30: {!r}".format(contenuto[:30]),
        )

    # Il difetto che contava di più: le parole non si moltiplicano. Un solo
    # file UTF-16 in una cartella, il conteggio deve restare quello vero.
    solo16 = radice / "solo-utf16"
    solo16.mkdir()
    (solo16 / "testo.txt").write_bytes(frase.encode("utf-16"))
    parole = pv.calcola_profilo(solo16, "Prova")["corpus"]["parole_totali"]
    verifica(
        "un file UTF-16 non moltiplica le parole",
        parole == parole_attese,
        "attese {}, contate {}".format(parole_attese, parole),
    )

    # Un file che porta un contrassegno ma un contenuto rotto è corrotto: deve
    # sollevare ErroreCorpus, non un'altra eccezione che sfuggirebbe al
    # chiamante e fermerebbe tutto il corpus. È la stessa promessa del P0-1,
    # qui sul ramo dei contrassegni. Due casi: un BOM UTF-8 seguito da byte
    # non UTF-8, e un BOM UTF-16 con un numero dispari di byte.
    rotti = radice / "bom-rotti"
    rotti.mkdir()
    (rotti / "buono.txt").write_text(frase, encoding="utf-8")
    (rotti / "bom8-rotto.txt").write_bytes(b"\xef\xbb\xbf" + "caff\xe8".encode("cp1252"))
    (rotti / "bom16-dispari.txt").write_bytes(b"\xff\xfe" + b"\x41")
    for nome in ("bom8-rotto.txt", "bom16-dispari.txt"):
        try:
            pv.leggi_file(rotti / nome)
            esito = False
        except pv.ErroreCorpus:
            esito = True
        except Exception as errore:  # noqa: BLE001
            esito = False
            print("    (ha sollevato {} invece di ErroreCorpus)".format(type(errore).__name__))
        verifica("un contrassegno con contenuto rotto dà ErroreCorpus ({})".format(nome), esito)

    profilo = pv.calcola_profilo(rotti, "Prova")["corpus"]
    verifica(
        "un contrassegno rotto non ferma il corpus, il file buono resta contato",
        profilo["file_letti"] == 1 and profilo["parole_totali"] == parole_attese,
        "file letti {}, parole {}".format(profilo["file_letti"], profilo["parole_totali"]),
    )
    verifica(
        "i due file col contrassegno rotto stanno fra le esclusioni",
        profilo["esclusioni_in_pulizia"].get("file_illeggibili") == 2,
        "esclusioni: {}".format(profilo["esclusioni_in_pulizia"]),
    )


def prova_virgolette_chiuse_non_fondono_le_frasi(radice: Path) -> None:
    """Il punto dentro le virgolette chiude la frase, come quello fuori.

    Il difetto originale: quando il punto precedeva il segno di chiusura
    delle virgolette («basta.» oppure "basta."), il carattere subito dopo
    il terminatore non era uno spazio, e la frase non si chiudeva: si fondeva
    con la successiva. La convenzione italiana standard, col punto fuori
    dalle virgolette, funzionava già e non va rotta. Una minuscola dopo la
    chiusura resta continuazione, non nuova frase.

    La prova confronta la lista intera delle frasi, non solo quante sono:
    il segno di chiusura deve restare attaccato alla prima frase e la
    seconda deve cominciare pulita. Un controllo sul solo numero passerebbe
    anche con una virgoletta orfana in testa alla frase dopo.

    Ultima riga: un'abbreviazione o un'iniziale puntata dentro le virgolette
    curve non deve spezzare, come non spezza fra caporali o virgolette
    dritte. Senza coerenza fra i segni che chiudono la frase e i segni che
    si tolgono per riconoscere l'abbreviazione, «sig.» fra curve si spezzava
    e fra caporali no.
    """
    aperta = chr(171)      # caporale di apertura
    chiusa = chr(187)      # caporale di chiusura
    ap_curva = chr(8220)   # virgoletta curva di apertura
    ch_curva = chr(8221)   # virgoletta curva di chiusura
    casi = [
        ('Ho detto "basta." Poi sono uscito.',
         ['Ho detto "basta."', "Poi sono uscito."], "virgolette dritte, punto dentro"),
        ("Disse " + aperta + "basta." + chiusa + " Poi taceva.",
         ["Disse " + aperta + "basta." + chiusa, "Poi taceva."], "caporali, punto dentro"),
        ("Ho detto " + aperta + "basta" + chiusa + ". Poi sono uscito.",
         ["Ho detto " + aperta + "basta" + chiusa + ".", "Poi sono uscito."], "standard, punto fuori"),
        ("Prima frase. Seconda frase.",
         ["Prima frase.", "Seconda frase."], "senza virgolette"),
        ('Chiese "davvero?" e restò calmo.',
         ['Chiese "davvero?" e restò calmo.'], "minuscola dopo la chiusura: non chiude"),
        ("Conobbi il " + ap_curva + "sig." + ch_curva + " Rossi. Poi partì.",
         ["Conobbi il " + ap_curva + "sig." + ch_curva + " Rossi.", "Poi partì."],
         "abbreviazione dentro le virgolette curve: non spezza"),
    ]
    for testo, attese, nota in casi:
        ottenute = pv.dividi_in_frasi(testo)
        verifica(
            "frasi divise bene ({})".format(nota),
            ottenute == attese,
            "atteso {}, ottenuto {}".format(attese, ottenute),
        )


def prova_domande_fra_virgolette_contate(radice: Path) -> None:
    """Una domanda dentro le virgolette conta come domanda.

    Il difetto originale: `dividi_in_frasi` tiene dentro la frase il segno
    che chiude la citazione, quindi «Che ore sono?» finisce con il caporale.
    Le due quote cercavano il terminatore sull'ultimo carattere e non lo
    trovavano mai: su un corpus di dialoghi, dove le domande e le esclamazioni
    stanno quasi sempre fra caporali, `quota_interrogative` e
    `quota_esclamative` restavano a 0.0 senza che niente lo segnalasse.

    L'invariante provata qui: lo stesso testo con e senza virgolette deve
    dare le stesse due quote. Il confronto è fra due misure, non con un
    numero scritto a mano, così la prova regge anche se un giorno cambia il
    modo di dividere le frasi.
    """
    aperta = chr(171)
    chiusa = chr(187)
    ap_curva = chr(8220)
    ch_curva = chr(8221)

    # Il comportamento di `chiude_con` su tutti i rami, compresi quelli che
    # il fix apre: nessun segno di chiusura deve nascondere il terminatore, e
    # nessun terminatore deve comparire dove non c'era.
    casi = [
        ("Che ore sono?", "?", True, "punto interrogativo nudo"),
        (aperta + "Che ore sono?" + chiusa, "?", True, "fra caporali"),
        ('"Che ore sono?"', "?", True, "fra virgolette dritte"),
        (ap_curva + "Che ore sono?" + ch_curva, "?", True, "fra virgolette curve"),
        ("(Davvero?)", "?", True, "fra parentesi"),
        (aperta + "Vieni!" + chiusa, "!", True, "esclamativa fra caporali"),
        (aperta + "basta." + chiusa, "?", False, "punto dentro le virgolette"),
        (aperta + "basta." + chiusa, "!", False, "punto dentro, non esclamativa"),
        (aperta + "Ciao" + chiusa, "?", False, "senza terminatore"),
        ("Forse piove [?]", "?", False, "segno editoriale fra parentesi quadre"),
        ("Che sorpresa (!)", "!", False, "segno editoriale fra parentesi tonde"),
        ("E adesso (davvero?)", "?", True, "domanda vera dentro le parentesi"),
        ("Ho detto un po'", "?", False, "apostrofo finale, non un terminatore"),
        ("Puntini...", "?", False, "puntini di sospensione"),
        ("Che?!", "!", True, "interrogativa ed esclamativa insieme: vale l'ultimo"),
        ("Che?!", "?", False, "il punto interrogativo non è l'ultimo terminatore"),
        ("", "?", False, "frase vuota"),
    ]
    for frase, segno, atteso, nota in casi:
        verifica(
            "chiude_con riconosce il caso: {}".format(nota),
            pv.chiude_con(frase, segno) is atteso,
            "frase {!r}, segno {!r}, atteso {}".format(frase, segno, atteso),
        )

    def quote(nome: str, contenuto: str) -> tuple:
        corpus = radice / nome
        corpus.mkdir()
        (corpus / "testo.txt").write_text(contenuto + NL, encoding="utf-8")
        respiro = pv.calcola_profilo(corpus, "Prova")["respiro_della_frase"]
        return respiro["quota_interrogative"], respiro["quota_esclamative"]

    dialogo = (
        aperta + "Che ore sono?" + chiusa + " " + aperta + "Dove vai adesso?" + chiusa
        + " " + aperta + "Vieni subito qui!" + chiusa
        + " Le parole cadevano una dopo l'altra senza nessuna fretta."
    )
    nudo = (
        "Che ore sono? Dove vai adesso? Vieni subito qui!"
        + " Le parole cadevano una dopo l'altra senza nessuna fretta."
    )
    con_virgolette = quote("dialogo-virgolette", dialogo)
    senza_virgolette = quote("dialogo-nudo", nudo)
    verifica(
        "le virgolette non cambiano le quote di domanda ed esclamazione",
        con_virgolette == senza_virgolette,
        "con {} contro senza {}".format(con_virgolette, senza_virgolette),
    )
    verifica(
        "le quote misurate sono quelle attese, non zero",
        con_virgolette == (50.0, 25.0),
        "ottenuto {}".format(con_virgolette),
    )


def prova_dividi_frasi_non_e_quadratico(radice: Path) -> None:
    """Un paragrafo lungo senza a capo non deve costare in modo quadratico.

    Il difetto originale: `dividi_in_frasi` copiava a ogni terminatore tutto
    il testo prima del punto e tutto quello dopo, e il tempo cresceva col
    quadrato della lunghezza. Un blocco unico da due MB, un formato comune
    per il testo estratto da un PDF o incollato dal web, costava sedici
    secondi contro i tre di uno stesso testo diviso in paragrafi.

    La prova non fissa un tempo assoluto, che dipende dalla macchina: misura
    come il tempo scala. Su un blocco quattro volte più lungo un algoritmo
    lineare impiega circa quattro volte tanto, uno quadratico circa sedici.
    La soglia a otto sta nel mezzo, con margine da entrambi i lati.

    Il testo porta anche una citazione col punto dentro le virgolette, così
    il ramo che oltrepassa i segni di chiusura (la seconda metà del fix)
    finisce anch'esso nella misura, e non solo la scansione dei terminatori.
    """
    from time import perf_counter

    base = (
        "La qualità di un testo si misura anche dal respiro delle sue frasi. "
        "Chi scrive bene alterna periodi lunghi e periodi più brevi. "
        'Disse "basta." Poi riprese a scrivere piano. '
        "La punteggiatura non è un ornamento ma una guida per il lettore. "
    )
    piccolo = (base * (120_000 // len(base) + 1))[:120_000]
    grande = (base * (480_000 // len(base) + 1))[:480_000]

    def tempo(testo: str) -> float:
        misure = []
        for _ in range(3):
            avvio = perf_counter()
            pv.dividi_in_frasi(testo)
            misure.append(perf_counter() - avvio)
        return min(misure)

    t_piccolo = tempo(piccolo)
    t_grande = tempo(grande)
    rapporto = t_grande / t_piccolo if t_piccolo else float("inf")
    verifica(
        "il tempo di dividi_in_frasi scala lineare, non quadratico",
        rapporto < 8.0,
        "quattro volte il testo, tempo x{:.1f} (piccolo {:.3f}s, grande {:.3f}s)".format(
            rapporto, t_piccolo, t_grande
        ),
    )


def prova_elenchi_e_citazioni_non_perdono_prosa(radice: Path) -> None:
    """La continuazione di una voce e una citazione breve restano prosa.

    Il difetto originale: la ricomposizione delle righe chiudeva ogni voce di
    elenco, quindi la sua continuazione a capo restava orfana; sotto le
    quindici parole e senza punto finale finiva fra i `titoli_e_marcatori` e
    usciva da ogni conteggio. Lo stesso capitava a una citazione breve
    («> La tesi centrale»), che non aveva alcun trattamento e cadeva nella
    stessa regola. Sono due abitudini di scrittura Markdown molto diffuse, e
    la prosa dell'autore spariva in silenzio.

    L'invariante provata qui: mandare a capo una voce di elenco non deve
    cambiare quante parole si contano, e una citazione deve contare come la
    stessa frase senza marcatore. Il confronto è fra due misure, non con un
    numero scritto a mano.

    L'ultimo blocco è il caso di controllo che il fix non deve rompere: due
    voci distinte restano due, un titolo vero resta titolo.
    """

    def parole(nome: str, contenuto: str) -> int:
        corpus = radice / nome
        corpus.mkdir()
        (corpus / "testo.md").write_text(contenuto, encoding="utf-8")
        return pv.calcola_profilo(corpus, "Prova")["corpus"]["parole_totali"]

    coda = (
        NL + NL + "Un paragrafo pieno che chiude il file con il suo punto fermo." + NL
    )
    voce_intera = "- una voce di elenco lunga che prosegue senza punto finale"
    spezzata = "- una voce di elenco lunga" + NL + "che prosegue senza punto finale"
    verifica(
        "la continuazione di una voce di elenco conta come la voce intera",
        parole("elenco-spezzato", spezzata + coda)
        == parole("elenco-intero", voce_intera + coda),
        "spezzata {}, intera {}".format(
            parole("elenco-spezzato-bis", spezzata + coda),
            parole("elenco-intero-bis", voce_intera + coda),
        ),
    )

    citata = "> La tesi centrale del saggio"
    nuda = "La tesi centrale del saggio."
    verifica(
        "una citazione breve conta come prosa",
        parole("citazione-breve", citata + coda) == parole("citazione-nuda", nuda + coda),
        "citata {}, nuda {}".format(
            parole("citazione-breve-bis", citata + coda),
            parole("citazione-nuda-bis", nuda + coda),
        ),
    )

    # Il confronto è sulla lista intera, non sul solo numero di righe: un
    # controllo sui conteggi passerebbe anche con l'etichetta sbagliata o con
    # il marcatore rimasto dentro il testo.
    esclusioni = pv.Counter()
    testo = (
        "# Titolo vero" + NL
        + "- prima voce" + NL
        + "- seconda voce che prosegue" + NL
        + "sulla riga dopo" + NL
        + NL
        + "> citazione su due" + NL
        + "> righe di seguito" + NL
        + NL
        + "Un paragrafo pieno che chiude." + NL
    )
    atteso = [
        ("titolo", "# Titolo vero"),
        ("elenco", "prima voce"),
        ("elenco", "seconda voce che prosegue sulla riga dopo"),
        ("vuota", ""),
        ("prosa", "citazione su due righe di seguito"),
        ("vuota", ""),
        ("prosa", "Un paragrafo pieno che chiude."),
    ]
    ottenuto = pv.classifica_righe(testo, esclusioni)
    verifica(
        "elenchi, citazioni e titoli classificati uno per uno",
        ottenuto == atteso,
        "atteso {}, ottenuto {}".format(atteso, ottenuto),
    )
    verifica(
        "solo il titolo vero finisce fra i titoli esclusi",
        esclusioni["titoli_e_marcatori"] == 1,
        "contati {}".format(esclusioni["titoli_e_marcatori"]),
    )

    # I quattro rami che il fix ha aperto, trovati dall'affiancamento esterno.
    # Il primo: un paragrafo scritto sotto un elenco, senza riga bianca in
    # mezzo, veniva inghiottito dall'ultima voce e due frasi diventavano una.
    coppie = [
        (
            "La lista:" + NL + "- pane" + NL + "- latte" + NL + "Domani vado in banca.",
            [
                ("prosa", "La lista:"),
                ("elenco", "pane"),
                ("elenco", "latte"),
                ("prosa", "Domani vado in banca."),
            ],
            "il paragrafo sotto l'elenco resta un paragrafo",
        ),
        (
            "- una voce che prosegue" + NL + "sulla riga dopo",
            [("elenco", "una voce che prosegue sulla riga dopo")],
            "la continuazione in minuscolo resta unita alla voce",
        ),
        (
            "> Prima citazione." + NL + ">" + NL + "> Seconda citazione.",
            [
                ("prosa", "Prima citazione."),
                ("vuota", ""),
                ("prosa", "Seconda citazione."),
            ],
            "la riga di sola citazione separa i due paragrafi citati",
        ),
        (
            "> Il conte rispose" + NL + "con un sorriso amaro",
            [("prosa", "Il conte rispose con un sorriso amaro")],
            "la citazione si tira dietro la propria continuazione",
        ),
        (
            "- una voce che parla di" + NL + "Mario Montanari",
            [("elenco", "una voce che parla di"), ("prosa", "Mario Montanari")],
            "la riga dopo un elenco non diventa titolo, nemmeno se corta",
        ),
    ]
    for testo_caso, atteso_caso, nota in coppie:
        esclusioni_caso = pv.Counter()
        ottenuto_caso = pv.classifica_righe(testo_caso + NL, esclusioni_caso)
        verifica(
            "segmentazione: {}".format(nota),
            ottenuto_caso == atteso_caso,
            "atteso {}, ottenuto {}".format(atteso_caso, ottenuto_caso),
        )


def prova_dialogo_non_diventa_titolo(radice: Path) -> None:
    """Una battuta di dialogo isolata resta prosa e resta nei conteggi.

    Il difetto originale: la regola del titolo implicito guardava l'ultimo
    carattere letterale della riga. Una battuta di dialogo finisce con il
    segno che chiude la citazione, non con il punto interrogativo, quindi
    «Che ore sono?» risultava senza punteggiatura forte, entrava fra i
    `titoli_e_marcatori` e spariva dal profilo con le sue parole e la sua
    frase. Su un corpus di sola narrativa dialogata sparivano tutte le righe
    e lo strumento si fermava dichiarando che il corpus non conteneva prosa,
    che era falso.

    Il confronto è sulla lista intera delle righe classificate, non sul
    numero: con il solo conteggio la prova passerebbe anche con l'etichetta
    sbagliata. Gli ultimi due casi sono i rami che il fix apre: un titolo
    vero che finisce con un segno di chiusura deve restare titolo, e una riga
    fatta di soli segni di chiusura non deve far sollevare un errore di
    indice.
    """
    casi = [
        ("«Che ore sono?»", "prosa", "la domanda fra caporali"),
        ("«Vattene subito!»", "prosa", "l'esclamazione fra caporali"),
        ("«Non lo so davvero.»", "prosa", "l'affermazione fra caporali"),
        ('"Basta cosi!"', "prosa", "l'esclamazione fra virgolette dritte"),
        ("(Che ore sono?)", "prosa", "la domanda fra parentesi"),
        ("«Ecco come stanno le cose:»", "prosa", "i due punti fra caporali"),
        ("Il primo capitolo", "titolo", "un titolo vero senza terminatore"),
        ("Il caso (a)", "titolo", "un titolo che chiude con una parentesi"),
        ('Il capitolo "uno"', "titolo", "un titolo che chiude con le virgolette"),
        ("»", "titolo", "una riga di soli segni di chiusura"),
    ]
    for riga, atteso, nota in casi:
        esclusioni = pv.Counter()
        ottenuto = pv.classifica_righe(riga + NL, esclusioni)
        verifica(
            "dialogo e titoli: {}".format(nota),
            ottenuto == [(atteso, riga)],
            "atteso {}, ottenuto {}".format([(atteso, riga)], ottenuto),
        )

    # Il caso che faceva rifiutare l'intero corpus. Si passa dallo strumento
    # completo, non dalla sola classificazione, perché il difetto si vedeva
    # nel messaggio finale.
    corpus = radice / "narrativa-dialogata"
    corpus.mkdir()
    (corpus / "dialogo.txt").write_text(
        "«Che ore sono?»" + NL + NL
        + "«Non lo so davvero.»" + NL + NL
        + "«Vattene subito!»" + NL,
        encoding="utf-8",
    )
    try:
        profilo = pv.calcola_profilo(corpus, "Prova")
        rifiutato = ""
    except pv.ErroreCorpus as errore:
        profilo = None
        rifiutato = str(errore)
    verifica(
        "un corpus di sola narrativa dialogata non viene rifiutato",
        profilo is not None,
        rifiutato or "profilo prodotto",
    )
    if profilo is not None:
        verifica(
            "le tre battute contano come tre frasi",
            profilo["corpus"]["frasi_totali"] == 3,
            "frasi contate: {}".format(profilo["corpus"]["frasi_totali"]),
        )
        esclusi = profilo["corpus"]["esclusioni_in_pulizia"].get("titoli_e_marcatori", 0)
        verifica(
            "nessuna battuta finisce fra i titoli esclusi",
            esclusi == 0,
            "titoli esclusi: {}".format(esclusi),
        )


def prova_separatore_di_citazione_non_cambia_la_classificazione(radice: Path) -> None:
    """Lo stesso documento si classifica allo stesso modo con i due separatori.

    Il difetto originale: la riga fatta di soli marcatori di citazione («> >»)
    diventa una riga vuota, ma il tipo della riga precedente non veniva
    azzerato. La riga successiva restava quindi trattata come la
    continuazione di un elenco, cioè esentata dalla regola del titolo
    implicito, e un titolo di sezione veniva contato come prosa. Con la riga
    bianca al posto dello stesso separatore il risultato era diverso, e la
    differenza non aveva alcun segno esteriore nella scheda.
    """
    coda = "Titolo di sezione"
    atteso = [("elenco", "voce unica."), ("vuota", ""), ("titolo", coda)]
    for separatore, nota in ((">" + " " + ">", "il separatore di citazione"), ("", "la riga bianca")):
        testo = "- voce unica." + NL + separatore + NL + coda + NL
        ottenuto = pv.classifica_righe(testo, pv.Counter())
        verifica(
            "con {} il titolo resta titolo".format(nota),
            ottenuto == atteso,
            "atteso {}, ottenuto {}".format(atteso, ottenuto),
        )


def prova_elenco_non_ingoia_il_paragrafo_nuovo(radice: Path) -> None:
    """Una voce di elenco non si tira dietro il paragrafo che comincia dopo.

    Il difetto originale, una regressione aperta dalla correzione che salvava
    le continuazioni: il criterio dichiarato era «la continuazione comincia in
    minuscolo», ma il codice verificava soltanto che la riga non cominciasse
    con una maiuscola. Una riga che apre con una cifra, una parentesi o un
    caporale non è né maiuscola né minuscola, quindi passava per continuazione
    e il paragrafo nuovo finiva dentro la voce di elenco.

    Nella stessa funzione, il ramo gemello: la riga che chiude con una battuta
    di dialogo non risultava chiusa, perché il confronto guardava l'ultimo
    carattere letterale, e due paragrafi distinti diventavano un blocco solo.

    Il confronto è sulla lista intera prodotta da
    `unisci_righe_dello_stesso_blocco`, non su un conteggio.
    """
    casi = [
        (
            ["- ho cambiato casa tre volte, l'ultima nel", "2023. L'anno della svolta."],
            ["- ho cambiato casa tre volte, l'ultima nel", "2023. L'anno della svolta."],
            "la cifra seguita da maiuscola apre un paragrafo nuovo",
        ),
        (
            ["- una voce qualsiasi", "«Che ore sono?» chiese Maria."],
            ["- una voce qualsiasi", "«Che ore sono?» chiese Maria."],
            "il caporale seguito da maiuscola apre un paragrafo nuovo",
        ),
        (
            ["- una voce qualsiasi", '"Basta" disse lui senza alzare gli occhi.'],
            ["- una voce qualsiasi", '"Basta" disse lui senza alzare gli occhi.'],
            "la virgoletta dritta seguita da maiuscola apre un paragrafo nuovo",
        ),
        (
            ["> una citazione qualsiasi", "«Che ore sono?» chiese Maria."],
            ["> una citazione qualsiasi", "«Che ore sono?» chiese Maria."],
            "la stessa regola vale per la citazione",
        ),
        (
            ["- comprare il pane", "(e magari anche il latte)."],
            ["- comprare il pane (e magari anche il latte)."],
            "la parentesi seguita da minuscola resta continuazione",
        ),
        (
            ["- una voce spezzata a meta dal", "ritorno a capo."],
            ["- una voce spezzata a meta dal ritorno a capo."],
            "la continuazione in minuscolo resta unita",
        ),
        (
            ["- il totale delle spese e di", "2023"],
            ["- il totale delle spese e di 2023"],
            "una riga senza lettere resta continuazione",
        ),
        (
            [
                "Maria chiese: «Che ore sono?»",
                "La casa restava in silenzio per tutto il pomeriggio.",
            ],
            [
                "Maria chiese: «Che ore sono?»",
                "La casa restava in silenzio per tutto il pomeriggio.",
            ],
            "due paragrafi chiusi da una battuta restano due",
        ),
        (
            [
                "Maria chiese: «Che ore sono?»",
                "Lui rispose: «Non lo so!»",
                "Il silenzio tornava a riempire la stanza.",
            ],
            [
                "Maria chiese: «Che ore sono?»",
                "Lui rispose: «Non lo so!»",
                "Il silenzio tornava a riempire la stanza.",
            ],
            "tre paragrafi di seguito restano tre",
        ),
        (
            ["una riga spezzata dalla", "larghezza fissa del file."],
            ["una riga spezzata dalla larghezza fissa del file."],
            "la prosa spezzata dall'impaginazione si ricompone",
        ),
        (
            ["»", "Il seguito del testo."],
            ["» Il seguito del testo."],
            "una riga di soli segni di chiusura non solleva un errore",
        ),
    ]
    for righe, atteso, nota in casi:
        ottenuto = pv.unisci_righe_dello_stesso_blocco(righe)
        verifica(
            "unione dei blocchi: {}".format(nota),
            ottenuto == atteso,
            "atteso {}, ottenuto {}".format(atteso, ottenuto),
        )


def prova_dividi_frasi_lineare_con_spazi_unicode(radice: Path) -> None:
    """La divisione in frasi resta lineare anche senza spazi ASCII.

    Il difetto originale: la scansione a ritroso che cerca l'inizio della
    parola prima di un punto si fermava sul solo spazio ASCII. Un testo che
    usa lo spazio sottile, quello stretto o quello ideografico, forme che
    arrivano da certi programmi di scrittura e dalla tipografia francese e
    asiatica, non ne offriva nessuno: la scansione tornava fino all'inizio del
    testo a ogni punto e il tempo cresceva col quadrato. Su 144 KB con spazio
    sottile la misura era di quattordici secondi e mezzo.

    Come la prova gemella, non si fissa un tempo assoluto ma si guarda come
    scala: raddoppiando il testo, un algoritmo lineare raddoppia il tempo, uno
    quadratico lo quadruplica. La soglia a tre sta nel mezzo.

    Gli ultimi due controlli sono il ramo che il fix apre: fermandosi anche
    sugli spazi tipografici, le abbreviazioni e le iniziali puntate che stanno
    dopo uno di quegli spazi vengono finalmente riconosciute, e non spezzano
    più la frase.
    """
    from time import perf_counter

    spazi = [
        ("sottile", chr(8201)),
        ("stretto", chr(8239)),
        ("ideografico", chr(12288)),
        ("unificatore", chr(160)),
    ]
    for nome, spazio in spazi:
        def testo_con(periodi: int, spazio: str = spazio) -> str:
            return spazio.join(
                "Questa{0}e{0}una{0}frase{0}di{0}prova{0}numero{1}.".format(spazio, indice)
                for indice in range(periodi)
            )

        def tempo(testo: str) -> float:
            misure = []
            for _ in range(3):
                avvio = perf_counter()
                pv.dividi_in_frasi(testo)
                misure.append(perf_counter() - avvio)
            return min(misure)

        t_piccolo = tempo(testo_con(400))
        t_grande = tempo(testo_con(800))
        rapporto = t_grande / t_piccolo if t_piccolo else float("inf")
        verifica(
            "lo spazio {} non rende quadratica la divisione in frasi".format(nome),
            rapporto < 3.0,
            "il doppio del testo, tempo x{:.1f} ({:.4f}s e {:.4f}s)".format(
                rapporto, t_piccolo, t_grande
            ),
        )

    sottile = chr(8201)
    frase = "Parlava{0}con{0}il{0}sig.{0}Rossi{0}di{0}persona.".format(sottile)
    verifica(
        "un'abbreviazione dopo uno spazio sottile non spezza la frase",
        pv.dividi_in_frasi(frase) == [frase],
        "ottenuto {}".format(pv.dividi_in_frasi(frase)),
    )
    iniziale = "Lo{0}scrisse{0}F.{0}Rossi{0}in{0}persona.".format(sottile)
    verifica(
        "un'iniziale puntata dopo uno spazio sottile non spezza la frase",
        pv.dividi_in_frasi(iniziale) == [iniziale],
        "ottenuto {}".format(pv.dividi_in_frasi(iniziale)),
    )


def prova_spoglia_segni_di_chiusura_non_e_quadratica(radice: Path) -> None:
    """Togliere i segni di chiusura costa in proporzione a quanti sono.

    Il difetto originale, segnalato dall'affiancamento esterno: la funzione
    affettava la stringa a ogni giro, quindi la ricopiava per intero per ogni
    segno tolto. L'impatto misurato era piccolo (sei centesimi di secondo su
    ottantamila segni), ma la funzione è passata da un uso solo a tre, uno dei
    quali per ogni riga del corpus, e il costo andava tolto prima di
    moltiplicarlo.

    Anche qui si guarda come scala, non un tempo assoluto.
    """
    from time import perf_counter

    def tempo(quanti: int) -> float:
        testo = "a" + chr(187) * quanti
        misure = []
        for _ in range(3):
            avvio = perf_counter()
            pv.spoglia_segni_di_chiusura(testo)
            misure.append(perf_counter() - avvio)
        return min(misure)

    t_piccolo = tempo(40_000)
    t_grande = tempo(160_000)
    rapporto = t_grande / t_piccolo if t_piccolo else float("inf")
    verifica(
        "spoglia_segni_di_chiusura scala lineare, non quadratica",
        rapporto < 8.0,
        "quattro volte i segni, tempo x{:.1f} ({:.4f}s e {:.4f}s)".format(
            rapporto, t_piccolo, t_grande
        ),
    )
    verifica(
        "la funzione condivisa non tocca il terminatore",
        pv.spoglia_segni_di_chiusura("«Che ore sono?»") == "«Che ore sono?",
        "ottenuto {!r}".format(pv.spoglia_segni_di_chiusura("«Che ore sono?»")),
    )
    verifica(
        "una riga di soli segni di chiusura si svuota senza errori",
        pv.spoglia_segni_di_chiusura("»»» ") == "",
        "ottenuto {!r}".format(pv.spoglia_segni_di_chiusura("»»» ")),
    )


def prova_unisci_righe_non_e_superlineare(radice: Path) -> None:
    """Un blocco senza terminatori non deve costare più che al quadrato.

    Il difetto originale: la ricomposizione costruiva la riga corrente con
    `corrente + " " + riga` dentro il ciclo, quindi ricopiava per intero una
    stringa che cresceva a ogni passo. Su un blocco che non incontra mai un
    terminatore di frase (una trascrizione senza punti, un elenco incollato
    senza trattini) raddoppiare le righe da 80.000 a 160.000 moltiplicava il
    tempo per sette, non per due, su un corpus di poche centinaia di
    kilobyte che l'avviso sui venti megabyte non segnala.

    Come la prova gemella su `dividi_in_frasi`, qui non si fissa un tempo
    assoluto ma si misura come scala: quattro volte le righe, meno di otto
    volte il tempo.
    """
    from time import perf_counter

    riga = "una riga senza terminatore di frase che continua"

    def tempo(quante: int) -> float:
        righe = [riga] * quante
        misure = []
        for _ in range(3):
            avvio = perf_counter()
            pv.unisci_righe_dello_stesso_blocco(righe)
            misure.append(perf_counter() - avvio)
        return min(misure)

    t_piccolo = tempo(20_000)
    t_grande = tempo(80_000)
    rapporto = t_grande / t_piccolo if t_piccolo else float("inf")
    verifica(
        "il tempo di unisci_righe scala lineare, non più che al quadrato",
        rapporto < 8.0,
        "quattro volte le righe, tempo x{:.1f} (piccolo {:.3f}s, grande {:.3f}s)".format(
            rapporto, t_piccolo, t_grande
        ),
    )


def prova_sovrascrittura_solo_con_firma(radice: Path) -> None:
    """Lo strumento non sovrascrive un file che non ha scritto lui.

    Il difetto originale: senza --out l'uscita finisce accanto ai testi, e un
    file dell'utente chiamato «scheda-voce.md» spariva al primo lancio. Ora lo
    strumento riscrive solo i file che portano la sua firma in testa, e si
    ferma con codice tre davanti a quelli che non riconosce.
    """
    # Un file dell'utente, senza firma, con lo stesso nome di un'uscita.
    corpus = radice / "sovrascrittura"
    corpus.mkdir()
    (corpus / "testo.txt").write_text(TESTO_ACCENTATO, encoding="utf-8")
    appunto = "Il mio appunto, da non perdere." + NL
    mio = corpus / "scheda-voce.md"
    mio.write_text(appunto, encoding="utf-8")
    codice = pv.main([str(corpus), "--nome", "Prova"])
    verifica(
        "un file senza firma non viene sovrascritto (codice tre)",
        codice == 3,
        "codice di uscita: {}".format(codice),
    )
    verifica(
        "il file dell'utente resta intatto",
        mio.read_text(encoding="utf-8") == appunto,
    )
    verifica(
        "senza firma non si scrive nulla, nemmeno il json",
        not (corpus / "profilo-voce.json").exists(),
    )

    # In una cartella pulita scrive, e il secondo lancio, trovando la propria
    # firma, sovrascrive senza fermarsi.
    pulita = radice / "sovra-pulita"
    pulita.mkdir()
    (pulita / "testo.txt").write_text(TESTO_ACCENTATO, encoding="utf-8")
    primo = pv.main([str(pulita), "--nome", "Uno"])
    secondo = pv.main([str(pulita), "--nome", "Due"])
    scheda = (pulita / "scheda-voce.md").read_text(encoding="utf-8")
    verifica(
        "in una cartella pulita scrive, e il rilancio sovrascrive i propri file",
        primo == 0 and secondo == 0 and "Due" in scheda,
        "primo: {}, secondo: {}".format(primo, secondo),
    )
    verifica(
        "la firma sta nella prima riga della scheda",
        scheda.splitlines()[0] == "<!-- {} -->".format(pv.FIRMA),
    )
    dati = json.loads((pulita / "profilo-voce.json").read_text(encoding="utf-8"))
    verifica(
        "la firma è la prima chiave del json",
        list(dati.keys())[0] == "_firma" and dati["_firma"] == pv.FIRMA,
    )

    # Caso misto: la scheda ha la firma, il json è dell'utente. Basta un file
    # non riconosciuto per fermare tutto, e la scheda pur firmata non va toccata.
    misto = radice / "sovra-misto"
    misto.mkdir()
    (misto / "testo.txt").write_text(TESTO_ACCENTATO, encoding="utf-8")
    (misto / "scheda-voce.md").write_text(scheda, encoding="utf-8")
    (misto / "profilo-voce.json").write_text("{}" + NL, encoding="utf-8")
    codice = pv.main([str(misto), "--nome", "Tre"])
    verifica(
        "basta un file non riconosciuto per fermare tutto (codice tre)",
        codice == 3,
        "codice di uscita: {}".format(codice),
    )
    verifica(
        "nel caso misto la scheda con firma non viene toccata",
        "Due" in (misto / "scheda-voce.md").read_text(encoding="utf-8"),
    )


def prova_firma_riconosciuta_solo_in_testa(radice: Path) -> None:
    """La firma vale solo in testa, non citata più in basso.

    Il difetto trovato in affiancamento: il controllo cercava la firma come
    sottostringa nei primi caratteri, così un documento dell'utente che la
    citava (un appunto che incolla l'intestazione di una scheda vera) veniva
    preso per una nostra uscita e sovrascritto, senza avviso. Ora la firma
    conta solo se è la prima riga della scheda o la prima chiave del JSON.
    """
    # Scheda dell'utente che cita la firma alla terza riga.
    corpus = radice / "firma-in-mezzo"
    corpus.mkdir()
    (corpus / "testo.txt").write_text(TESTO_ACCENTATO, encoding="utf-8")
    scheda_utente = (
        "I miei appunti." + NL
        + "Intestazione copiata da una scheda vera:" + NL
        + "<!-- {} -->".format(pv.FIRMA) + NL
    )
    (corpus / "scheda-voce.md").write_text(scheda_utente, encoding="utf-8")
    codice = pv.main([str(corpus), "--nome", "Prova"])
    verifica(
        "la firma citata in mezzo alla scheda non basta a sovrascriverla",
        codice == 3,
        "codice di uscita: {}".format(codice),
    )
    verifica(
        "la scheda dell'utente con la firma in mezzo resta intatta",
        (corpus / "scheda-voce.md").read_text(encoding="utf-8") == scheda_utente,
    )

    # JSON dell'utente che cita la firma come valore, non come prima chiave.
    corpus2 = radice / "firma-json-non-prima"
    corpus2.mkdir()
    (corpus2 / "testo.txt").write_text(TESTO_ACCENTATO, encoding="utf-8")
    json_utente = '{{"mio": "dato", "nota": "{}"}}'.format(pv.FIRMA) + NL
    (corpus2 / "profilo-voce.json").write_text(json_utente, encoding="utf-8")
    codice = pv.main([str(corpus2), "--nome", "Prova"])
    verifica(
        "la firma non come prima chiave del json non basta",
        codice == 3,
        "codice di uscita: {}".format(codice),
    )
    verifica(
        "il json dell'utente con la firma come valore resta intatto",
        (corpus2 / "profilo-voce.json").read_text(encoding="utf-8") == json_utente,
    )


def prova_elisioni_staccate(radice: Path) -> None:
    """Anche le elisioni con testa lunga si staccano per il conteggio.

    Il difetto: forma_lessicale staccava «l'arte» ma non «dell'arte», perché si
    fermava alle teste di tre lettere. Così «arte» e «dell'arte» contavano come
    due parole diverse e la varietà lessicale usciva gonfiata.
    """
    coppie = [
        ("l'arte", "arte"),
        ("dell'arte", "arte"),
        ("nell'anno", "anno"),
        ("sull'onda", "onda"),
        ("dall'alto", "alto"),
        ("quell'uomo", "uomo"),
        ("quest'anno", "anno"),
        ("senz'altro", "altro"),
        ("mezz'ora", "ora"),
        ("un'idea", "idea"),
        ("all'aperto", "aperto"),
        ("gl'italiani", "italiani"),
        ("anch'io", "io"),
        ("nessun'altra", "altra"),
        ("quant'altro", "altro"),
    ]
    for forma, attesa in coppie:
        ottenuta = pv.forma_lessicale(forma)
        verifica(
            "elisione staccata: {} -> {}".format(forma, attesa),
            ottenuta == attesa,
            "ottenuta: {}".format(ottenuta),
        )
    # Il troncamento (coda vuota) non è un'elisione e tiene il proprio
    # apostrofo: «un po» senza apostrofo è una forma che l'italiano non
    # ammette, e la scheda la mostrava fra le sequenze ricorrenti.
    for tronca in ("po'", "va'", "da'", "fa'", "di'", "sta'", "Po'"):
        atteso = tronca.lower()
        verifica(
            "il troncamento tiene l'apostrofo: {} -> {}".format(tronca, atteso),
            pv.forma_lessicale(tronca) == atteso,
            "ottenuta: {}".format(pv.forma_lessicale(tronca)),
        )
    # Un cognome ha la coda maiuscola e resta intero, senza confondersi con un
    # nome comune: «Dell'Orso» non deve diventare «orso».
    verifica(
        "un cognome non si spezza: Dell'Orso",
        pv.forma_lessicale("Dell'Orso") == "dell'orso",
        "ottenuta: {}".format(pv.forma_lessicale("Dell'Orso")),
    )
    # Un anno eliso ha la coda non alfabetica e non diventa un numero puro.
    verifica(
        "un anno eliso non diventa numero: dell'800",
        pv.forma_lessicale("dell'800") == "dell'800",
        "ottenuta: {}".format(pv.forma_lessicale("dell'800")),
    )
    # L'apostrofo tipografico curvo va trattato come quello dritto.
    verifica(
        "l'apostrofo curvo si stacca come il dritto",
        pv.forma_lessicale("dell’arte") == "arte",
        "ottenuta: {}".format(pv.forma_lessicale("dell’arte")),
    )


def prova_ttr_grezzo_fuori_dal_posizionamento(radice: Path) -> None:
    """Sotto le mille parole il TTR esce dalla tabella di posizionamento.

    Il difetto trovato in affiancamento: per un corpus corto il TTR a finestra
    ripiega sul rapporto grezzo, che dipende dalla lunghezza; collocarlo
    rispetto all'intervallo umano dava un giudizio senza senso, e annotarlo
    soltanto lasciava nel campo «posizione» quel giudizio contraddetto dalla
    cautela accanto. Ora sotto soglia il TTR viene tolto dal posizionamento, e
    la scheda lo dichiara. La soglia è <=, perché a mille parole esatte la
    finestra mobile coincide col rapporto grezzo.
    """

    def voce_ttr(profilo):
        # «Varietà lessicale» individua solo il TTR: cercare «mille parole»
        # prenderebbe anche «Trattini lunghi ogni mille parole».
        for voce in profilo["posizione_rispetto_ai_riferimenti"]:
            if "Varietà lessicale" in voce["misura"]:
                return voce
        return None

    corto = radice / "ttr-corto"
    corto.mkdir()
    (corto / "testo.txt").write_text(TESTO_ACCENTATO * 5, encoding="utf-8")
    profilo_corto = pv.calcola_profilo(corto, "Prova")
    verifica(
        "il corpus corto di prova sta sotto le mille parole",
        profilo_corto["corpus"]["parole_totali"] < pv.FINESTRA_TTR_CONFRONTO,
        "parole: {}".format(profilo_corto["corpus"]["parole_totali"]),
    )
    verifica(
        "sotto soglia il TTR non compare nel posizionamento",
        voce_ttr(profilo_corto) is None,
    )
    scheda_corto = pv.scrivi_scheda(profilo_corto)
    verifica(
        "sotto soglia la scheda dichiara che il TTR è escluso",
        "non compare in questa tabella" in scheda_corto,
    )

    lungo = radice / "ttr-lungo"
    lungo.mkdir()
    (lungo / "testo.txt").write_text(TESTO_ACCENTATO * 40, encoding="utf-8")
    profilo_lungo = pv.calcola_profilo(lungo, "Prova")
    verifica(
        "il corpus lungo di prova supera le mille parole",
        profilo_lungo["corpus"]["parole_totali"] > pv.FINESTRA_TTR_CONFRONTO,
        "parole: {}".format(profilo_lungo["corpus"]["parole_totali"]),
    )
    verifica(
        "sopra soglia il TTR compare nel posizionamento",
        voce_ttr(profilo_lungo) is not None,
    )


def prova_anno_a_inizio_riga_non_e_elenco(radice: Path) -> None:
    """Un anno a inizio riga è prosa, non una voce di elenco.

    Il difetto: «2023. Anno di svolta...» finiva classificato come elenco per
    via del pattern numero-punto, e con esso la sua prosa spariva dal respiro
    della frase. Un elenco vero, numerato piccolo, deve invece restare elenco.
    """
    esc: pv.Counter = pv.Counter()
    anno = pv.classifica_righe("2023. Anno di svolta per il settore.", esc)
    verifica(
        "un anno a inizio riga è prosa",
        anno == [("prosa", "2023. Anno di svolta per il settore.")],
        "ottenuto: {}".format(anno),
    )
    for voce, atteso in (
        ("1. Primo punto.", "Primo punto."),
        ("12. Dodicesimo punto.", "Dodicesimo punto."),
        ("999. Ultima voce piccola.", "Ultima voce piccola."),
        ("- Trattino.", "Trattino."),
    ):
        esc = pv.Counter()
        righe = pv.classifica_righe(voce, esc)
        verifica(
            "un elenco vero resta elenco: {}".format(voce),
            righe == [("elenco", atteso)],
            "ottenuto: {}".format(righe),
        )
    # Il confine della regola: da mille in su è prosa (un anno, un numero
    # grande), non elenco. E una riga di migliaia di cifre non deve far
    # crashare la conversione a intero (il limite di Python 3.12).
    for riga_prosa in (
        "1000. Mille esatto, non una voce di elenco.",
        "2023. Anno di svolta per il settore.",
        "9" * 5000 + ". Riga con troppe cifre per un intero.",
    ):
        esc = pv.Counter()
        tipi = [tipo for tipo, _ in pv.classifica_righe(riga_prosa, esc)]
        verifica(
            "da mille in su non è elenco: {}".format(riga_prosa[:24]),
            "elenco" not in tipi,
            "tipi: {}".format(tipi),
        )


def prova_frontmatter_riconosciuto(radice: Path) -> None:
    """Il frontmatter resta fuori dai conteggi anche con riga vuota iniziale
    o chiusura con tre punti.

    Il difetto: un delimitatore preceduto da una riga vuota non apriva il
    blocco, e i metadati finivano nei conteggi; un blocco chiuso con «...» non
    si chiudeva mai e faceva sparire in silenzio tutta la prosa che seguiva.
    """
    corpo = "Prosa vera del corpo, con la sua parola rara zqxwv scritta dentro."
    spia = "parolametadatiraraxyz"

    base = radice / "fm-baseline"
    base.mkdir()
    (base / "testo.md").write_text(corpo + NL, encoding="utf-8")
    atteso = pv.calcola_profilo(base, "Prova")["corpus"]["parole_totali"]

    casi = [
        (
            "riga-vuota-iniziale",
            NL + "---" + NL + "title: Prova" + NL
            + "description: " + spia + " e poi molte altre parole in fila per "
            + "superare la soglia del titolo di quindici parole piena zeppa" + NL
            + "---" + NL + corpo + NL,
        ),
        (
            "chiusura-tre-punti",
            "---" + NL + "title: Prova con " + spia + NL + "..." + NL + corpo + NL,
        ),
        (
            "frontmatter-normale-non-regressione",
            "---" + NL + "title: Prova con " + spia + NL + "---" + NL + corpo + NL,
        ),
    ]
    for nome, testo in casi:
        corpus = radice / ("fm-" + nome)
        corpus.mkdir()
        (corpus / "testo.md").write_text(testo, encoding="utf-8")
        profilo = pv.calcola_profilo(corpus, "Prova")
        scheda = pv.scrivi_scheda(profilo)
        verifica(
            "{}: i metadati restano fuori dai conteggi".format(nome),
            profilo["corpus"]["parole_totali"] == atteso,
            "attese {}, contate {}".format(
                atteso, profilo["corpus"]["parole_totali"]
            ),
        )
        verifica(
            "{}: la spia dei metadati non entra nella scheda".format(nome),
            spia not in scheda,
        )
        verifica(
            "{}: il corpo invece è contato".format(nome),
            "zqxwv" in scheda,
        )


def prova_frontmatter_non_chiuso_non_perde_la_prosa(radice: Path) -> None:
    """Un delimitatore --- decorativo, mai chiuso, non fa sparire la prosa.

    Il difetto, trovato in affiancamento: dopo il riconoscimento del frontmatter
    dietro una riga vuota, un file che si apre con una riga vuota e un --- usato
    come separatore, senza un secondo --- né un «...», vedeva tutta la prosa
    seguente presa per metadati e sparire dai conteggi. Un blocco che non si
    chiude non era frontmatter, e ora le sue righe tornano contenuto.
    """
    corpo = "Questa e prosa vera con parole sue, zqxwv compresa, e non metadati."
    base = radice / "nc-base"
    base.mkdir()
    (base / "t.txt").write_text(corpo + NL, encoding="utf-8")
    atteso = pv.calcola_profilo(base, "Prova")["corpus"]["parole_totali"]

    aperto = radice / "nc-aperto"
    aperto.mkdir()
    (aperto / "t.md").write_text(NL + "---" + NL + corpo + NL, encoding="utf-8")
    profilo = pv.calcola_profilo(aperto, "Prova")
    scheda = pv.scrivi_scheda(profilo)
    verifica(
        "un --- decorativo mai chiuso non fa sparire la prosa",
        profilo["corpus"]["parole_totali"] == atteso,
        "attese {}, contate {}".format(
            atteso, profilo["corpus"]["parole_totali"]
        ),
    )
    verifica(
        "la parola-spia della prosa è nella scheda",
        "zqxwv" in scheda,
    )


def prova_righe_vuote_finali_conservate(radice: Path) -> None:
    """Solo l'ultimo ritorno a capo si toglie, non ogni riga vuota finale.

    Il difetto: rstrip azzerava in blocco tutte le righe vuote finali, non
    solo l'a capo che ogni editor lascia. Le righe vuote volute in fondo
    sparivano dal conteggio che decide come il file separa i paragrafi.
    """
    esc: pv.Counter = pv.Counter()
    tante = pv.classifica_righe("Prosa piena." + NL + NL + NL, esc)
    verifica(
        "restano le righe vuote finali oltre l'ultimo a capo",
        tante == [("prosa", "Prosa piena."), ("vuota", ""), ("vuota", "")],
        "ottenute: {}".format(tante),
    )
    esc = pv.Counter()
    una = pv.classifica_righe("Prosa piena." + NL, esc)
    verifica(
        "l'unico a capo finale non lascia una riga vuota",
        una == [("prosa", "Prosa piena.")],
        "ottenute: {}".format(una),
    )


def prova_frasi_vuote_non_gonfiano_il_gulpease(radice: Path) -> None:
    """Righe di sola punteggiatura non contano come frasi.

    Il difetto: una riga fatta di soli puntini o punti esclamativi diventava
    una frase senza parole, esclusa dalla media delle lunghezze ma non dal
    numero totale di frasi, e così gonfiava il Gulpease, che al numeratore
    usa proprio il numero di frasi.
    """
    prosa = (
        "La qualità di un testo si misura dal respiro delle sue frasi vere. "
        "Chi scrive alterna periodi lunghi e periodi brevi con equilibrio. "
        "La punteggiatura guida il lettore senza mai gridare troppo forte. "
    ) * 5

    def profilo_di(nome: str, testo: str):
        corpus = radice / nome
        corpus.mkdir()
        (corpus / "testo.txt").write_text(testo, encoding="utf-8")
        return pv.calcola_profilo(corpus, "Prova")

    pulito = profilo_di("gulp-pulito", prosa + NL)
    punti = NL.join(["..."] * 8)  # otto righe di soli puntini
    sporco = profilo_di("gulp-sporco", prosa + NL + punti + NL)
    verifica(
        "le righe di soli puntini non cambiano il numero di frasi",
        sporco["corpus"]["frasi_totali"] == pulito["corpus"]["frasi_totali"],
        "pulito {}, sporco {}".format(
            pulito["corpus"]["frasi_totali"], sporco["corpus"]["frasi_totali"]
        ),
    )
    verifica(
        "le righe di soli puntini non gonfiano il Gulpease",
        sporco["leggibilita"]["gulpease_corpus"]
        == pulito["leggibilita"]["gulpease_corpus"],
        "pulito {}, sporco {}".format(
            pulito["leggibilita"]["gulpease_corpus"],
            sporco["leggibilita"]["gulpease_corpus"],
        ),
    )
    verifica(
        "la distribuzione delle lunghezze di frase resta identica",
        sporco["respiro_della_frase"]["distribuzione_per_fasce"]
        == pulito["respiro_della_frase"]["distribuzione_per_fasce"],
        "pulito {}, sporco {}".format(
            pulito["respiro_della_frase"]["distribuzione_per_fasce"],
            sporco["respiro_della_frase"]["distribuzione_per_fasce"],
        ),
    )


def prova_connettivi_non_fra_le_parole_piene(radice: Path) -> None:
    """Un connettivo non compare due volte, fra i connettivi e fra le piene.

    Il difetto: il filtro delle parole piene escludeva solo le parole vuote,
    non i connettivi, quindi le forme meno comuni («benché», «laddove»)
    finivano in entrambe le liste della scheda.
    """
    corpus = radice / "connettivi-doppi"
    corpus.mkdir()
    testo = (
        "Benche il tema sia arduo, sebbene manchi il tempo, affinche tutto "
        "torni, laddove serve, benche sia tardi, sebbene stanchi, affinche "
        "regga, laddove conviene, benche costi, sebbene pesi." + NL
    ) * 3
    (corpus / "testo.txt").write_text(testo, encoding="utf-8")
    ricorrenze = pv.calcola_profilo(corpus, "Prova")["ricorrenze"]
    connettivi = {forma for forma, _ in ricorrenze["connettivi_frequenti"]}
    piene = {forma for forma, _ in ricorrenze["parole_piene_frequenti"]}
    verifica(
        "i connettivi ricorrono nella loro lista",
        {"benche", "sebbene", "affinche", "laddove"} <= connettivi,
        "connettivi: {}".format(sorted(connettivi)),
    )
    verifica(
        "nessun connettivo compare anche fra le parole piene",
        connettivi & piene == set(),
        "intersezione: {}".format(sorted(connettivi & piene)),
    )


def prova_parentesi_vuote_contate(radice: Path) -> None:
    """Le parentesi vuote rimosse si contano fra le esclusioni.

    Il difetto: pulisci toglieva «(:)», «( )», «()» dal testo ma, a differenza
    di ogni altra categoria, non incrementava il conteggio delle esclusioni.
    """
    esc: pv.Counter = pv.Counter()
    ripulito = pv.pulisci("Testo con (:) e ( ) e () dentro il corpo.", esc)
    verifica(
        "le tre parentesi vuote sono contate",
        esc.get("parentesi_vuote") == 3,
        "esclusioni: {}".format(dict(esc)),
    )
    verifica(
        "le parentesi vuote sono davvero tolte dal testo",
        "(" not in ripulito and ")" not in ripulito,
        "ripulito: {!r}".format(ripulito),
    )
    # Un indirizzo fra parentesi non deve produrre una parentesi vuota fantasma:
    # la rimozione dell'email lascia «( )», ma non era una parentesi vuota
    # dell'autore, e il conteggio si fa sul testo originale.
    esc2: pv.Counter = pv.Counter()
    pv.pulisci("Scrivimi a (mario.rossi@example.com) quando vuoi.", esc2)
    verifica(
        "un'email fra parentesi non genera una parentesi vuota fantasma",
        esc2.get("parentesi_vuote", 0) == 0,
        "esclusioni: {}".format(dict(esc2)),
    )


def prova_re_email_non_e_quadratica(radice: Path) -> None:
    """La ricerca delle email resta lineare, e le email vere si riconoscono.

    Il difetto: la parte locale senza tetto di lunghezza faceva ripartire il
    motore da ogni confine di parola, e su una catena lunga di caratteri
    ammessi ma senza chiocciola il tempo cresceva col quadrato della lunghezza.
    I limiti di lunghezza sui tratti tengono la ricerca lineare.

    La prova non fissa un tempo assoluto, che dipende dalla macchina: misura
    come il tempo scala. Su una catena quattro volte più lunga un algoritmo
    lineare impiega circa quattro volte tanto, uno quadratico circa sedici. La
    soglia a otto sta nel mezzo, con margine da entrambi i lati.
    """
    from time import perf_counter

    def tempo(catena: str) -> float:
        misure = []
        for _ in range(5):
            avvio = perf_counter()
            pv.RE_EMAIL.findall(catena)
            misure.append(perf_counter() - avvio)
        return min(misure)

    piccolo = "a." * 8000
    grande = "a." * 32000  # quattro volte più lungo, molti confini, nessuna @
    t_piccolo = tempo(piccolo)
    t_grande = tempo(grande)
    rapporto = t_grande / t_piccolo if t_piccolo else float("inf")
    verifica(
        "il tempo di RE_EMAIL scala lineare, non quadratico",
        rapporto < 8.0,
        "quattro volte la catena, tempo x{:.1f}".format(rapporto),
    )

    # Non-regressione: le email vere restano riconosciute, con la lista esatta.
    casi = [
        ("Scrivimi a mario.rossi@example.com per informazioni.",
         ["mario.rossi@example.com"]),
        ("Due indirizzi: a@b.co e nome+tag@sub.dominio.it insieme.",
         ["a@b.co", "nome+tag@sub.dominio.it"]),
        ("Un host con trattino: utente@mio-host.co.uk scrive spesso.",
         ["utente@mio-host.co.uk"]),
        ("Nessuna chiocciola qui, e utente@senzadominio da solo non conta.",
         []),
    ]
    for indice, (testo, atteso) in enumerate(casi, 1):
        ottenuto = pv.RE_EMAIL.findall(testo)
        verifica(
            "email riconosciute, caso {}".format(indice),
            ottenuto == atteso,
            "atteso {}, ottenuto {}".format(atteso, ottenuto),
        )
    # Un indirizzo con parte locale lunga ma non assurda va ancora rimosso: i
    # tetti sono generosi, non fermi a 64, per non lasciarlo nel testo a
    # gonfiare i conteggi come se fossero parole.
    indirizzo_lungo = "a" * 100 + "@dominio.it"
    verifica(
        "un indirizzo con parte locale lunga viene comunque riconosciuto",
        pv.RE_EMAIL.findall("Scrivi a " + indirizzo_lungo + " oggi.") == [indirizzo_lungo],
        "ottenuto: {}".format(pv.RE_EMAIL.findall(indirizzo_lungo)),
    )


def prova_errore_scrittura_senza_percorso(radice: Path) -> None:
    """Il messaggio d'errore di scrittura non rivela il percorso assoluto.

    Il difetto: il testo predefinito dell'OSError riportava il percorso
    completo del file, compreso il nome utente del sistema, e finiva su stderr.
    """
    # Il percorso si costruisce nativo (con radice reale), non a mano con i
    # backslash di Windows: su POSIX pathlib non li scomporrebbe, e la prova
    # fallirebbe su codice sano. La cartella intermedia fa da spia del percorso.
    segreto = radice / "cartella-utente-privata" / "scheda-voce.md"
    finto = OSError(17, "Impossibile creare un file", str(segreto))
    msg = pv.errore_scrittura_pulito(finto)
    verifica(
        "il messaggio non contiene il percorso, solo il nome del file",
        "cartella-utente-privata" not in msg and "scheda-voce.md" in msg,
        "messaggio: {}".format(msg),
    )
    verifica(
        "il messaggio tiene il nome del file e il motivo",
        "scheda-voce.md" in msg and "Impossibile creare un file" in msg,
        "messaggio: {}".format(msg),
    )
    senza = OSError(28, "Spazio su disco esaurito")
    msg_senza = pv.errore_scrittura_pulito(senza)
    verifica(
        "un errore senza file dà comunque un messaggio col motivo",
        "Spazio su disco esaurito" in msg_senza,
        "messaggio: {}".format(msg_senza),
    )


def prova_versione_allineata(radice: Path) -> None:
    """La versione dello strumento è allineata e coerente col JSON.

    Il difetto: VERSIONE era ferma a «1.0.0», disallineata dalla versione della
    skill in cui lo strumento esce.
    """
    verifica(
        "VERSIONE non è più il vecchio 1.0.0 disallineato",
        pv.VERSIONE != "1.0.0",
        "VERSIONE: {}".format(pv.VERSIONE),
    )
    verifica(
        "VERSIONE ha il formato semver X.Y.Z",
        re.fullmatch(r"\d+\.\d+\.\d+", pv.VERSIONE) is not None,
        "VERSIONE: {}".format(pv.VERSIONE),
    )
    corpus = radice / "versione"
    corpus.mkdir()
    (corpus / "testo.txt").write_text(TESTO_ACCENTATO, encoding="utf-8")
    profilo = pv.calcola_profilo(corpus, "Prova")
    verifica(
        "il JSON riporta la stessa versione della costante",
        profilo["strumento"]["versione"] == pv.VERSIONE,
        "nel json: {}, costante: {}".format(
            profilo["strumento"]["versione"], pv.VERSIONE
        ),
    )


def prova_estensione_markdown_nei_messaggi(radice: Path) -> None:
    """Il messaggio «nessun file» elenca tutte e tre le estensioni raccolte.

    Il difetto: raccogli_file prende .txt, .md e .markdown, ma il messaggio
    d'errore ne nominava solo due.
    """
    corpus = radice / "senza-testi"
    corpus.mkdir()
    (corpus / "immagine.png").write_bytes(b"\x89PNG")
    try:
        pv.calcola_profilo(corpus, "Prova")
        verifica("un corpus senza testi solleva un errore", False)
    except pv.ErroreCorpus as errore:
        verifica(
            "il messaggio nomina .txt, .md e .markdown",
            ".txt, .md o .markdown" in str(errore),
            "messaggio: {}".format(errore),
        )


def prova_nome_cartella_senza_percorso(radice: Path) -> None:
    """Il nome della cartella nel JSON non è mai un percorso assoluto.

    Il difetto: per la radice del filesystem, che non ha nome, il campo
    «cartella» ripiegava sul percorso intero (per esempio «C:\\»), che porta
    con sé informazioni di sistema.
    """
    # I percorsi si costruiscono nativi: Path(os.sep) è la radice del filesystem
    # su ogni sistema, mentre «C:/» su POSIX sarebbe un percorso relativo di nome
    # «C:» e farebbe fallire la prova su codice sano.
    for percorso, atteso in (
        (Path(os.sep), "corpus"),          # radice del filesystem, senza nome
        (radice, radice.name),             # una cartella vera, con il suo nome
        (radice / "miei-testi", "miei-testi"),
    ):
        ottenuto = pv.nome_cartella(percorso)
        verifica(
            "nome cartella pulito per {}".format(percorso),
            ottenuto == atteso and "/" not in ottenuto and "\\" not in ottenuto,
            "ottenuto: {}".format(ottenuto),
        )


def prova_ricorrenze_mostrano_la_forma_lessicale(radice: Path) -> None:
    """Le ricorrenze mostrano la forma lessicale, non la parola tale e quale.

    Il docstring di confronto() prometteva che «nella scheda ogni parola resta
    scritta come l'autore l'ha scritta», ma le ricorrenze usano forma_lessicale,
    che minuscola e stacca l'elisione: «L'amore» vi compare come «amore». Il
    docstring ora lo dichiara, e questa prova fissa sia il comportamento reale
    sia il fatto che la vecchia promessa non torni nel sorgente.
    """
    corpus = radice / "ricorrenze-forma"
    corpus.mkdir()
    testo = (
        "L'amore vince sempre, e l'amore resta anche dopo. "
        "L'amore non chiede, l'amore aspetta con pazienza vera." + NL
    ) * 3
    (corpus / "testo.txt").write_text(testo, encoding="utf-8")
    piene = {
        forma
        for forma, _ in pv.calcola_profilo(corpus, "Prova")["ricorrenze"][
            "parole_piene_frequenti"
        ]
    }
    verifica(
        "l'elisione è staccata nelle ricorrenze: amore, non l'amore",
        "amore" in piene and "l'amore" not in piene,
        "parole piene: {}".format(sorted(piene)),
    )
    sorgente = Path(pv.__file__).read_text(encoding="utf-8")
    verifica(
        "il docstring di confronto non promette più la forma originale",
        "ogni parola resta scritta" not in sorgente,
    )

    # Il difetto trovato sulla scheda vera: nei bigrammi compariva «un po»
    # senza apostrofo, cioè una forma scorretta in un documento che nasce
    # per essere allegato come prova della propria voce. Il controllo è sul
    # documento consegnato all'utente, non sulla sola funzione.
    corpus = radice / "ricorrenze-troncamento"
    corpus.mkdir()
    (corpus / "testo.txt").write_text(
        (
            "Il lavoro va un po' meglio di ieri, e la giornata scorre. "
            "Aspetta un po' prima di rispondere a quella lettera lunga. "
            "Serve un po' di pazienza per arrivare in fondo al discorso." + NL
        ) * 2,
        encoding="utf-8",
    )
    profilo = pv.calcola_profilo(corpus, "Prova")
    bigrammi = {forma for forma, _ in profilo["ricorrenze"]["bigrammi_ricorrenti"]}
    scheda = pv.scrivi_scheda(profilo)
    verifica(
        "il bigramma tiene l'apostrofo: un po', mai un po",
        "un po'" in bigrammi and "un po" not in bigrammi,
        "bigrammi: {}".format(sorted(bigrammi)),
    )
    verifica(
        "la scheda consegnata non mostra la forma senza apostrofo",
        "un po'" in scheda,
        "cercato «un po'» nella scheda",
    )


def prova_doppioni_del_corpus(radice: Path) -> None:
    """Un file raggiunto da due nomi diversi si conta una volta sola.

    Il difetto: la deduplica avveniva sui percorsi non risolti, quindi un
    hard link (o un collegamento simbolico interno) a un file già nel corpus
    lo faceva leggere e contare due volte. Ora l'identità del file, cioè il
    dispositivo e il numero di inode, riconosce che è lo stesso.
    """
    corpus = radice / "doppioni"
    corpus.mkdir()
    originale = corpus / "aaa_originale.txt"
    originale.write_text(TESTO_ACCENTATO, encoding="utf-8")
    parole_uno = pv.calcola_profilo(corpus, "Prova")["corpus"]["parole_totali"]

    # Hard link: stesso file, nome diverso. Su NTFS non serve alcun privilegio,
    # quindi questo ramo di norma gira davvero anche su Windows.
    duplicato = corpus / "zzz_duplicato.txt"
    try:
        os.link(originale, duplicato)
    except (OSError, NotImplementedError) as errore:
        salta(
            "doppioni del corpus (hard link)",
            "il sistema non permette di creare l'hard link ({})".format(
                type(errore).__name__
            ),
        )
    else:
        letti = sorted(percorso.name for percorso in pv.raccogli_file(corpus))
        verifica(
            "un hard link interno non aggiunge un secondo file",
            letti == ["aaa_originale.txt"],
            "letti: {}".format(letti),
        )
        corpo = pv.calcola_profilo(corpus, "Prova")["corpus"]
        verifica(
            "l'hard link non raddoppia le parole",
            corpo["parole_totali"] == parole_uno,
            "un file: {}, con l'hard link: {}".format(
                parole_uno, corpo["parole_totali"]
            ),
        )
        verifica(
            "il doppione è dichiarato fra le esclusioni",
            corpo["esclusioni_in_pulizia"].get("doppioni_del_corpus") == 1,
            "esclusioni: {}".format(corpo["esclusioni_in_pulizia"]),
        )

    # Collegamento simbolico interno a un file già presente: stesso caso, ma
    # su Windows serve un privilegio, quindi questo ramo salta da sé.
    corpus_link = radice / "doppioni-link"
    corpus_link.mkdir()
    (corpus_link / "aaa_originale.txt").write_text(TESTO_ACCENTATO, encoding="utf-8")
    collegamento = corpus_link / "zzz_collegamento.txt"
    try:
        collegamento.symlink_to(corpus_link / "aaa_originale.txt")
    except (OSError, NotImplementedError) as errore:
        salta(
            "doppioni del corpus (collegamento simbolico interno)",
            "il sistema non permette di creare il collegamento ({})".format(
                type(errore).__name__
            ),
        )
        return
    letti = sorted(percorso.name for percorso in pv.raccogli_file(corpus_link))
    verifica(
        "un collegamento simbolico interno non aggiunge un secondo file",
        letti == ["aaa_originale.txt"],
        "letti: {}".format(letti),
    )


def prova_nomi_uscita_case_insensitive(radice: Path) -> None:
    """Un file col nome di un'uscita, in maiuscole diverse, resta escluso.

    Il difetto: il confronto con i nomi delle uscite era sensibile alle
    maiuscole, quindi «Scheda-Voce.md» sfuggiva all'esclusione e su un
    filesystem che non distingue le maiuscole finiva nel corpus, dove è la
    stessa uscita che lo strumento scrive.
    """
    corpus = radice / "nomi-uscita"
    corpus.mkdir()
    (corpus / "testo.txt").write_text(TESTO_ACCENTATO, encoding="utf-8")
    (corpus / "Scheda-Voce.md").write_text("Roba mia, non un'uscita." + NL, encoding="utf-8")
    letti = sorted(percorso.name for percorso in pv.raccogli_file(corpus))
    verifica(
        "un nome d'uscita in maiuscole diverse resta escluso",
        letti == ["testo.txt"],
        "letti: {}".format(letti),
    )


PROVE = (
    prova_accenti_riconosciuti,
    prova_paragrafi_a_capo_singolo,
    prova_uscita_esclusa_dal_corpus,
    prova_accenti_nel_sorgente,
    prova_a_capo_rigido_non_fa_sparire_la_prosa,
    prova_decimali_allitaliana,
    prova_file_illeggibile_non_ferma_il_corpus,
    prova_codifica_riconosciuta_dal_contrassegno,
    prova_cartelle_collegate_non_rompono_la_scansione,
    prova_estensioni_maiuscole_raccolte,
    prova_virgolette_chiuse_non_fondono_le_frasi,
    prova_domande_fra_virgolette_contate,
    prova_elenchi_e_citazioni_non_perdono_prosa,
    prova_dialogo_non_diventa_titolo,
    prova_separatore_di_citazione_non_cambia_la_classificazione,
    prova_elenco_non_ingoia_il_paragrafo_nuovo,
    prova_dividi_frasi_lineare_con_spazi_unicode,
    prova_spoglia_segni_di_chiusura_non_e_quadratica,
    prova_unisci_righe_non_e_superlineare,
    prova_dividi_frasi_non_e_quadratico,
    prova_elisioni_staccate,
    prova_ttr_grezzo_fuori_dal_posizionamento,
    prova_anno_a_inizio_riga_non_e_elenco,
    prova_frontmatter_riconosciuto,
    prova_frontmatter_non_chiuso_non_perde_la_prosa,
    prova_righe_vuote_finali_conservate,
    prova_frasi_vuote_non_gonfiano_il_gulpease,
    prova_connettivi_non_fra_le_parole_piene,
    prova_parentesi_vuote_contate,
    prova_re_email_non_e_quadratica,
    prova_errore_scrittura_senza_percorso,
    prova_versione_allineata,
    prova_estensione_markdown_nei_messaggi,
    prova_nome_cartella_senza_percorso,
    prova_ricorrenze_mostrano_la_forma_lessicale,
    prova_doppioni_del_corpus,
    prova_nomi_uscita_case_insensitive,
    prova_sovrascrittura_solo_con_firma,
    prova_firma_riconosciuta_solo_in_testa,
    prova_contenimento,
)


def main() -> int:
    with tempfile.TemporaryDirectory(prefix="prova-profilo-voce-") as temporanea:
        radice = Path(temporanea)
        for prova in PROVE:
            try:
                prova(radice)
            except Exception as errore:  # noqa: BLE001
                # Qui la cattura larga è giusta, al contrario che nel codice
                # dello strumento: questo è il banco di prova, e un'eccezione
                # in una prova non deve impedire alle altre di girare. Le due
                # sulla sicurezza chiudono l'elenco, e senza questo blocco un
                # errore nelle prime le lasciava senza esecuzione. L'errore
                # non viene inghiottito: diventa una prova fallita, con nome
                # e messaggio.
                verifica(
                    "{}: nessuna eccezione imprevista".format(prova.__name__),
                    False,
                    "{}: {}".format(type(errore).__name__, errore),
                )

    fallite = [nome for nome, esito, _ in esiti if not esito]
    print("")
    print(
        "{}, {}, {}.".format(
            accorda(len(esiti), "prova", "prove"),
            accorda(len(fallite), "fallita", "fallite"),
            accorda(len(saltate), "saltata", "saltate"),
        )
    )
    for nome, motivo in saltate:
        print("  saltata: {} ({})".format(nome, motivo))
    return 1 if fallite else 0


if __name__ == "__main__":
    sys.exit(main())

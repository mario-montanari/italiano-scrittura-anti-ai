#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Calcola il profilo quantitativo di una voce autoriale su un corpus italiano.

Fa parte della skill italiano-scrittura-anti-ai. Legge una cartella di testi
scritti dalla stessa persona nello stesso registro e produce due file: una
scheda leggibile e i dati grezzi in formato JSON.

    python profilo_voce.py CARTELLA [--out CARTELLA] [--nome "Nome autore"]

Non usa librerie esterne, non accede alla rete, non modifica i file del
corpus e non scrive nulla fuori dalla cartella di uscita.

Le decisioni di conteggio (cosa e una frase, cosa e una parola, cosa viene
escluso) sono dichiarate nel reference della skill e valgono come contratto:
chi rifa i conti a mano deve ottenere gli stessi numeri.

Questo strumento misura. Non giudica, non riscrive, non stabilisce se un
testo sia stato generato da una macchina.
"""

from __future__ import annotations

import argparse
import json
import re
import statistics
import sys
import unicodedata
from collections import Counter
from pathlib import Path
from typing import Dict, Iterable, List, Optional, Sequence, Tuple

VERSIONE = "1.0.0"
SOGLIA_PAROLE_AFFIDABILE = 2000
FINESTRA_MATTR = 50
FINESTRA_TTR_CONFRONTO = 1000
PAROLE_MINIME_BLOCCO_GULPEASE = 100
MAX_PAROLE_TITOLO = 15

# Sotto questa quota di righe vuote il file non usa la riga bianca per
# separare i paragrafi: lo fa con il ritorno a capo singolo, come in molti
# testi salvati da un elaboratore di testi. Cercare le righe bianche in un
# file cosi impasterebbe decine di paragrafi in un blocco solo, e la misura
# del respiro del paragrafo diventerebbe un artefatto del formato.
QUOTA_RIGHE_VUOTE_PER_STILE_MARKDOWN = 0.20

# --------------------------------------------------------------------------
# Liste chiuse
# --------------------------------------------------------------------------

# Abbreviazioni italiane il cui punto non chiude la frase.
ABBREVIAZIONI = frozenset(
    """
    ecc etc dott dott.ssa dr prof prof.ssa avv ing arch geom rag sig sig.ra
    sigg on rev mons cav comm egr spett gent
    art artt cfr ed es pag pagg pp cap capp vol voll fig figg tab tabb par
    sez nn num tel fax cod cap str p.zza v.le c.so loc fraz
    a.c d.c sec secc ca vs cd c.d n.b p.s p.es
    """.split()
)

# Parole vuote: escluse dal conteggio delle parole piu frequenti (6.7).
# Restano invece dentro gli n-grammi, perche i tic autentici sono spesso
# fatti proprio di parole vuote (*il tuo utente*, *e compito del*).
PAROLE_VUOTE = frozenset(
    """
    il lo la i gli le l un uno una un' del dello della dei degli delle dell
    al allo alla ai agli alle all dal dallo dalla dai dagli dalle dall
    nel nello nella nei negli nelle nell sul sullo sulla sui sugli sulle sull
    col coi di a da in con su per tra fra
    e ed o od ma se anche pure ne ci vi si che chi cui come quando mentre
    perche perche' poiche poiche' dunque quindi allora invece pero pero'
    non piu piu' meno molto poco tanto troppo assai gia gia' ancora sempre
    mai forse solo soltanto proprio anzi cioe cioe' ovvero oppure
    essere sono sei siamo siete e' era eri erano eravamo eravate fu furono
    sara sara' saranno sia siano stato stata stati state essendo
    avere ho hai ha abbiamo avete hanno aveva avevo avevi avevamo avevate
    avevano avro avro' avra' avranno abbia abbiano avuto avendo
    fare fa fanno fatto puo puo' possono potere deve devono dovere
    questo questa questi queste quello quella quelli quelle
    io tu lui lei noi voi loro me te se' mi ti gli le ne
    mio mia miei mie tuo tua tuoi tue suo sua suoi sue nostro nostra nostri
    nostre vostro vostra vostri vostre
    ogni tutti tutte tutto tutta alcuni alcune qualche altro altra altri altre
    stesso stessa stessi stesse tale tali
    c ci n s v d
    """.split()
)

# Connettivi contati a parte (6.7): sono il marcatore piu citato
# in metodologie-operative.md sezione 6.
CONNETTIVI = frozenset(
    """
    inoltre tuttavia pertanto quindi dunque infatti ovvero invece mentre
    perche perche' poiche poiche' sebbene benche benche' qualora laddove
    nonostante affinche affinche' altresi altresi' peraltro comunque
    ciononostante conseguentemente successivamente precedentemente
    """.split()
)

PRONOMI = {
    "prima_singolare": frozenset("io mi me mio mia miei mie".split()),
    "prima_plurale": frozenset("noi ci nostro nostra nostri nostre".split()),
    "seconda_singolare": frozenset("tu ti te tuo tua tuoi tue".split()),
    "seconda_plurale": frozenset("voi vi vostro vostra vostri vostre".split()),
}

# Intervalli citati in references/metodologie-operative.md sezione 6.
# Quella sezione dichiara di se stessa che sono stime indicative, ordini di
# grandezza su campioni limitati, non misurazioni con intervallo di
# confidenza. Servono a collocare, mai a emettere un verdetto.
RIFERIMENTI = {
    "cv_lunghezza_frase": {
        "etichetta": "Coefficiente di variazione della lunghezza di frase",
        "umano": (0.55, 0.75),
        "confronto_ai": "GPT 0,25-0,35",
    },
    "sigma_lunghezza_frase": {
        "etichetta": "Deviazione standard della lunghezza di frase",
        "umano": (8.0, 12.0),
        "confronto_ai": "GPT 4-5, Claude 5-6",
    },
    "ttr_finestra_1000": {
        "etichetta": "Varieta lessicale su finestre di mille parole",
        "umano": (0.52, 0.62),
        "confronto_ai": "GPT 0,40-0,48",
        "cautela": (
            "misura che non discrimina da sola. Un corpus tematicamente "
            "ristretto ripete il lessico del suo campo e scende sotto "
            "l'intervallo per ragioni di argomento, non di autore. Nel "
            "collaudo di questo strumento un testo generato ha ottenuto "
            "varieta piu alta di un testo umano, perche la prosa burocratica "
            "evita la ripetizione con la variazione elegante, che e a sua "
            "volta un tic"
        ),
    },
    "quota_hapax": {
        "etichetta": "Parole usate una volta sola sul vocabolario",
        "umano": (0.45, 0.55),
        "confronto_ai": "GPT 0,30-0,40",
        "cautela": "intervallo osservato su narrativa, non su saggistica",
    },
    "connettivi_percento": {
        "etichetta": "Densita di connettivi sul totale delle parole",
        "umano": (1.5, 2.0),
        "confronto_ai": "testi generati 3-5",
        "cautela": (
            "la fonte non dichiara quali connettivi conta: il confronto vale "
            "solo rispetto all'elenco chiuso usato da questo strumento"
        ),
    },
    "trattini_lunghi_per_mille": {
        "etichetta": "Trattini lunghi ogni mille parole",
        "umano": (0.0, 0.5),
        "confronto_ai": "testi generati italiani 2-5",
    },
    "gulpease_deviazione_blocchi": {
        "etichetta": "Variazione del Gulpease fra i blocchi del testo",
        "umano": (6.0, 10.0),
        "confronto_ai": "testi generati sotto 3-4",
    },
}

# --------------------------------------------------------------------------
# Espressioni regolari
# --------------------------------------------------------------------------

RE_URL = re.compile(r"(?:https?://|www\.)\S+", re.IGNORECASE)
RE_EMAIL = re.compile(r"\b[\w.+-]+@[\w-]+\.[\w.-]+\b")
RE_MARCATORE_H = re.compile(r"\(\s*h\s*[1-6]\s*\)", re.IGNORECASE)
RE_MARCATORE_IMG = re.compile(
    r"^\s*(?:img\b.*|\[img[^\]]*\]|immagine di esempio.*)$", re.IGNORECASE
)
RE_TITOLO_MD = re.compile(r"^\s*#{1,6}\s+")
RE_ELENCO = re.compile(r"^\s*(?:[-*•·–]+|\d+[.)]|[a-z][.)])\s+")
RE_PARENTESI_VUOTE = re.compile(r"\(\s*[:,;]?\s*\)")
RE_SPAZI = re.compile(r"[ \t ]+")
RE_TERMINATORE = re.compile(r"[.!?…]+")
# Il trattino interno non separa: *e-commerce* e *social-media* sono parole
# composte, non due parole. Il trattino usato come inciso ha spazi intorno e
# quindi non rientra in questa forma.
RE_PAROLA = re.compile(r"[\w'’]+(?:-[\w'’]+)*", re.UNICODE)


# --------------------------------------------------------------------------
# Lettura del corpus
# --------------------------------------------------------------------------


class ErroreCorpus(Exception):
    """Errore che impedisce di calcolare il profilo."""


def leggi_file(percorso: Path) -> Tuple[str, str]:
    """Legge un file di testo e restituisce contenuto e codifica usata.

    Tenta UTF-8, anche con BOM. Ripiega su cp1252, la codifica dei file di
    testo salvati su Windows. Una codifica sbagliata rovina accenti e
    apostrofi, quindi anche i conteggi: per questo la codifica effettiva
    finisce nel rapporto.
    """
    dati = percorso.read_bytes()
    for codifica in ("utf-8-sig", "utf-8", "cp1252"):
        try:
            return dati.decode(codifica), codifica
        except UnicodeDecodeError:
            continue
    raise ErroreCorpus(
        "Il file {} non e leggibile ne in UTF-8 ne in cp1252.".format(percorso.name)
    )


def raccogli_file(cartella: Path) -> List[Path]:
    """Elenca i file di testo del corpus, in ordine deterministico."""
    if not cartella.exists():
        raise ErroreCorpus("La cartella {} non esiste.".format(cartella))
    if not cartella.is_dir():
        raise ErroreCorpus("{} non e una cartella.".format(cartella))
    trovati: List[Path] = []
    for estensione in ("*.txt", "*.md", "*.markdown"):
        trovati.extend(cartella.rglob(estensione))
    return sorted(set(trovati))


# --------------------------------------------------------------------------
# Pulizia e segmentazione
# --------------------------------------------------------------------------


def normalizza(testo: str) -> str:
    """Uniforma apostrofi, virgolette e spazi senza toccare le lettere."""
    testo = unicodedata.normalize("NFC", testo)
    testo = testo.replace("\r\n", "\n").replace("\r", "\n")
    testo = testo.replace("’", "'").replace("ʼ", "'")
    return testo


def pulisci(testo: str, esclusioni: Counter) -> str:
    """Toglie cio che non e prosa d'autore, contando ogni rimozione."""
    esclusioni["indirizzi_web"] += len(RE_URL.findall(testo))
    testo = RE_URL.sub(" ", testo)
    esclusioni["indirizzi_posta"] += len(RE_EMAIL.findall(testo))
    testo = RE_EMAIL.sub(" ", testo)
    esclusioni["marcatori_impaginazione"] += len(RE_MARCATORE_H.findall(testo))
    testo = RE_MARCATORE_H.sub(" ", testo)
    testo = RE_PARENTESI_VUOTE.sub(" ", testo)
    return testo


def conta_parole_grezze(riga: str) -> int:
    """Conta le parole di una riga senza costruire la lista."""
    return sum(1 for token in RE_PAROLA.findall(riga) if contiene_lettera(token))


def contiene_lettera(token: str) -> bool:
    return any(carattere.isalpha() for carattere in token)


def classifica_righe(testo: str, esclusioni: Counter) -> List[Tuple[str, str]]:
    """Etichetta ogni riga come vuota, titolo, elenco o prosa.

    Regole dichiarate:
    - una riga che inizia con marcatore Markdown o con (h1)...(h6) e titolo;
    - una riga che inizia con trattino, asterisco o numero puntato e elenco;
    - una riga che non finisce con punteggiatura forte o due punti e ha meno
      di quindici parole e titolo, e non entra nei conteggi;
    - tutto il resto e prosa.
    I blocchi di codice e il frontmatter vengono saltati per intero.
    """
    righe: List[Tuple[str, str]] = []
    dentro_codice = False
    dentro_frontmatter = False
    for indice, riga_grezza in enumerate(testo.split("\n")):
        riga = RE_SPAZI.sub(" ", riga_grezza).strip()

        if riga.startswith("```") or riga.startswith("~~~"):
            dentro_codice = not dentro_codice
            esclusioni["righe_di_codice"] += 1
            continue
        if dentro_codice:
            esclusioni["righe_di_codice"] += 1
            continue

        if riga == "---":
            if indice == 0:
                dentro_frontmatter = True
                esclusioni["righe_di_metadati"] += 1
                continue
            if dentro_frontmatter:
                dentro_frontmatter = False
                esclusioni["righe_di_metadati"] += 1
                continue
        if dentro_frontmatter:
            esclusioni["righe_di_metadati"] += 1
            continue

        if not riga:
            righe.append(("vuota", ""))
            continue

        if RE_TITOLO_MD.match(riga) or RE_MARCATORE_IMG.match(riga):
            esclusioni["titoli_e_marcatori"] += 1
            righe.append(("titolo", riga))
            continue

        if RE_ELENCO.match(riga):
            righe.append(("elenco", RE_ELENCO.sub("", riga, count=1).strip()))
            continue

        if riga[-1] not in ".!?…:" and conta_parole_grezze(riga) < MAX_PAROLE_TITOLO:
            esclusioni["titoli_e_marcatori"] += 1
            righe.append(("titolo", riga))
            continue

        righe.append(("prosa", riga))
    return righe


def dividi_in_frasi(testo: str) -> List[str]:
    """Divide un blocco di prosa in frasi secondo le regole dichiarate.

    Chiudono la frase il punto, il punto esclamativo, il punto interrogativo
    e i puntini di sospensione, quando sono seguiti da spazio o fine testo e
    la parola successiva non comincia per minuscola. Non chiudono i due
    punti, il punto e virgola, il punto delle abbreviazioni note, il punto
    fra cifre e il punto di un'iniziale puntata.
    """
    frasi: List[str] = []
    inizio = 0
    for confine in RE_TERMINATORE.finditer(testo):
        fine = confine.end()
        if fine < len(testo) and not testo[fine].isspace():
            continue

        if confine.group() == ".":
            precedente = testo[: confine.start()]
            ultimo = precedente.rsplit(" ", 1)[-1] if precedente else ""
            nudo = ultimo.strip("«»()[]\"'").lower()
            if nudo in ABBREVIAZIONI:
                continue
            if len(nudo) == 1 and nudo.isalpha():
                continue

        resto = testo[fine:].lstrip()
        if resto and resto[0].isalpha() and resto[0].islower():
            continue

        frase = testo[inizio:fine].strip()
        if frase:
            frasi.append(frase)
        inizio = fine

    coda = testo[inizio:].strip()
    if coda:
        frasi.append(coda)
    return frasi


def righe_vuote_separano_i_paragrafi(righe: Sequence[Tuple[str, str]]) -> bool:
    """Rileva come il file separa i paragrafi.

    Un file Markdown lascia una riga bianca fra un paragrafo e l'altro. Un
    testo salvato da un elaboratore di testi va a capo una volta sola. Se si
    applica la regola sbagliata, decine di paragrafi finiscono in un blocco
    unico e la misura del respiro del paragrafo descrive il formato del file
    invece della voce di chi scrive.
    """
    vuote = sum(1 for tipo, _ in righe if tipo == "vuota")
    piene = sum(1 for tipo, _ in righe if tipo in ("prosa", "elenco"))
    if piene == 0:
        return True
    return vuote / piene >= QUOTA_RIGHE_VUOTE_PER_STILE_MARKDOWN


def costruisci_paragrafi(
    righe: Sequence[Tuple[str, str]], righe_vuote_separano: bool = True
) -> List[List[Tuple[str, bool]]]:
    """Raggruppa le righe in paragrafi di frasi.

    Ogni frase porta con se l'informazione se proviene da una voce di
    elenco: chi scrive molto per elenchi ha frasi piu corte per un motivo
    strutturale, e la scheda deve poterlo dire.

    Quando le righe vuote non separano i paragrafi, ogni riga di prosa e un
    paragrafo a se, mentre le voci di elenco contigue restano insieme perche
    formano un blocco solo sulla pagina.
    """
    paragrafi: List[List[Tuple[str, bool]]] = []
    corrente: List[Tuple[str, bool]] = []
    buffer_prosa: List[str] = []

    def svuota_prosa() -> None:
        if buffer_prosa:
            unito = " ".join(buffer_prosa)
            corrente.extend((frase, False) for frase in dividi_in_frasi(unito))
            buffer_prosa.clear()

    def chiudi_paragrafo() -> None:
        svuota_prosa()
        if corrente:
            paragrafi.append(list(corrente))
            corrente.clear()

    tipo_precedente = "vuota"
    for tipo, contenuto in righe:
        if tipo in ("vuota", "titolo"):
            chiudi_paragrafo()
        elif tipo == "elenco":
            if not righe_vuote_separano and tipo_precedente != "elenco":
                chiudi_paragrafo()
            else:
                svuota_prosa()
            frasi = dividi_in_frasi(contenuto)
            if not frasi and contenuto:
                frasi = [contenuto]
            corrente.extend((frase, True) for frase in frasi)
        else:
            if not righe_vuote_separano:
                chiudi_paragrafo()
            buffer_prosa.append(contenuto)
        tipo_precedente = tipo
    chiudi_paragrafo()
    return paragrafi


# --------------------------------------------------------------------------
# Estrazione di parole
# --------------------------------------------------------------------------


def parole_di(testo: str) -> List[str]:
    """Parole come si vedono sulla pagina: l'apostrofo interno non separa."""
    return [token for token in RE_PAROLA.findall(testo) if contiene_lettera(token)]


def forma_lessicale(parola: str) -> str:
    """Forma usata per i conteggi di vocabolario.

    Stacca l'elisione iniziale e riduce a minuscolo, altrimenti
    *l'attenzione* e *attenzione* risulterebbero due parole diverse e la
    varieta lessicale uscirebbe gonfiata. Non e una lemmatizzazione: le
    forme flesse restano distinte, e lo strumento lo dichiara.
    """
    minuscola = parola.lower()
    if "'" in minuscola:
        testa, _, coda = minuscola.partition("'")
        if coda and len(testa) <= 3:
            return coda
        if not coda:
            return testa
    return minuscola


def conta_lettere(testo: str) -> int:
    return sum(1 for carattere in testo if carattere.isalpha())


# --------------------------------------------------------------------------
# Misure
# --------------------------------------------------------------------------


def deviazione(valori: Sequence[float]) -> float:
    """Deviazione standard campionaria, zero se il campione e minimo."""
    return statistics.stdev(valori) if len(valori) > 1 else 0.0


def gulpease(frasi: int, lettere: int, parole: int) -> Optional[float]:
    """Indice Gulpease (Lucisano e Piemontese, 1988)."""
    if parole == 0:
        return None
    return 89 + (300 * frasi - 10 * lettere) / parole


def mattr(forme: Sequence[str], finestra: int) -> Optional[float]:
    """Type-Token Ratio a finestra mobile (Covington e McFall, 2010).

    Su testi piu corti della finestra restituisce il rapporto grezzo, che
    dipende dalla lunghezza: la scheda lo segnala invece di tacerlo.
    """
    totale = len(forme)
    if totale == 0:
        return None
    if totale <= finestra:
        return len(set(forme)) / totale

    conteggi = Counter(forme[:finestra])
    distinte = len(conteggi)
    somma = distinte
    misurazioni = 1
    for indice in range(finestra, totale):
        uscente = forme[indice - finestra]
        conteggi[uscente] -= 1
        if conteggi[uscente] == 0:
            del conteggi[uscente]
            distinte -= 1
        entrante = forme[indice]
        if entrante not in conteggi:
            distinte += 1
        conteggi[entrante] += 1
        somma += distinte
        misurazioni += 1
    return somma / misurazioni / finestra


def ngrammi_ricorrenti(
    frasi: Sequence[str], dimensione: int, minimo: int, quanti: int
) -> List[Tuple[str, int]]:
    """Sequenze di N parole che ricorrono, senza attraversare le frasi."""
    conteggio: Counter = Counter()
    for frase in frasi:
        forme = [forma_lessicale(parola) for parola in parole_di(frase)]
        for indice in range(len(forme) - dimensione + 1):
            conteggio[" ".join(forme[indice : indice + dimensione])] += 1
    return [
        (sequenza, occorrenze)
        for sequenza, occorrenze in conteggio.most_common(quanti * 4)
        if occorrenze >= minimo
    ][:quanti]


def estremi_di_frase(
    frasi: Sequence[str], quante_parole: int, quanti: int, dalla_fine: bool
) -> List[Tuple[str, int]]:
    """Coppie di parole con cui le frasi piu spesso iniziano o finiscono."""
    conteggio: Counter = Counter()
    for frase in frasi:
        forme = [forma_lessicale(parola) for parola in parole_di(frase)]
        if len(forme) < quante_parole:
            continue
        estremo = forme[-quante_parole:] if dalla_fine else forme[:quante_parole]
        conteggio[" ".join(estremo)] += 1
    return [voce for voce in conteggio.most_common(quanti) if voce[1] > 1]


def posizione_rispetto(valore: Optional[float], chiave: str) -> Optional[Dict]:
    """Colloca un valore rispetto all'intervallo umano citato dalla skill."""
    if valore is None or chiave not in RIFERIMENTI:
        return None
    riferimento = RIFERIMENTI[chiave]
    minimo, massimo = riferimento["umano"]
    if valore < minimo:
        etichetta = "sotto l'intervallo citato per la prosa umana"
    elif valore > massimo:
        etichetta = "sopra l'intervallo citato per la prosa umana"
    else:
        etichetta = "dentro l'intervallo citato per la prosa umana"
    voce = {
        "misura": riferimento["etichetta"],
        "valore": round(valore, 3),
        "intervallo_umano": [minimo, massimo],
        "confronto_ai": riferimento["confronto_ai"],
        "posizione": etichetta,
    }
    if "cautela" in riferimento:
        voce["cautela"] = riferimento["cautela"]
    return voce


def conta_punteggiatura(testo: str, parole: int) -> Dict[str, float]:
    """Frequenza dei segni ogni mille parole."""
    if parole == 0:
        return {}
    grezzi = {
        "virgole": testo.count(","),
        "punti_e_virgola": testo.count(";"),
        "due_punti": testo.count(":"),
        "parentesi_tonde": testo.count("("),
        "puntini_di_sospensione": testo.count("…") + len(re.findall(r"\.{3}", testo)),
        "punti_esclamativi": testo.count("!"),
        "punti_interrogativi": testo.count("?"),
        "trattini_brevi": testo.count("-"),
        "trattini_medi": testo.count("–"),
        "trattini_lunghi": testo.count("—"),
        "caporali": testo.count("«"),
        "virgolette_inglesi": testo.count("“") + testo.count("”"),
        "virgolette_dritte": testo.count('"'),
    }
    return {
        chiave: round(valore * 1000 / parole, 2) for chiave, valore in grezzi.items()
    }


# --------------------------------------------------------------------------
# Costruzione del profilo
# --------------------------------------------------------------------------


def calcola_profilo(cartella: Path, nome: Optional[str]) -> Dict:
    """Legge il corpus e restituisce il profilo completo."""
    percorsi = raccogli_file(cartella)
    if not percorsi:
        raise ErroreCorpus(
            "Nessun file .txt o .md trovato in {}.".format(cartella)
        )

    esclusioni: Counter = Counter()
    schede_file: List[Dict] = []
    paragrafi_totali: List[List[Tuple[str, bool]]] = []
    testo_analizzato: List[str] = []

    for percorso in percorsi:
        contenuto, codifica = leggi_file(percorso)
        contenuto = pulisci(normalizza(contenuto), esclusioni)
        righe = classifica_righe(contenuto, esclusioni)
        stile_markdown = righe_vuote_separano_i_paragrafi(righe)
        paragrafi = costruisci_paragrafi(righe, stile_markdown)
        frasi_file = [frase for paragrafo in paragrafi for frase, _ in paragrafo]
        parole_file = sum(len(parole_di(frase)) for frase in frasi_file)
        if parole_file == 0:
            esclusioni["file_senza_testo"] += 1
            continue
        paragrafi_totali.extend(paragrafi)
        testo_analizzato.extend(frasi_file)
        schede_file.append(
            {
                "file": percorso.name,
                "codifica": codifica,
                "parole": parole_file,
                "frasi": len(frasi_file),
                "paragrafi": len(paragrafi),
                "separazione_paragrafi": "riga vuota"
                if stile_markdown
                else "ritorno a capo singolo",
            }
        )

    if not paragrafi_totali:
        raise ErroreCorpus(
            "Il corpus non contiene prosa analizzabile dopo la pulizia."
        )

    frasi: List[str] = []
    da_elenco: List[bool] = []
    for paragrafo in paragrafi_totali:
        for frase, elenco in paragrafo:
            frasi.append(frase)
            da_elenco.append(elenco)

    lunghezze = [len(parole_di(frase)) for frase in frasi]
    lunghezze = [valore for valore in lunghezze if valore > 0]
    parole_tutte: List[str] = []
    for frase in frasi:
        parole_tutte.extend(parole_di(frase))
    forme = [forma_lessicale(parola) for parola in parole_tutte]
    testo_unito = " ".join(frasi)
    totale_parole = len(parole_tutte)
    totale_lettere = conta_lettere(testo_unito)

    media_lunghezza = statistics.mean(lunghezze) if lunghezze else 0.0
    sigma_lunghezza = deviazione(lunghezze)
    cv_lunghezza = sigma_lunghezza / media_lunghezza if media_lunghezza else 0.0

    fasce = Counter()
    for valore in lunghezze:
        if valore <= 5:
            fasce["1-5"] += 1
        elif valore <= 15:
            fasce["6-15"] += 1
        elif valore <= 25:
            fasce["16-25"] += 1
        elif valore <= 35:
            fasce["26-35"] += 1
        else:
            fasce["oltre 35"] += 1

    frasi_per_paragrafo = [len(paragrafo) for paragrafo in paragrafi_totali]
    parole_per_paragrafo = [
        sum(len(parole_di(frase)) for frase, _ in paragrafo)
        for paragrafo in paragrafi_totali
    ]
    parole_in_elenco = sum(
        len(parole_di(frase))
        for frase, elenco in zip(frasi, da_elenco)
        if elenco
    )

    blocchi: List[Dict[str, int]] = []
    accumulo = {"frasi": 0, "parole": 0, "lettere": 0}
    for paragrafo in paragrafi_totali:
        testo_paragrafo = " ".join(frase for frase, _ in paragrafo)
        accumulo["frasi"] += len(paragrafo)
        accumulo["parole"] += len(parole_di(testo_paragrafo))
        accumulo["lettere"] += conta_lettere(testo_paragrafo)
        if accumulo["parole"] >= PAROLE_MINIME_BLOCCO_GULPEASE:
            blocchi.append(dict(accumulo))
            accumulo = {"frasi": 0, "parole": 0, "lettere": 0}
    if accumulo["parole"] >= PAROLE_MINIME_BLOCCO_GULPEASE:
        blocchi.append(dict(accumulo))
    gulpease_blocchi = [
        valore
        for valore in (
            gulpease(blocco["frasi"], blocco["lettere"], blocco["parole"])
            for blocco in blocchi
        )
        if valore is not None
    ]

    vocabolario = Counter(forme)
    hapax = sum(1 for occorrenze in vocabolario.values() if occorrenze == 1)
    mattr_50 = mattr(forme, FINESTRA_MATTR)
    ttr_1000 = mattr(forme, FINESTRA_TTR_CONFRONTO)

    conteggio_connettivi = sum(
        1 for forma in forme if forma in CONNETTIVI
    )
    percentuale_connettivi = (
        conteggio_connettivi * 100 / totale_parole if totale_parole else 0.0
    )
    connettivi_frequenti = Counter(
        forma for forma in forme if forma in CONNETTIVI
    ).most_common(15)

    persone = {}
    for famiglia, insieme in PRONOMI.items():
        occorrenze = sum(1 for forma in forme if forma in insieme)
        persone[famiglia] = {
            "occorrenze": occorrenze,
            "per_mille_parole": round(occorrenze * 1000 / totale_parole, 2)
            if totale_parole
            else 0.0,
        }
    occorrenze_si = sum(1 for forma in forme if forma == "si")
    persone["costruzioni_con_si"] = {
        "occorrenze": occorrenze_si,
        "per_mille_parole": round(occorrenze_si * 1000 / totale_parole, 2)
        if totale_parole
        else 0.0,
        "nota": "riflessive e impersonali insieme, conteggio per eccesso",
    }

    parole_piene = Counter(
        forma
        for forma in forme
        if forma not in PAROLE_VUOTE and len(forma) > 2
    ).most_common(25)

    punteggiatura = conta_punteggiatura(testo_unito, totale_parole)

    profilo = {
        "strumento": {
            "nome": "profilo_voce.py",
            "versione": VERSIONE,
            "finestra_mattr": FINESTRA_MATTR,
            "finestra_ttr_confronto": FINESTRA_TTR_CONFRONTO,
        },
        "corpus": {
            "autore": nome,
            "cartella": str(cartella),
            "file": schede_file,
            "file_letti": len(schede_file),
            "parole_totali": totale_parole,
            "frasi_totali": len(frasi),
            "paragrafi_totali": len(paragrafi_totali),
            "affidabilita": "solida"
            if totale_parole >= SOGLIA_PAROLE_AFFIDABILE
            else "indicativa",
            "soglia_affidabilita": SOGLIA_PAROLE_AFFIDABILE,
            "esclusioni_in_pulizia": dict(esclusioni),
        },
        "respiro_della_frase": {
            "lunghezza_media": round(media_lunghezza, 2),
            "deviazione_standard": round(sigma_lunghezza, 2),
            "coefficiente_di_variazione": round(cv_lunghezza, 3),
            "mediana": statistics.median(lunghezze) if lunghezze else 0,
            "minimo": min(lunghezze) if lunghezze else 0,
            "massimo": max(lunghezze) if lunghezze else 0,
            "quota_sotto_sei_parole": round(
                sum(1 for valore in lunghezze if valore < 6) * 100 / len(lunghezze), 1
            )
            if lunghezze
            else 0.0,
            "quota_sopra_trentacinque_parole": round(
                sum(1 for valore in lunghezze if valore > 35) * 100 / len(lunghezze), 1
            )
            if lunghezze
            else 0.0,
            "quota_interrogative": round(
                sum(1 for frase in frasi if frase.rstrip().endswith("?"))
                * 100
                / len(frasi),
                1,
            )
            if frasi
            else 0.0,
            "quota_esclamative": round(
                sum(1 for frase in frasi if frase.rstrip().endswith("!"))
                * 100
                / len(frasi),
                1,
            )
            if frasi
            else 0.0,
            "distribuzione_per_fasce": dict(fasce),
        },
        "respiro_del_paragrafo": {
            "frasi_per_paragrafo_media": round(
                statistics.mean(frasi_per_paragrafo), 2
            )
            if frasi_per_paragrafo
            else 0.0,
            "frasi_per_paragrafo_deviazione": round(
                deviazione(frasi_per_paragrafo), 2
            ),
            "parole_per_paragrafo_media": round(
                statistics.mean(parole_per_paragrafo), 2
            )
            if parole_per_paragrafo
            else 0.0,
            "quota_testo_in_elenchi": round(
                parole_in_elenco * 100 / totale_parole, 1
            )
            if totale_parole
            else 0.0,
        },
        "leggibilita": {
            "gulpease_corpus": round(
                gulpease(len(frasi), totale_lettere, totale_parole) or 0.0, 1
            ),
            "blocchi_misurati": len(gulpease_blocchi),
            "gulpease_medio_per_blocco": round(
                statistics.mean(gulpease_blocchi), 1
            )
            if gulpease_blocchi
            else None,
            "gulpease_deviazione_fra_blocchi": round(
                deviazione(gulpease_blocchi), 2
            )
            if gulpease_blocchi
            else None,
        },
        "ricchezza_del_lessico": {
            "mattr_finestra_50": round(mattr_50, 3) if mattr_50 else None,
            "ttr_finestra_1000": round(ttr_1000, 3) if ttr_1000 else None,
            "vocabolario": len(vocabolario),
            "parole_usate_una_volta_sola": hapax,
            "quota_hapax": round(hapax / len(vocabolario), 3) if vocabolario else None,
        },
        "punteggiatura_per_mille_parole": punteggiatura,
        "virgole_per_frase": round(
            testo_unito.count(",") / len(frasi), 2
        )
        if frasi
        else 0.0,
        "persona_e_lettore": persone,
        "ricorrenze": {
            "connettivi_percento_sul_totale": round(percentuale_connettivi, 2),
            "connettivi_frequenti": connettivi_frequenti,
            "parole_piene_frequenti": parole_piene,
            "bigrammi_ricorrenti": ngrammi_ricorrenti(frasi, 2, 3, 20),
            "trigrammi_ricorrenti": ngrammi_ricorrenti(frasi, 3, 3, 20),
            "aperture_di_frase": estremi_di_frase(frasi, 2, 15, dalla_fine=False),
            "chiusure_di_frase": estremi_di_frase(frasi, 2, 15, dalla_fine=True),
        },
    }

    profilo["posizione_rispetto_ai_riferimenti"] = [
        voce
        for voce in (
            posizione_rispetto(cv_lunghezza, "cv_lunghezza_frase"),
            posizione_rispetto(sigma_lunghezza, "sigma_lunghezza_frase"),
            posizione_rispetto(ttr_1000, "ttr_finestra_1000"),
            posizione_rispetto(
                profilo["ricchezza_del_lessico"]["quota_hapax"], "quota_hapax"
            ),
            posizione_rispetto(percentuale_connettivi, "connettivi_percento"),
            posizione_rispetto(
                punteggiatura.get("trattini_lunghi"), "trattini_lunghi_per_mille"
            ),
            posizione_rispetto(
                profilo["leggibilita"]["gulpease_deviazione_fra_blocchi"],
                "gulpease_deviazione_blocchi",
            ),
        )
        if voce is not None
    ]
    return profilo


# --------------------------------------------------------------------------
# Scheda leggibile
# --------------------------------------------------------------------------


def tabella(intestazioni: Sequence[str], righe: Iterable[Sequence[str]]) -> List[str]:
    fuori = ["| " + " | ".join(intestazioni) + " |"]
    fuori.append("|" + "|".join(["---"] * len(intestazioni)) + "|")
    for riga in righe:
        fuori.append("| " + " | ".join(str(cella) for cella in riga) + " |")
    fuori.append("")
    return fuori


def elenco_coppie(voci: Sequence[Sequence], vuoto: str) -> List[str]:
    if not voci:
        return [vuoto, ""]
    return [
        ", ".join("{} ({})".format(voce[0], voce[1]) for voce in voci),
        "",
    ]


def scrivi_scheda(profilo: Dict) -> str:
    """Compone la scheda leggibile, con l'affidabilita in apertura."""
    corpus = profilo["corpus"]
    frase = profilo["respiro_della_frase"]
    paragrafo = profilo["respiro_del_paragrafo"]
    lettura = profilo["leggibilita"]
    lessico = profilo["ricchezza_del_lessico"]
    persone = profilo["persona_e_lettore"]
    ricorrenze = profilo["ricorrenze"]

    titolo = corpus["autore"] or "voce anonima"
    fuori: List[str] = ["# Scheda voce: {}".format(titolo), ""]

    fuori += [
        "> Profilo calcolato su {} file, {} parole totali. Affidabilita: {}.".format(
            corpus["file_letti"], corpus["parole_totali"], corpus["affidabilita"]
        ),
        "> I valori descrivono questo corpus, non una persona: cambiando",
        "> registro cambiano. Questa scheda misura, non giudica.",
        "",
        "Livello **misurato**, prodotto da `profilo_voce.py` versione {}.".format(
            profilo["strumento"]["versione"]
        ),
        "Il livello **osservato** (tic autentici, aperture e chiusure tipiche,",
        "cio che questa voce non fa mai) si aggiunge leggendo il corpus, e cita",
        "sempre il passo da cui nasce.",
        "",
        "## Respiro della frase",
        "",
    ]
    fuori += tabella(
        ["Misura", "Valore"],
        [
            ["Frasi", corpus["frasi_totali"]],
            ["Lunghezza media", "{} parole".format(frase["lunghezza_media"])],
            ["Deviazione standard", frase["deviazione_standard"]],
            [
                "Coefficiente di variazione",
                "{} (variazione del respiro)".format(
                    frase["coefficiente_di_variazione"]
                ),
            ],
            ["Mediana", frase["mediana"]],
            ["Minimo e massimo", "{} e {}".format(frase["minimo"], frase["massimo"])],
            [
                "Frasi sotto le sei parole",
                "{} per cento".format(frase["quota_sotto_sei_parole"]),
            ],
            [
                "Frasi sopra le trentacinque parole",
                "{} per cento".format(frase["quota_sopra_trentacinque_parole"]),
            ],
            [
                "Frasi che sono domande",
                "{} per cento".format(frase["quota_interrogative"]),
            ],
            [
                "Frasi esclamative",
                "{} per cento".format(frase["quota_esclamative"]),
            ],
        ],
    )
    fuori += ["Distribuzione per fasce di lunghezza:", ""]
    fuori += tabella(
        ["Fascia (parole)", "Frasi"],
        [
            [fascia, frase["distribuzione_per_fasce"].get(fascia, 0)]
            for fascia in ("1-5", "6-15", "16-25", "26-35", "oltre 35")
        ],
    )

    fuori += ["## Respiro del paragrafo", ""]
    fuori += tabella(
        ["Misura", "Valore"],
        [
            ["Paragrafi", corpus["paragrafi_totali"]],
            ["Frasi per paragrafo", paragrafo["frasi_per_paragrafo_media"]],
            [
                "Variazione fra paragrafi",
                paragrafo["frasi_per_paragrafo_deviazione"],
            ],
            ["Parole per paragrafo", paragrafo["parole_per_paragrafo_media"]],
            [
                "Testo dentro elenchi",
                "{} per cento".format(paragrafo["quota_testo_in_elenchi"]),
            ],
        ],
    )

    fuori += ["## Leggibilita", ""]
    fuori += tabella(
        ["Misura", "Valore"],
        [
            ["Gulpease sul corpus", lettura["gulpease_corpus"]],
            [
                "Gulpease medio per blocco",
                lettura["gulpease_medio_per_blocco"]
                if lettura["gulpease_medio_per_blocco"] is not None
                else "corpus troppo breve",
            ],
            [
                "Variazione fra blocchi",
                lettura["gulpease_deviazione_fra_blocchi"]
                if lettura["gulpease_deviazione_fra_blocchi"] is not None
                else "corpus troppo breve",
            ],
            ["Blocchi misurati", lettura["blocchi_misurati"]],
        ],
    )
    fuori += [
        "Il Gulpease conta lettere e frasi, non idee: un testo di parole corte",
        "e incomprensibili prende un punteggio alto.",
        "",
    ]

    fuori += ["## Ricchezza del lessico", ""]
    fuori += tabella(
        ["Misura", "Valore"],
        [
            ["Varieta a finestra di 50 parole", lessico["mattr_finestra_50"]],
            ["Varieta a finestra di mille parole", lessico["ttr_finestra_1000"]],
            ["Vocabolario", "{} forme diverse".format(lessico["vocabolario"])],
            ["Usate una volta sola", lessico["parole_usate_una_volta_sola"]],
            ["Quota di parole usate una volta sola", lessico["quota_hapax"]],
        ],
    )
    fuori += [
        "Lo strumento non ha un dizionario: *scrive* e *scrivere* contano come",
        "due parole diverse.",
        "",
        "Le due varieta rispondono a domande diverse e possono divergere. La",
        "finestra corta dice quanto il lessico si muove riga per riga. La",
        "finestra lunga risente del tema: un testo che parla sempre della",
        "stessa cosa ripete le parole di quel campo anche se il resto del",
        "vocabolario e ricco.",
        "",
    ]

    fuori += ["## Punteggiatura, ogni mille parole", ""]
    fuori += tabella(
        ["Segno", "Frequenza"],
        [
            [chiave.replace("_", " "), valore]
            for chiave, valore in profilo["punteggiatura_per_mille_parole"].items()
        ],
    )
    fuori += [
        "Virgole per frase: {}.".format(profilo["virgole_per_frase"]),
        "",
    ]
    segni = profilo["punteggiatura_per_mille_parole"]
    fuori_norma = []
    if segni.get("trattini_lunghi", 0):
        fuori_norma.append(
            "trattini lunghi ({} ogni mille parole), esclusi dalla regola 1".format(
                segni["trattini_lunghi"]
            )
        )
    if segni.get("virgolette_inglesi", 0) or segni.get("virgolette_dritte", 0):
        fuori_norma.append(
            "virgolette non italiane ({} inglesi e {} dritte ogni mille "
            "parole), escluse dalla regola 3, che vuole i caporali".format(
                segni.get("virgolette_inglesi", 0), segni.get("virgolette_dritte", 0)
            )
        )
    if fuori_norma:
        fuori += ["**Avviso.** Il corpus contiene " + "; ".join(fuori_norma) + "."]
        fuori += [
            "Sono segni da correggere, non tratti di voce da riprodurre.",
            "",
        ]

    fuori += ["## Persona e rapporto con il lettore", ""]
    fuori += tabella(
        ["Famiglia", "Occorrenze", "Ogni mille parole"],
        [
            [
                chiave.replace("_", " "),
                valore["occorrenze"],
                valore["per_mille_parole"],
            ]
            for chiave, valore in persone.items()
        ],
    )
    fuori += [
        "Conteggio per difetto: in italiano il soggetto si omette, e *ho",
        "scritto* non contiene pronomi pur essendo prima persona.",
        "",
    ]

    fuori += ["## Ricorrenze", ""]
    fuori += [
        "Densita di connettivi: {} per cento delle parole.".format(
            ricorrenze["connettivi_percento_sul_totale"]
        ),
        "",
        "**Connettivi piu usati.**",
        "",
    ]
    fuori += elenco_coppie(ricorrenze["connettivi_frequenti"], "Nessuno ricorrente.")
    fuori += ["**Parole piene piu frequenti.**", ""]
    fuori += elenco_coppie(ricorrenze["parole_piene_frequenti"], "Nessuna.")
    fuori += ["**Sequenze di due parole che tornano.**", ""]
    fuori += elenco_coppie(ricorrenze["bigrammi_ricorrenti"], "Nessuna.")
    fuori += ["**Sequenze di tre parole che tornano.**", ""]
    fuori += elenco_coppie(ricorrenze["trigrammi_ricorrenti"], "Nessuna.")
    fuori += ["**Aperture di frase ricorrenti.**", ""]
    fuori += elenco_coppie(ricorrenze["aperture_di_frase"], "Nessuna ricorrente.")
    fuori += ["**Chiusure di frase ricorrenti.**", ""]
    fuori += elenco_coppie(ricorrenze["chiusure_di_frase"], "Nessuna ricorrente.")
    fuori += [
        "Una sequenza frequente puo essere un tic autentico da difendere oppure",
        "una zeppa da togliere. Lo strumento non sa distinguerli: nel dubbio",
        "prevale la voce dell'autore.",
        "",
    ]

    fuori += ["## Posizione rispetto ai riferimenti della skill", ""]
    fuori += tabella(
        ["Misura", "Valore", "Intervallo umano citato", "Posizione"],
        [
            [
                voce["misura"],
                voce["valore"],
                "{} - {}".format(*voce["intervallo_umano"]),
                voce["posizione"],
            ]
            for voce in profilo["posizione_rispetto_ai_riferimenti"]
        ],
    )
    cautele = [
        "- {}: {}".format(voce["misura"], voce["cautela"])
        for voce in profilo["posizione_rispetto_ai_riferimenti"]
        if "cautela" in voce
    ]
    if cautele:
        fuori += ["Cautele su singole righe:", ""] + cautele + [""]
    fuori += [
        "**La posizione non e un giudizio.** Stare sotto un intervallo non",
        "rende un testo sospetto, e starci dentro non lo assolve. Le sei",
        "misure vanno lette insieme e incrociate con la lettura: presa da",
        "sola, nessuna distingue una voce umana da un testo generato.",
        "",
    ]
    fuori += [
        "Gli intervalli vengono da `references/metodologie-operative.md`",
        "sezione 6, che dichiara di se stessa: stime indicative, ordini di",
        "grandezza su campioni limitati, non misurazioni pubblicate con",
        "intervallo di confidenza. Nessuna combinazione di questi numeri",
        "stabilisce se un testo sia stato generato da una macchina, e usarli",
        "in quel modo sarebbe l'errore che la skill contesta ai detector",
        "automatici.",
        "",
        "## File letti",
        "",
    ]
    fuori += tabella(
        ["File", "Parole", "Frasi", "Paragrafi", "Separazione", "Codifica"],
        [
            [
                voce["file"],
                voce["parole"],
                voce["frasi"],
                voce["paragrafi"],
                voce["separazione_paragrafi"],
                voce["codifica"],
            ]
            for voce in corpus["file"]
        ],
    )
    fuori += [
        "La colonna «separazione» dice come il file divide i paragrafi. Il",
        "riconoscimento e automatico: applicare la regola sbagliata farebbe",
        "misurare il formato del file al posto della voce.",
        "",
    ]

    esclusioni = corpus["esclusioni_in_pulizia"]
    if esclusioni:
        fuori += ["## Escluso in pulizia", ""]
        fuori += tabella(
            ["Elemento", "Quantita"],
            [
                [chiave.replace("_", " "), valore]
                for chiave, valore in sorted(esclusioni.items())
            ],
        )

    fuori += [
        "## Limiti dichiarati",
        "",
        "1. Non analizza la sintassi: nessun conteggio di subordinate, nessun",
        "   rapporto fra paratassi e ipotassi.",
        "2. Non ha un dizionario: non riduce le parole alla forma base, non",
        "   distingue gli omografi, non riconosce i nomi propri.",
        "3. Non capisce il senso: ironia, citazioni e discorso riportato",
        "   contano come testo qualunque.",
        "4. Non giudica la qualita: un testo pessimo e uno ottimo possono",
        "   avere lo stesso profilo.",
        "5. Non e un rilevatore di AI e non serve a ingannarne uno.",
        "6. Descrive un corpus, non una persona.",
        "",
    ]
    return "\n".join(fuori)


# --------------------------------------------------------------------------
# Riga di comando
# --------------------------------------------------------------------------


def costruisci_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description=(
            "Calcola il profilo quantitativo di una voce autoriale a partire "
            "da una cartella di testi italiani dello stesso autore e dello "
            "stesso registro."
        ),
        epilog=(
            "Esempio: python profilo_voce.py ./miei-articoli "
            '--nome "Nome Cognome"'
        ),
    )
    parser.add_argument("corpus", help="cartella contenente i testi (.txt o .md)")
    parser.add_argument(
        "--out",
        help="cartella dove scrivere scheda-voce.md e profilo-voce.json",
    )
    parser.add_argument("--nome", help="nome dell'autore, usato nel titolo")
    parser.add_argument(
        "--versione", action="version", version="profilo_voce.py " + VERSIONE
    )
    return parser


def main(argomenti: Optional[Sequence[str]] = None) -> int:
    opzioni = costruisci_parser().parse_args(argomenti)
    cartella = Path(opzioni.corpus).expanduser()
    uscita = Path(opzioni.out).expanduser() if opzioni.out else cartella

    try:
        profilo = calcola_profilo(cartella, opzioni.nome)
    except ErroreCorpus as errore:
        print("Errore: {}".format(errore), file=sys.stderr)
        return 2

    try:
        uscita.mkdir(parents=True, exist_ok=True)
        percorso_scheda = uscita / "scheda-voce.md"
        percorso_dati = uscita / "profilo-voce.json"
        percorso_scheda.write_text(scrivi_scheda(profilo), encoding="utf-8")
        percorso_dati.write_text(
            json.dumps(profilo, ensure_ascii=False, indent=2), encoding="utf-8"
        )
    except OSError as errore:
        print("Errore di scrittura: {}".format(errore), file=sys.stderr)
        return 2

    corpus = profilo["corpus"]
    print(
        "Profilo calcolato su {} file, {} parole, {} frasi. Affidabilita: {}.".format(
            corpus["file_letti"],
            corpus["parole_totali"],
            corpus["frasi_totali"],
            corpus["affidabilita"],
        )
    )
    print("Scheda: {}".format(percorso_scheda))
    print("Dati:   {}".format(percorso_dati))
    return 0


if __name__ == "__main__":
    sys.exit(main())

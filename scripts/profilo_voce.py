#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Calcola il profilo quantitativo di una voce autoriale su un corpus italiano.

Fa parte della skill italiano-scrittura-anti-ai. Legge una cartella di testi
scritti dalla stessa persona nello stesso registro e produce due file: una
scheda leggibile e i dati grezzi in formato JSON.

    python profilo_voce.py CARTELLA [--out CARTELLA] [--nome "Nome autore"]

Non usa librerie esterne, non accede alla rete, non modifica i file del
corpus e non scrive nulla fuori dalla cartella di uscita.

Le decisioni di conteggio (cosa è una frase, cosa è una parola, cosa viene
escluso) sono descritte nel reference della skill come riferimento
indicativo: chi rifà i conti a mano arriva agli stessi ordini di grandezza,
non alla stessa cifra. Le regole esatte, con le liste chiuse e le soglie,
stanno qui nel codice, che resta la fonte.

Questo strumento misura. Non giudica, non riscrive, non stabilisce se un
testo sia stato generato da una macchina.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import statistics
import sys
import unicodedata
from collections import Counter
from pathlib import Path
from typing import Dict, Iterable, List, Optional, Sequence, Tuple

VERSIONE = "1.4.0"
SOGLIA_PAROLE_AFFIDABILE = 2000
FINESTRA_MATTR = 50
FINESTRA_TTR_CONFRONTO = 1000
PAROLE_MINIME_BLOCCO_GULPEASE = 100
MAX_PAROLE_TITOLO = 15

# Sotto questa quota di righe vuote il file non usa la riga bianca per
# separare i paragrafi: lo fa con il ritorno a capo singolo, come in molti
# testi salvati da un elaboratore di testi. Cercare le righe bianche in un
# file così impasterebbe decine di paragrafi in un blocco solo, e la misura
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

# Parole vuote: escluse dal conteggio delle parole più frequenti (6.7).
# Restano invece dentro gli n-grammi, perché i tic autentici sono spesso
# fatti proprio di parole vuote (*il tuo utente*, *è compito del*).
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

# Connettivi contati a parte (6.7): sono il marcatore più citato
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

# Nomi dei file che questo strumento scrive. Vengono esclusi dal corpus:
# senza --out l'uscita finisce accanto ai testi, e al lancio successivo la
# scheda verrebbe riletta come se fosse prosa dell'autore.
NOMI_DI_USCITA = frozenset({"scheda-voce.md", "profilo-voce.json"})

# Estensioni dei file che formano il corpus. Il confronto avviene sul nome
# ridotto a minuscole, perché su Linux e macOS il glob distingue le maiuscole
# e un «appunti.TXT» resterebbe fuori senza che nessuno lo dichiari.
ESTENSIONI_DEL_CORPUS = (".txt", ".md", ".markdown")

# Firma con cui lo strumento riconosce i propri file. Senza --out l'uscita
# finisce nella cartella del corpus, e un file che l'utente avesse chiamato
# «scheda-voce.md» o «profilo-voce.json» verrebbe sovrascritto senza
# preavviso. La firma compare in testa a entrambe le uscite (prima riga della
# scheda, prima chiave del JSON): al lancio successivo lo strumento sovrascrive
# solo i file che la portano in quella posizione, e si ferma davanti a quelli
# che non riconosce. Cercarla come semplice sottostringa non basterebbe: un
# documento dell'utente che si limita a citarla più in basso non è una nostra
# uscita e non va toccato.
FIRMA = (
    "profilo-voce: file generato da profilo_voce.py e riscritto a ogni "
    "esecuzione; non modificarlo a mano, le modifiche vanno perse"
)

# Oltre questa soglia il corpus viene comunque elaborato, ma con un avviso:
# l'occupazione di memoria cresce di circa venticinque volte la dimensione
# del testo, e su una macchina comune un corpus molto grande la esaurisce.
BYTE_CON_AVVISO = 20 * 1024 * 1024

# I segni che chiudono una citazione o un inciso. Un terminatore di frase che
# li precede chiude comunque la frase: «basta.» e "basta." mettono il punto
# dentro le virgolette, e senza oltrepassare il segno la frase si fonderebbe
# con la successiva. Nessun segno di apertura entra qui: dopo un punto può
# stare solo un segno che chiude.
SEGNI_DI_CHIUSURA = frozenset("»)]\"'" + "”’")

# I segni che possono avvolgere una parola. Servono a isolare la parola nuda
# quando si controlla se un punto appartiene a un'abbreviazione: «sig.», "B.",
# "sig." vanno ridotti a *sig* o *B*. Coprono ogni segno di SEGNI_DI_CHIUSURA
# più i corrispettivi di apertura, così il controllo resta coerente con chi
# stabilisce il confine della frase, in ogni stile di virgolettatura.
SEGNI_ATTORNO_PAROLA = "«»“”‘’()[]\"'"


def confronto(forma: str) -> str:
    """Forma con cui una parola si confronta con le liste chiuse.

    Toglie gli accenti e l'apostrofo finale, e serve soltanto a stabilire se
    una parola appartiene a una lista chiusa (parole vuote, connettivi): il suo
    risultato non compare mai nella scheda. La forma mostrata nelle ricorrenze
    la decide `forma_lessicale`, che minuscola e stacca l'elisione iniziale,
    quindi lì una parola può apparire diversa da come l'autore l'ha scritta.

    Senza questo passaggio *perche'* dell'elenco non corrisponderebbe a
    *perché* del testo, e le liste riconoscerebbero soltanto la forma senza
    accento. Il risultato sarebbe il rovescio di quello che serve: un testo
    scritto con gli accenti giusti verrebbe misurato peggio di uno scritto
    male, perché le sue congiunzioni e le sue parole vuote resterebbero
    invisibili al conteggio.
    """
    decomposta = unicodedata.normalize("NFD", forma)
    piana = "".join(
        carattere for carattere in decomposta if not unicodedata.combining(carattere)
    )
    return unicodedata.normalize("NFC", piana).rstrip("'")


PAROLE_VUOTE_CONFRONTO = frozenset(confronto(parola) for parola in PAROLE_VUOTE)
CONNETTIVI_CONFRONTO = frozenset(confronto(parola) for parola in CONNETTIVI)

# Intervalli citati in references/metodologie-operative.md sezione 6.
# Quella sezione dichiara di sé stessa che sono stime indicative, ordini di
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
        "etichetta": "Varietà lessicale su finestre di mille parole",
        "umano": (0.52, 0.62),
        "confronto_ai": "GPT 0,40-0,48",
        "cautela": (
            "misura che non discrimina da sola. Un corpus tematicamente "
            "ristretto ripete il lessico del suo campo e scende sotto "
            "l'intervallo per ragioni di argomento, non di autore. Nel "
            "collaudo di questo strumento un testo generato ha ottenuto "
            "varietà più alta di un testo umano, perché la prosa burocratica "
            "evita la ripetizione con la variazione elegante, che è a sua "
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
        "etichetta": "Densità di connettivi sul totale delle parole",
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
# Le lunghezze massime dei tratti (parte locale ed etichette del dominio) tengono
# la ricerca lineare: senza un tetto, una catena lunga di caratteri ammessi ma
# senza chiocciola faceva ripartire il motore da ogni confine di parola e il
# tempo cresceva col quadrato. I tetti sono generosi, ben oltre ogni indirizzo
# reale (RFC ferma la parte locale a 64), così anche un indirizzo lungo viene
# comunque rimosso: solo una catena assurda, oltre 256 caratteri filati, resta
# nel testo. Un tetto qualunque, purché finito, basta a togliere il quadratico.
RE_EMAIL = re.compile(r"\b[\w.+-]{1,256}@[\w-]{1,255}(?:\.[\w-]{1,255})+\b")
RE_MARCATORE_H = re.compile(r"\(\s*h\s*[1-6]\s*\)", re.IGNORECASE)
RE_MARCATORE_IMG = re.compile(
    r"^\s*(?:img\b.*|\[img[^\]]*\]|immagine di esempio.*)$", re.IGNORECASE
)
RE_TITOLO_MD = re.compile(r"^\s*#{1,6}\s+")
RE_ELENCO = re.compile(r"^\s*(?:[-*•·–]+|\d+[.)]|[a-z][.)])\s+")
# La citazione Markdown apre con uno o più segni di maggiore. Il contenuto è
# prosa e va contato; il marcatore è impaginazione e si toglie, anche quando
# più righe della stessa citazione sono state rimesse insieme.
RE_CITAZIONE = re.compile(r"^\s*>+\s*")
RE_MARCATORE_CITAZIONE = re.compile(r"(?:^|(?<=\s))>+\s*")
# Il numero iniziale di una possibile voce di elenco, per distinguere «1.»
# (elenco) da «2023.» (un anno, cioè prosa che comincia con una data).
RE_NUMERO_ELENCO = re.compile(r"^\s*(\d+)[.)]")
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


# I contrassegni iniziali (BOM), dal più lungo al più corto: quello UTF-16
# little endian (FF FE) è il prefisso di quello UTF-32 little endian
# (FF FE 00 00), quindi l'UTF-32 va provato prima o verrebbe frainteso.
CONTRASSEGNI = (
    (b"\x00\x00\xfe\xff", "utf-32"),
    (b"\xff\xfe\x00\x00", "utf-32"),
    (b"\xef\xbb\xbf", "utf-8-sig"),
    (b"\xff\xfe", "utf-16"),
    (b"\xfe\xff", "utf-16"),
)


def leggi_file(percorso: Path) -> Tuple[str, str]:
    """Legge un file di testo e restituisce contenuto e codifica usata.

    Il contrassegno iniziale (BOM), se c'è, decide la codifica: quello UTF-8
    dà «utf-8-sig», quelli UTF-16 e UTF-32 fanno leggere il file in quella
    codifica, nelle due direzioni. I contrassegni si provano dal più lungo,
    perché quello UTF-16 little endian è il prefisso di quello UTF-32. Un file
    che porta un contrassegno ma non decodifica è corrotto e viene escluso con
    ErroreCorpus, come il resto della lettura, invece di fermare tutto il
    corpus.

    Senza contrassegno si tenta prima UTF-8 e poi cp1252, la codifica dei file
    di testo salvati su Windows.

    Prima questa funzione tentava «utf-8-sig» per primo su ogni file: un file
    senza BOM veniva comunque etichettato «utf-8-sig», e un file UTF-16 con
    BOM, che UTF-8 rifiuta, scivolava su cp1252 e diventava mojibake pieno di
    byte nulli, con le parole moltiplicate e nessun avviso. Una codifica
    sbagliata rovina accenti e apostrofi, e quindi i conteggi: per questo la
    codifica effettiva finisce nel rapporto.

    Il riconoscimento si fonda sul solo contrassegno, non sui byte nulli, per
    non prendere per Unicode un testo latino con molti spazi. Il costo, raro e
    accettato, è che un file di un'altra codifica che cominci per caso con
    quei byte (per esempio «ÿþ» in cp1252) verrebbe frainteso: un inizio così
    non ricorre nella prosa italiana.
    """
    dati = percorso.read_bytes()
    for firma, codifica in CONTRASSEGNI:
        if dati.startswith(firma):
            try:
                return dati.decode(codifica), codifica
            except UnicodeDecodeError:
                raise ErroreCorpus(
                    "Il file {} porta un contrassegno {} ma un contenuto "
                    "non valido.".format(percorso.name, codifica)
                )
    for codifica in ("utf-8", "cp1252"):
        try:
            return dati.decode(codifica), codifica
        except UnicodeDecodeError:
            continue
    raise ErroreCorpus(
        "Il file {} non è leggibile né in UTF-8 né in cp1252.".format(percorso.name)
    )


def cartella_da_scendere(
    candidata: Path, radice: Path, viste: set
) -> Tuple[bool, str]:
    """Decide se scendere in una sottocartella del corpus, e perché no.

    Quattro motivi la tengono fuori, e ognuno ha il proprio nome nelle
    esclusioni della scheda: un collegamento simbolico a directory, un
    percorso che non si lascia risolvere, un percorso che porta fuori dalla
    cartella indicata (una giunzione, per esempio), e un percorso già
    percorso, che è la forma che prende un ciclo. Le cartelle viste si
    accumulano nell'insieme ricevuto, che la funzione aggiorna quando la
    risposta è sì.

    Il collegamento simbolico si riconosce per primo, e non entra fra le
    cartelle viste. Prenderne nota farebbe potare più tardi la cartella vera
    a cui rimanda, che risulterebbe già percorsa e sparirebbe dal corpus con
    tutti i suoi file: un collegamento chiamato `a-testi` che rimanda a
    `testi` basta a far sparire `testi`, perché la scansione procede in
    ordine alfabetico e nel collegamento non si scende mai.
    """
    try:
        if candidata.is_symlink():
            return False, "cartelle_collegate"
    except OSError:
        return False, "cartelle_non_risolvibili"
    try:
        risolta = candidata.resolve()
    except OSError:
        return False, "cartelle_non_risolvibili"
    if risolta != radice and radice not in risolta.parents:
        return False, "cartelle_fuori_dalla_cartella"
    if risolta in viste:
        return False, "cartelle_gia_percorse"
    viste.add(risolta)
    return True, ""


def raccogli_file(cartella: Path, esclusioni: Optional[Counter] = None) -> List[Path]:
    """Elenca i file di testo del corpus, in ordine deterministico.

    Due cose vengono tenute fuori, e ognuna conta come esclusione dichiarata
    nella scheda invece che sparire in silenzio.

    La prima sono i due file che questo strumento scrive. Senza `--out`
    finiscono accanto ai testi, e al lancio successivo la scheda verrebbe
    letta come prosa dell'autore.

    La seconda è tutto ciò che sta fuori dalla cartella indicata. Un
    collegamento simbolico o una giunzione dentro il corpus porterebbe
    altrove, e un profilo che misura anche file di cui l'utente non sa
    niente non misura la sua voce. Il controllo vale per i file e anche per
    le cartelle: una discesa affidata a `rglob` seguiva i collegamenti fra
    directory senza riconoscere i cicli, e su Python fino al 3.12 una catena
    che torna su sé stessa faceva morire il processo per ricorsione, mentre
    dal 3.13 le stesse cartelle sparivano senza comparire fra le esclusioni.

    L'estensione si riconosce a minuscole: su un filesystem che distingue le
    maiuscole un `appunti.TXT` restava fuori dal corpus e da ogni conteggio.
    """
    if not cartella.exists():
        raise ErroreCorpus("La cartella {} non esiste.".format(cartella))
    if not cartella.is_dir():
        raise ErroreCorpus("{} non è una cartella.".format(cartella))
    conta = esclusioni if esclusioni is not None else Counter()
    radice = cartella.resolve()
    trovati: List[Path] = []
    cartelle_viste = {radice}
    def cartella_illeggibile(errore: OSError) -> None:
        # Senza questa funzione `os.walk` inghiotte in silenzio l'errore di
        # una cartella che esiste ma non si lascia leggere (permessi negati),
        # e i suoi file sparirebbero senza comparire fra le esclusioni.
        conta["cartelle_illeggibili"] += 1

    # `os.walk` non scende nei collegamenti simbolici a directory, quindi il
    # ciclo non può ripartire da capo; le cartelle che porterebbero fuori o
    # che sono già state percorse si tolgono qui e diventano un'esclusione
    # dichiarata invece di sparire in silenzio.
    for cartella_corrente, sottocartelle, nomi in os.walk(
        cartella, followlinks=False, onerror=cartella_illeggibile
    ):
        qui = Path(cartella_corrente)
        restano: List[str] = []
        for nome in sorted(sottocartelle):
            scendere, motivo = cartella_da_scendere(qui / nome, radice, cartelle_viste)
            if scendere:
                restano.append(nome)
            else:
                conta[motivo] += 1
        sottocartelle[:] = restano
        for nome in nomi:
            if nome.lower().endswith(ESTENSIONI_DEL_CORPUS):
                trovati.append(qui / nome)
    dentro: List[Path] = []
    impronte_viste: set = set()
    for percorso in sorted(set(trovati)):
        # Il confronto è a minuscole: su un filesystem che non distingue le
        # maiuscole un file «Scheda-Voce.md» è la stessa uscita di
        # «scheda-voce.md» e va escluso lo stesso.
        if percorso.name.lower() in NOMI_DI_USCITA:
            conta["uscite_dello_strumento"] += 1
            continue
        try:
            risolto = percorso.resolve()
        except OSError:
            conta["file_non_risolvibili"] += 1
            continue
        if risolto != radice and radice not in risolto.parents:
            conta["file_fuori_dalla_cartella"] += 1
            continue
        # Due nomi diversi possono portare allo stesso file: un collegamento
        # simbolico o una giunzione interni al corpus, oppure un hard link.
        # Letti entrambi, quel file conterebbe due volte. L'identità del file
        # (dispositivo più numero di inode) lo riconosce; dove il filesystem
        # non dà un inode utile (vale zero), si ripiega sul percorso risolto,
        # che coglie comunque i collegamenti simbolici ma non gli hard link.
        try:
            info = risolto.stat()
            impronta = (
                (info.st_dev, info.st_ino)
                if info.st_ino
                else ("percorso", str(risolto))
            )
        except OSError:
            impronta = ("percorso", str(risolto))
        if impronta in impronte_viste:
            conta["doppioni_del_corpus"] += 1
            continue
        impronte_viste.add(impronta)
        dentro.append(percorso)
    return dentro


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
    """Toglie ciò che non è prosa d'autore, contando ogni rimozione."""
    # Le parentesi vuote si contano sul testo originale, prima delle altre
    # rimozioni: togliere un indirizzo fra parentesi, «(mario@x.it)», lascia
    # «( )», che non era una parentesi vuota dell'autore e non va contata come
    # tale. La rimozione avviene invece in coda, così ripulisce anche quei resti.
    esclusioni["parentesi_vuote"] += len(RE_PARENTESI_VUOTE.findall(testo))
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


def apre_elenco(riga: str) -> bool:
    """Vero se la riga è davvero una voce di elenco.

    Un numero grande a inizio riga, come un anno («2023. L'anno in cui...»),
    somiglia a una voce numerata ma è prosa che comincia con una data. Da mille
    in su non lo si tratta da elenco, o quella riga sparirebbe dai conteggi come
    un titolo, mentre un elenco vero si ferma a numeri ben più piccoli.
    """
    if not RE_ELENCO.match(riga):
        return False
    numero_iniziale = RE_NUMERO_ELENCO.match(riga)
    if numero_iniziale:
        # Il confronto è per numero di cifre, non con int(): da mille in su
        # servono almeno quattro cifre significative. Una riga che comincia con
        # migliaia di cifre farebbe sollevare a int() un ValueError (il limite
        # di Python 3.12 sulle conversioni lunghe), fermando l'intero corpus.
        cifre = numero_iniziale.group(1).lstrip("0")
        if len(cifre) >= 4:
            return False
    return True


def ha_parole(testo: str) -> bool:
    """Vero se il testo contiene almeno una parola con una lettera.

    Serve a tenere fuori dai paragrafi le frasi fatte di sola punteggiatura,
    come una riga di soli puntini: senza parole non sono frasi, e contate come
    tali gonfierebbero il numeratore del Gulpease e il conteggio delle frasi.
    """
    return any(contiene_lettera(token) for token in RE_PAROLA.findall(testo))


def spoglia_segni_di_chiusura(testo: str) -> str:
    """Toglie da destra i segni che chiudono una citazione, mai il terminatore.

    Il discorso diretto italiano si scrive fra caporali, e una battuta finisce
    con il caporale, non con il punto interrogativo: l'ultimo carattere di
    «Che ore sono?» è il caporale. Ogni regola che guarda l'ultimo carattere
    per decidere se una riga o una frase ha chiuso deve prima togliere quei
    segni, o la battuta risulta priva di terminatore: è la causa comune di tre
    difetti diversi, dalla domanda del dialogo che non entrava nei conteggi
    alla riga di dialogo scambiata per un titolo.

    Si tolgono anche gli spazi, così una riga che finisce con uno spazio dopo
    le virgolette si comporta come quella che non ce l'ha. Il taglio si fa per
    indice e non affettando la stringa a ogni giro: ricopiarla ogni volta
    rendeva quadratico il tempo su una riga fatta di molti segni di chiusura.
    """
    fine = len(testo)
    while fine > 0 and (testo[fine - 1] in SEGNI_DI_CHIUSURA or testo[fine - 1].isspace()):
        fine -= 1
    return testo[:fine]


def unisci_righe_dello_stesso_blocco(righe: Sequence[str]) -> List[str]:
    """Rimette insieme le righe che l'impaginazione ha spezzato.

    Un file di testo scritto a mano, o esportato senza reflow, manda a capo
    la prosa a una larghezza fissa. Ogni riga così prodotta finisce senza
    punteggiatura forte e sta sotto le quindici parole, cioè si presenta
    esattamente come un titolo: senza questo passaggio la prosa sparirebbe
    dai conteggi in silenzio. Un titolo vero è invece una riga isolata fra
    righe vuote, e da questo passaggio esce intatta.

    Un titolo Markdown non si unisce mai a ciò che segue: lì il ritorno a capo
    è struttura del documento, non impaginazione. Una voce di elenco e una
    citazione invece proseguono, perché anche loro vengono mandate a capo:
    una voce chiusa a forza lasciava orfana la propria continuazione, che
    finiva fra i titoli e usciva dai conteggi. Proseguono però solo su una
    riga il cui primo carattere alfabetico non è maiuscolo, il segno che
    quella riga continua una frase invece di aprirne una: senza questo confine
    un paragrafo scritto sotto un elenco, senza riga bianca in mezzo, veniva
    inghiottito dall'ultima voce, e due frasi diventavano una sola. Il primo
    carattere alfabetico, e non il primo carattere: una riga che apre con una
    cifra, una parentesi o un caporale non è né maiuscola né minuscola, e
    guardando il solo primo carattere veniva inghiottita comunque.

    Il criterio ha tre limiti dichiarati, e sono il prezzo di questo confine.
    Una continuazione legittima che apre con un nome proprio dietro un segno,
    come «Roma» dopo una voce che finisce per «andammo a», viene lasciata
    dov'è: la maiuscola non distingue il nome proprio dall'inizio di frase.
    Una riga senza alcun carattere alfabetico, come un separatore di soli
    trattini, vale come continuazione e si unisce alla voce. Negli alfabeti
    senza distinzione di maiuscola e minuscola, come il giapponese e
    l'ebraico, il criterio non discrimina e ogni riga vale come
    continuazione.

    Le righe si accumulano in una lista e si uniscono una volta sola alla
    chiusura del blocco. Concatenare la stringa a ogni riga la ricopiava per
    intero ogni volta, e su un blocco senza terminatori il tempo cresceva più
    che al quadrato: 160.000 righe costavano sette volte 80.000, non due.
    """

    def apre_un_blocco(riga: str) -> bool:
        return bool(
            RE_TITOLO_MD.match(riga)
            or RE_MARCATORE_IMG.match(riga)
            or apre_elenco(riga)
            or RE_CITAZIONE.match(riga)
        )

    def apre_una_frase_nuova(riga: str) -> bool:
        """Vero se la riga comincia una frase invece di continuarne una."""
        for carattere in riga:
            if carattere.isalpha():
                return carattere.isupper()
        return False

    def chiude(riga: str, prossima: str) -> bool:
        coda = spoglia_segni_di_chiusura(riga)
        if coda and coda[-1] in ".!?…:":
            return True
        if RE_TITOLO_MD.match(riga) or RE_MARCATORE_IMG.match(riga):
            return True
        if not prossima:
            return True
        if RE_CITAZIONE.match(riga) and RE_CITAZIONE.match(prossima):
            # Due righe di citazione di seguito sono lo stesso blocco: a
            # separarne due è la riga di solo marcatore, che a questo punto
            # è già diventata una riga vuota.
            return False
        if apre_elenco(riga) or RE_CITAZIONE.match(riga):
            # La continuazione di una voce o di una citazione non comincia con
            # una maiuscola. Il confronto guarda il primo carattere alfabetico
            # e non il primo carattere: davanti alla maiuscola possono esserci
            # una cifra, una parentesi o un caporale, e guardando solo il primo
            # carattere un paragrafo nuovo passava per continuazione.
            return apre_un_blocco(prossima) or apre_una_frase_nuova(prossima)
        return apre_un_blocco(prossima)

    fuori: List[str] = []
    pezzi: List[str] = []
    for indice, riga in enumerate(righe):
        if not riga:
            if pezzi:
                fuori.append(" ".join(pezzi))
                pezzi = []
            fuori.append("")
            continue
        pezzi.append(riga)
        prossima = righe[indice + 1] if indice + 1 < len(righe) else ""
        if chiude(riga, prossima):
            fuori.append(" ".join(pezzi))
            pezzi = []
    if pezzi:
        fuori.append(" ".join(pezzi))
    return fuori


def classifica_righe(testo: str, esclusioni: Counter) -> List[Tuple[str, str]]:
    """Etichetta ogni riga come vuota, titolo, elenco o prosa.

    Regole dichiarate:
    - le righe che l'impaginazione ha spezzato vengono prima rimesse insieme,
      così un a capo a larghezza fissa non passa per una sequenza di titoli;
    - una riga che inizia con marcatore Markdown o con (h1)...(h6) è titolo;
    - una riga che inizia con trattino, asterisco o numero puntato è elenco;
    - una riga che inizia con il segno di maggiore è una citazione: il
      marcatore se ne va e il testo conta come prosa, anche quando è breve;
    - una riga che non finisce con punteggiatura forte o due punti e ha meno
      di quindici parole è titolo, e non entra nei conteggi; il terminatore si
      cerca sotto i segni che chiudono una citazione, o una battuta di dialogo
      come «Che ore sono?» risulterebbe senza punteggiatura; il rovescio è che
      un titolo breve che chiude con una citazione interrogativa, come
      «Il problema "Che fare?"», conta ora come prosa: la stessa regola non
      può salvare la battuta e insieme escludere quel titolo;
    - tutto il resto è prosa.
    I blocchi di codice e il frontmatter vengono saltati per interi.
    """
    utili: List[str] = []
    buffer_frontmatter: List[str] = []
    dentro_codice = False
    dentro_frontmatter = False
    apertura_frontmatter_possibile = True
    # Si toglie solo l'ultimo ritorno a capo, quello che quasi ogni editor
    # lascia in fondo al file: contato come riga vuota falserebbe la quota che
    # decide come il file separa i paragrafi. Le altre righe vuote finali, che
    # possono essere volute, restano: un rstrip di tutti gli a capo le
    # azzererebbe in blocco.
    testo_corpo = testo[:-1] if testo.endswith(chr(10)) else testo
    for riga_grezza in testo_corpo.split(chr(10)):
        riga = RE_SPAZI.sub(" ", riga_grezza).strip()

        if riga.startswith("```") or riga.startswith("~~~"):
            apertura_frontmatter_possibile = False
            dentro_codice = not dentro_codice
            esclusioni["righe_di_codice"] += 1
            continue
        if dentro_codice:
            esclusioni["righe_di_codice"] += 1
            continue

        # Il frontmatter apre con --- solo se prima non è comparsa alcuna riga
        # di contenuto (le sole righe vuote iniziali non contano), e chiude con
        # --- oppure con ..., le due forme che YAML ammette. Le righe restano in
        # un buffer finché il blocco non si chiude: se non si chiude mai (un ---
        # decorativo, un file troncato) non era frontmatter, e il buffer torna
        # fra le righe utili invece di far sparire il documento come metadati.
        if not dentro_frontmatter and apertura_frontmatter_possibile and riga == "---":
            dentro_frontmatter = True
            buffer_frontmatter.append(riga)
            continue
        if dentro_frontmatter:
            buffer_frontmatter.append(riga)
            if riga == "---" or riga == "...":
                esclusioni["righe_di_metadati"] += len(buffer_frontmatter)
                buffer_frontmatter.clear()
                dentro_frontmatter = False
            continue

        if riga:
            apertura_frontmatter_possibile = False
        # Una riga fatta del solo marcatore di citazione separa due paragrafi
        # citati: è la forma che il Markdown usa al posto della riga bianca
        # dentro una citazione. Trattarla come contenuto la faceva sparire
        # nell'unione, e i due paragrafi diventavano uno solo.
        if riga and RE_CITAZIONE.fullmatch(riga):
            riga = ""
        utili.append(riga)

    # Un blocco aperto con --- ma mai chiuso non era frontmatter: le sue righe
    # sono contenuto e vanno classificate, non contate fra i metadati.
    utili.extend(buffer_frontmatter)

    righe: List[Tuple[str, str]] = []
    tipo_precedente = "vuota"
    for riga in unisci_righe_dello_stesso_blocco(utili):
        if not riga:
            righe.append(("vuota", ""))
            tipo_precedente = "vuota"
            continue

        # Una citazione è prosa: il marcatore si toglie e la riga non passa
        # dalla regola del titolo implicito, o una citazione breve («> La
        # tesi centrale», sotto le quindici parole e senza punto finale)
        # uscirebbe dai conteggi come se fosse un'intestazione. Il marcatore
        # si toglie anche in mezzo, dove più righe della stessa citazione
        # sono state rimesse insieme; un segno di maggiore usato come simbolo
        # dentro una citazione se ne va con loro, ed è il limite dichiarato.
        citazione = bool(RE_CITAZIONE.match(riga))
        if citazione:
            riga = RE_SPAZI.sub(" ", RE_MARCATORE_CITAZIONE.sub(" ", riga)).strip()
            if not riga:
                # Una citazione che si svuota vale come riga vuota anche per
                # la riga dopo: senza azzerare il tipo precedente, lo stesso
                # documento cambiava classificazione secondo come era scritto
                # il separatore, e un titolo dopo «> >» diventava prosa.
                righe.append(("vuota", ""))
                tipo_precedente = "vuota"
                continue

        if RE_TITOLO_MD.match(riga) or RE_MARCATORE_IMG.match(riga):
            esclusioni["titoli_e_marcatori"] += 1
            righe.append(("titolo", riga))
            tipo_precedente = "titolo"
            continue

        if apre_elenco(riga):
            righe.append(("elenco", RE_ELENCO.sub("", riga, count=1).strip()))
            tipo_precedente = "elenco"
            continue

        # La riga che segue subito una voce di elenco o una citazione, senza
        # riga bianca in mezzo, è il paragrafo che quel blocco si tira dietro:
        # corta o no, resta prosa. Applicarle la regola del titolo implicito
        # la farebbe sparire dai conteggi proprio dove il blocco sopra ha
        # appena rifiutato di inglobarla.
        # Il terminatore si cerca dopo aver tolto i segni che chiudono una
        # citazione: una battuta di dialogo finisce con il caporale, e
        # guardando l'ultimo carattere letterale risultava senza punteggiatura
        # forte. Ogni battuta isolata usciva così dai conteggi come titolo, e
        # un corpus di sola narrativa dialogata veniva rifiutato per intero
        # con un messaggio falso.
        coda_della_riga = spoglia_segni_di_chiusura(riga)
        if (
            not citazione
            and tipo_precedente not in ("elenco", "citazione")
            and (not coda_della_riga or coda_della_riga[-1] not in ".!?…:")
            and conta_parole_grezze(riga) < MAX_PAROLE_TITOLO
        ):
            esclusioni["titoli_e_marcatori"] += 1
            righe.append(("titolo", riga))
            tipo_precedente = "titolo"
            continue

        righe.append(("prosa", riga))
        tipo_precedente = "citazione" if citazione else "prosa"
    return righe


def dividi_in_frasi(testo: str) -> List[str]:
    """Divide un blocco di prosa in frasi secondo le regole dichiarate.

    Chiudono la frase il punto, il punto esclamativo, il punto interrogativo
    e i puntini di sospensione, quando sono seguiti da spazio o fine testo e
    la parola successiva non comincia per minuscola. Il terminatore chiude
    anche quando sta dentro le virgolette che chiudono una citazione, come
    in «basta.» o "basta.". Non chiudono i due punti, il punto e virgola, il
    punto delle abbreviazioni note, il punto fra cifre e il punto di
    un'iniziale puntata.

    La ricerca lavora per indici e non per fette di stringa: né la parola
    che precede il punto né il testo che segue vengono copiati per intero.
    Copiarli a ogni terminatore rendeva quadratico il tempo su un paragrafo
    lungo senza a capo, un formato comune per il testo estratto da un PDF o
    incollato da una pagina web.
    """
    frasi: List[str] = []
    inizio = 0
    n = len(testo)
    for confine in RE_TERMINATORE.finditer(testo):
        fine = confine.end()

        # Si oltrepassano i segni che chiudono una citazione, così il punto
        # interno alle virgolette chiude la frase come quello esterno.
        while fine < n and testo[fine] in SEGNI_DI_CHIUSURA:
            fine += 1

        if fine < n and not testo[fine].isspace():
            continue

        if confine.group() == ".":
            # L'ultima parola prima del punto, cercata a ritroso fino allo
            # spazio precedente invece di copiare tutto ciò che sta prima. Si
            # ferma su qualunque spazio, non sul solo spazio ASCII: un testo
            # che usa lo spazio sottile, quello stretto o quello ideografico
            # non ne offriva nessuno, la scansione tornava fino all'inizio del
            # testo a ogni punto e il tempo cresceva al quadrato.
            avvio = confine.start()
            while avvio > 0 and not testo[avvio - 1].isspace():
                avvio -= 1
            nudo = testo[avvio : confine.start()].strip(SEGNI_ATTORNO_PAROLA).lower()
            if nudo in ABBREVIAZIONI:
                continue
            if len(nudo) == 1 and nudo.isalpha():
                continue

        # La prima lettera dopo il confine, cercata in avanti saltando gli
        # spazi invece di copiare e ripulire tutto il resto del testo.
        successivo = fine
        while successivo < n and testo[successivo].isspace():
            successivo += 1
        if successivo < n and testo[successivo].isalpha() and testo[successivo].islower():
            continue

        frase = testo[inizio:fine].strip()
        if frase:
            frasi.append(frase)
        inizio = fine

    coda = testo[inizio:].strip()
    if coda:
        frasi.append(coda)
    return frasi


def chiude_con(frase: str, terminatore: str) -> bool:
    """Vero se la frase chiude con quel terminatore, virgolette comprese.

    Il discorso diretto italiano si scrive fra caporali, e `dividi_in_frasi`
    tiene dentro la frase i segni che chiudono la citazione: «Che ore sono?»
    finisce con il caporale, non con il punto interrogativo. Cercare il
    terminatore sull'ultimo carattere faceva sparire dai conteggi ogni domanda
    e ogni esclamazione del dialogo, cioè proprio dove sono più frequenti, e
    le due quote uscivano a zero senza che niente lo segnalasse.

    Si tolgono da destra i soli segni di chiusura, mai il terminatore: una
    frase che finisce con un punto dentro le virgolette, «basta.», resta
    affermativa, e una che non ha terminatore, «Ciao», non diventa nulla di
    diverso da quello che è.

    Un terminatore isolato fra parentesi, come in «Forse piove [?]» o «Che
    sorpresa (!)», è un segno editoriale di chi trascrive, non una domanda o
    un'esclamazione di chi scrive: si riconosce dall'apertura che lo precede
    e non entra nel conteggio.
    """
    coda = spoglia_segni_di_chiusura(frase)
    if not coda.endswith(terminatore):
        return False
    return not coda[: -len(terminatore)].rstrip().endswith(("(", "[", "{"))


def righe_vuote_separano_i_paragrafi(righe: Sequence[Tuple[str, str]]) -> bool:
    """Rileva come il file separa i paragrafi.

    Un file Markdown lascia una riga bianca fra un paragrafo e l'altro. Un
    testo salvato da un elaboratore di testi va a capo una volta sola. Se si
    applica la regola sbagliata, decine di paragrafi finiscono in un blocco
    unico, e la misura del respiro del paragrafo descrive il formato del file
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

    Ogni frase porta con sé l'informazione se proviene da una voce di
    elenco: chi scrive molto per elenchi ha frasi più corte per un motivo
    strutturale, e la scheda deve poterlo dire.

    Quando le righe vuote non separano i paragrafi, ogni riga di prosa è un
    paragrafo a sé, mentre le voci di elenco contigue restano insieme perché
    formano un blocco solo sulla pagina.
    """
    paragrafi: List[List[Tuple[str, bool]]] = []
    corrente: List[Tuple[str, bool]] = []
    buffer_prosa: List[str] = []

    def svuota_prosa() -> None:
        if buffer_prosa:
            unito = " ".join(buffer_prosa)
            corrente.extend(
                (frase, False)
                for frase in dividi_in_frasi(unito)
                if ha_parole(frase)
            )
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
            corrente.extend(
                (frase, True) for frase in frasi if ha_parole(frase)
            )
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

    Stacca l'elisione iniziale e riduce a minuscolo, altrimenti *l'attenzione*
    e *attenzione* risulterebbero due parole diverse e la varietà lessicale
    uscirebbe gonfiata. Stacca solo quando la coda è una parola comune: comincia
    con una lettera minuscola ed è fatta di sole lettere. Così *dell'arte* dà
    *arte* e *anch'io* dà *io*, ma un cognome come *Dell'Orso*, che ha la coda
    maiuscola, resta intero e non si confonde con *orso*, e un anno come
    *dell'800*, che ha la coda non alfabetica, non diventa il numero *800*.
    Il troncamento tiene invece l'apostrofo: *po'*, *va'*, *da'* hanno la coda
    vuota e restano come sono. Toglierlo faceva comparire *un po* nelle
    ricorrenze della scheda, cioè una forma che l'italiano non ammette, in un
    documento che nasce per essere allegato come prova della propria voce.

    Non è una lemmatizzazione: le forme flesse restano distinte, e lo strumento
    lo dichiara. L'apostrofo tipografico è già ridotto a quello dritto da
    `normalizza`, ma la funzione lo ripete per reggere anche se chiamata da
    sola.
    """
    parola = parola.replace("’", "'").replace("ʼ", "'")
    if "'" in parola:
        coda = parola.partition("'")[2]
        if coda and coda[:1].islower() and coda.isalpha():
            return coda.lower()
    return parola.lower()


def conta_lettere(testo: str) -> int:
    return sum(1 for carattere in testo if carattere.isalpha())


# --------------------------------------------------------------------------
# Misure
# --------------------------------------------------------------------------


def deviazione(valori: Sequence[float]) -> float:
    """Deviazione standard campionaria, zero se il campione è minimo."""
    return statistics.stdev(valori) if len(valori) > 1 else 0.0


def gulpease(frasi: int, lettere: int, parole: int) -> Optional[float]:
    """Indice Gulpease (Lucisano e Piemontese, 1988)."""
    if parole == 0:
        return None
    return 89 + (300 * frasi - 10 * lettere) / parole


def mattr(forme: Sequence[str], finestra: int) -> Optional[float]:
    """Type-Token Ratio a finestra mobile (Covington e McFall, 2010).

    Su testi più corti della finestra restituisce il rapporto grezzo, che
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
    """Coppie di parole con cui le frasi più spesso iniziano o finiscono."""
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


def nome_cartella(cartella: Path) -> str:
    """Nome della cartella per la scheda, mai il percorso assoluto.

    Finisce nel campo «cartella» del JSON, che nasce per essere allegato a una
    difesa: il percorso intero porterebbe con sé il nome utente del sistema. La
    radice del filesystem non ha nome, e allora si usa un'etichetta neutra
    invece del percorso.
    """
    return cartella.name or "corpus"


def calcola_profilo(cartella: Path, nome: Optional[str]) -> Dict:
    """Legge il corpus e restituisce il profilo completo."""
    esclusioni: Counter = Counter()
    percorsi = raccogli_file(cartella, esclusioni)
    if not percorsi:
        raise ErroreCorpus(
            "Nessun file .txt, .md o .markdown trovato in {}.".format(cartella)
        )

    byte_totali = 0
    for percorso in percorsi:
        try:
            byte_totali += percorso.stat().st_size
        except OSError:
            continue
    if byte_totali > BYTE_CON_AVVISO:
        print(
            "Avviso: il corpus pesa {} MB. L'elaborazione tiene in memoria "
            "circa venticinque volte la dimensione del testo, quindi su una "
            "macchina comune un corpus di questa taglia può esaurirla. "
            "Conviene lavorare su una selezione dello stesso registro.".format(
                round(byte_totali / (1024 * 1024))
            ),
            file=sys.stderr,
        )

    schede_file: List[Dict] = []
    paragrafi_totali: List[List[Tuple[str, bool]]] = []

    for percorso in percorsi:
        try:
            contenuto, codifica = leggi_file(percorso)
        except (OSError, ErroreCorpus):
            # Un file può diventare illeggibile fra l'elenco e la lettura:
            # permessi cambiati, antivirus che lo tiene aperto, una cartella
            # il cui nome finisce per .txt. Oppure il contenuto non decodifica
            # in nessuna delle codifiche tentate, e allora `leggi_file`
            # solleva `ErroreCorpus`, che non discende da `OSError` e va
            # quindi nominata a parte. La cattura resta esplicita su queste
            # due: un `except Exception` nudo inghiottirebbe anche gli errori
            # di programmazione, facendoli passare per file illeggibili.
            esclusioni["file_illeggibili"] += 1
            continue
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
        if esclusioni["file_illeggibili"] and not schede_file:
            # Distinguere questo caso serve a chi legge il messaggio: un
            # corpus tutto illeggibile e un corpus di sole intestazioni
            # danno lo stesso risultato vuoto per motivi opposti.
            raise ErroreCorpus(
                "Nessun file del corpus ha prodotto testo. Esclusi come "
                "illeggibili: {} su {}. Le codifiche tentate sono UTF-8 e "
                "cp1252.".format(esclusioni["file_illeggibili"], len(percorsi))
            )
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
        1 for forma in forme if confronto(forma) in CONNETTIVI_CONFRONTO
    )
    percentuale_connettivi = (
        conteggio_connettivi * 100 / totale_parole if totale_parole else 0.0
    )
    connettivi_frequenti = Counter(
        forma for forma in forme if confronto(forma) in CONNETTIVI_CONFRONTO
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

    # I connettivi hanno la loro lista dedicata: escluderli anche qui evita che
    # le forme meno comuni («benché», «laddove») compaiano due volte, sia fra i
    # connettivi sia fra le parole piene.
    parole_piene = Counter(
        forma
        for forma in forme
        if confronto(forma) not in PAROLE_VUOTE_CONFRONTO
        and confronto(forma) not in CONNETTIVI_CONFRONTO
        and len(forma) > 2
    ).most_common(25)

    punteggiatura = conta_punteggiatura(testo_unito, totale_parole)

    profilo = {
        "_firma": FIRMA,
        "strumento": {
            "nome": "profilo_voce.py",
            "versione": VERSIONE,
            "finestra_mattr": FINESTRA_MATTR,
            "finestra_ttr_confronto": FINESTRA_TTR_CONFRONTO,
        },
        "corpus": {
            "autore": nome,
            # Solo il nome, non il percorso: la scheda voce nasce per essere
            # allegata a una difesa, e il percorso completo porterebbe con sé
            # il nome utente del sistema operativo.
            "cartella": nome_cartella(cartella),
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
                sum(1 for frase in frasi if chiude_con(frase, "?"))
                * 100
                / len(frasi),
                1,
            )
            if frasi
            else 0.0,
            "quota_esclamative": round(
                sum(1 for frase in frasi if chiude_con(frase, "!"))
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
            # Con un blocco solo la deviazione vale zero per definizione, e
            # zero verrebbe letto come «non varia mai» invece che come «non
            # c'è un secondo blocco da confrontare». Meglio dichiarare che
            # la misura manca, così non entra nemmeno nel posizionamento.
            "gulpease_deviazione_fra_blocchi": round(
                deviazione(gulpease_blocchi), 2
            )
            if len(gulpease_blocchi) > 1
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
            # Sotto la finestra di mille parole il TTR ripiega sul rapporto
            # grezzo, che dipende dalla lunghezza: collocarlo rispetto
            # all'intervallo umano darebbe un giudizio senza senso, quindi qui
            # viene omesso e la scheda lo dichiara. La soglia è <=, perché a
            # mille parole esatte la finestra mobile è una sola e coincide col
            # rapporto grezzo.
            posizione_rispetto(ttr_1000, "ttr_finestra_1000")
            if totale_parole > FINESTRA_TTR_CONFRONTO
            else None,
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


def numero(valore: object) -> str:
    """Scrive un valore con la virgola decimale, come vuole l'italiano.

    Si applica al singolo valore prima che diventi testo. Una sostituzione
    sul documento finito prenderebbe anche i numeri di versione e i punti
    fermi di fine frase, che punti decimali non sono.

    Il file JSON resta col punto: là il numero è un dato da rileggere con un
    programma, non una cifra da leggere con gli occhi.
    """
    if isinstance(valore, float):
        return "{}".format(valore).replace(".", ",")
    return "{}".format(valore)


def tabella(intestazioni: Sequence[str], righe: Iterable[Sequence[str]]) -> List[str]:
    fuori = ["| " + " | ".join(intestazioni) + " |"]
    fuori.append("|" + "|".join(["---"] * len(intestazioni)) + "|")
    for riga in righe:
        fuori.append("| " + " | ".join(numero(cella) for cella in riga) + " |")
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
    """Compone la scheda leggibile, con l'affidabilità in apertura."""
    corpus = profilo["corpus"]
    frase = profilo["respiro_della_frase"]
    paragrafo = profilo["respiro_del_paragrafo"]
    lettura = profilo["leggibilita"]
    lessico = profilo["ricchezza_del_lessico"]
    persone = profilo["persona_e_lettore"]
    ricorrenze = profilo["ricorrenze"]

    titolo = corpus["autore"] or "voce anonima"
    fuori: List[str] = [
        "<!-- {} -->".format(FIRMA),
        "# Scheda voce: {}".format(titolo),
        "",
    ]

    fuori += [
        "> Profilo calcolato su {} file, {} parole totali. Affidabilità: {}.".format(
            corpus["file_letti"], corpus["parole_totali"], corpus["affidabilita"]
        ),
        "> I valori descrivono questo corpus, non una persona: cambiando",
        "> registro cambiano. Questa scheda misura, non giudica.",
        "",
        "Livello **misurato**, prodotto da `profilo_voce.py` versione {}.".format(
            profilo["strumento"]["versione"]
        ),
        "Il livello **osservato** (tic autentici, aperture e chiusure tipiche,",
        "ciò che questa voce non fa mai) si aggiunge leggendo il corpus, e cita",
        "sempre il passo da cui nasce.",
        "",
        "## Respiro della frase",
        "",
    ]
    fuori += tabella(
        ["Misura", "Valore"],
        [
            ["Frasi", corpus["frasi_totali"]],
            ["Lunghezza media", "{} parole".format(numero(frase["lunghezza_media"]))],
            ["Deviazione standard", frase["deviazione_standard"]],
            [
                "Coefficiente di variazione",
                "{} (variazione del respiro)".format(
                    numero(frase["coefficiente_di_variazione"])
                ),
            ],
            ["Mediana", frase["mediana"]],
            [
                "Minimo e massimo",
                "{} e {}".format(numero(frase["minimo"]), numero(frase["massimo"])),
            ],
            [
                "Frasi sotto le sei parole",
                "{} per cento".format(numero(frase["quota_sotto_sei_parole"])),
            ],
            [
                "Frasi sopra le trentacinque parole",
                "{} per cento".format(
                    numero(frase["quota_sopra_trentacinque_parole"])
                ),
            ],
            [
                "Frasi che sono domande",
                "{} per cento".format(numero(frase["quota_interrogative"])),
            ],
            [
                "Frasi esclamative",
                "{} per cento".format(numero(frase["quota_esclamative"])),
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
                "{} per cento".format(numero(paragrafo["quota_testo_in_elenchi"])),
            ],
        ],
    )

    fuori += ["## Leggibilità", ""]
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
                else (
                    "un solo blocco, niente da confrontare"
                    if lettura["blocchi_misurati"] == 1
                    else "corpus troppo breve"
                ),
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
            ["Varietà a finestra di 50 parole", lessico["mattr_finestra_50"]],
            ["Varietà a finestra di mille parole", lessico["ttr_finestra_1000"]],
            ["Vocabolario", "{} forme diverse".format(lessico["vocabolario"])],
            ["Usate una volta sola", lessico["parole_usate_una_volta_sola"]],
            ["Quota di parole usate una volta sola", lessico["quota_hapax"]],
        ],
    )
    if corpus["parole_totali"] < FINESTRA_TTR_CONFRONTO:
        piu_corta = (
            "di tutte e due le finestre"
            if corpus["parole_totali"] < FINESTRA_MATTR
            else "della finestra da mille parole"
        )
        fuori += [
            "Il corpus è più corto {}. Per quella misura il valore qui sopra "
            "non è una media a finestra mobile, ma il rapporto grezzo fra "
            "forme diverse e parole totali: dipende dalla lunghezza del testo "
            "e non si confronta con corpus di taglia diversa.".format(piu_corta),
            "",
        ]
    fuori += [
        "Lo strumento non ha un dizionario: *scrive* e *scrivere* contano come",
        "due parole diverse.",
        "",
        "Le due varietà rispondono a domande diverse e possono divergere. La",
        "finestra corta dice quanto il lessico si muove riga per riga. La",
        "finestra lunga risente del tema: un testo che parla sempre della",
        "stessa cosa ripete le parole di quel campo anche se il resto del",
        "vocabolario è ricco.",
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
        "Virgole per frase: {}.".format(numero(profilo["virgole_per_frase"])),
        "",
    ]
    segni = profilo["punteggiatura_per_mille_parole"]
    fuori_norma = []
    if segni.get("trattini_lunghi", 0):
        fuori_norma.append(
            "trattini lunghi ({} ogni mille parole), esclusi dalla regola 1".format(
                numero(segni["trattini_lunghi"])
            )
        )
    if segni.get("virgolette_inglesi", 0) or segni.get("virgolette_dritte", 0):
        fuori_norma.append(
            "virgolette non italiane ({} inglesi e {} dritte ogni mille "
            "parole), escluse dalla regola 3, che vuole i caporali".format(
                numero(segni.get("virgolette_inglesi", 0)),
                numero(segni.get("virgolette_dritte", 0)),
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
        "Densità di connettivi: {} per cento delle parole.".format(
            numero(ricorrenze["connettivi_percento_sul_totale"])
        ),
        "",
        "**Connettivi più usati.**",
        "",
    ]
    fuori += elenco_coppie(ricorrenze["connettivi_frequenti"], "Nessuno ricorrente.")
    fuori += ["**Parole piene più frequenti.**", ""]
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
        "Una sequenza frequente può essere un tic autentico da difendere oppure",
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
                "{} - {}".format(*[numero(v) for v in voce["intervallo_umano"]]),
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
    if corpus["parole_totali"] <= FINESTRA_TTR_CONFRONTO:
        fuori += [
            "La varietà a finestra di mille parole non compare in questa "
            "tabella: sotto quella soglia è un rapporto grezzo che dipende "
            "dalla lunghezza, e collocarlo rispetto all'intervallo umano "
            "darebbe un giudizio senza senso. La sezione «Ricchezza del "
            "lessico» la riporta con la stessa cautela.",
            "",
        ]
    fuori += [
        "Anche questi intervalli sono soglie decise da qualcuno, come quelle",
        "dei rilevatori che `references/scudo-falsi-positivi.md` contesta. La",
        "differenza sta nell'uso: qui servono a orientare chi scrive il proprio",
        "testo, e non a stabilire niente sul testo di un altro.",
        "",
        "**La posizione non è un giudizio.** Stare sotto un intervallo non",
        "rende un testo sospetto, e starci dentro non lo assolve. Le sei",
        "misure vanno lette insieme e incrociate con la lettura: presa da",
        "sola, nessuna distingue una voce umana da un testo generato.",
        "",
    ]
    fuori += [
        "Gli intervalli vengono da `references/metodologie-operative.md`",
        "sezione 6, che dichiara di sé stessa: stime indicative, ordini di",
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
        "riconoscimento è automatico: applicare la regola sbagliata farebbe",
        "misurare il formato del file al posto della voce.",
        "",
    ]

    esclusioni = corpus["esclusioni_in_pulizia"]
    if esclusioni:
        fuori += ["## Escluso in pulizia", ""]
        fuori += tabella(
            ["Elemento", "Quantità"],
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
        "4. Non giudica la qualità: un testo pessimo e uno ottimo possono",
        "   avere lo stesso profilo.",
        "5. Non è un rilevatore di AI e non serve a ingannarne uno.",
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
    parser.add_argument(
        "corpus", help="cartella contenente i testi (.txt, .md o .markdown)"
    )
    parser.add_argument(
        "--out",
        help="cartella dove scrivere scheda-voce.md e profilo-voce.json",
    )
    parser.add_argument("--nome", help="nome dell'autore, usato nel titolo")
    parser.add_argument(
        "--versione", action="version", version="profilo_voce.py " + VERSIONE
    )
    return parser


def porta_la_firma(percorso: Path) -> bool:
    """Vero se il file esiste ed è una nostra uscita, riconosciuta dalla firma
    in testa: la prima riga per la scheda, la prima chiave `_firma` per il JSON.

    Il controllo è posizionale, non una ricerca ovunque nel file: un documento
    dell'utente che citasse la firma più in basso non deve essere scambiato per
    una nostra uscita e sovrascritto. Un percorso che non è un file regolare
    (una cartella o una pipe con lo stesso nome) o che non si lascia leggere non
    porta la firma e viene trattato come non nostro: meglio fermarsi che
    cancellare il lavoro di qualcun altro o restare appesi ad aprire una pipe
    senza scrittore.
    """
    if not percorso.is_file():
        return False
    try:
        if percorso.suffix == ".json":
            with percorso.open("r", encoding="utf-8") as sorgente:
                dati = json.load(sorgente)
            return (
                isinstance(dati, dict)
                and next(iter(dati), None) == "_firma"
                and dati.get("_firma") == FIRMA
            )
        with percorso.open("r", encoding="utf-8", errors="replace") as sorgente:
            prima_riga = sorgente.readline()
        return prima_riga.strip() == "<!-- {} -->".format(FIRMA)
    except (OSError, ValueError):
        return False


def errore_scrittura_pulito(errore: OSError) -> str:
    """Messaggio d'errore di scrittura senza il percorso assoluto.

    Il testo predefinito di un OSError include il percorso completo del file,
    che su molti sistemi porta con sé il nome utente. La scheda voce nasce per
    essere allegata a una difesa, quindi nemmeno i suoi errori devono rivelare
    il percorso: si tiene il motivo e, se c'è, il solo nome del file.
    """
    motivo = errore.strerror or type(errore).__name__
    nome = Path(errore.filename).name if errore.filename else ""
    if nome:
        return "Errore di scrittura su «{}»: {}.".format(nome, motivo)
    return "Errore di scrittura: {}.".format(motivo)


def main(argomenti: Optional[Sequence[str]] = None) -> int:
    opzioni = costruisci_parser().parse_args(argomenti)
    cartella = Path(opzioni.corpus).expanduser()
    uscita = Path(opzioni.out).expanduser() if opzioni.out else cartella

    try:
        profilo = calcola_profilo(cartella, opzioni.nome)
    except ErroreCorpus as errore:
        print("Errore: {}".format(errore), file=sys.stderr)
        return 2

    percorso_scheda = uscita / "scheda-voce.md"
    percorso_dati = uscita / "profilo-voce.json"

    # Prima di scrivere, un file per volta: se esiste già e non porta la firma
    # dello strumento, è di qualcun altro e non va toccato. Il controllo
    # precede ogni scrittura, così un conflitto sul secondo file non lascia il
    # primo già riscritto. Nel messaggio solo il nome, non il percorso, che
    # porterebbe con sé il nome utente del sistema operativo.
    for percorso in (percorso_scheda, percorso_dati):
        if percorso.exists() and not porta_la_firma(percorso):
            print(
                "Errore: «{}» esiste già e non porta la firma di questo "
                "strumento. Può essere un file tuo, o una scheda di una "
                "versione precedente. Non lo sovrascrivo: scrivi in un'altra "
                "cartella con --out, oppure rimuovilo se è una vecchia "
                "uscita.".format(percorso.name),
                file=sys.stderr,
            )
            return 3

    try:
        uscita.mkdir(parents=True, exist_ok=True)
        percorso_scheda.write_text(scrivi_scheda(profilo), encoding="utf-8")
        percorso_dati.write_text(
            json.dumps(profilo, ensure_ascii=False, indent=2), encoding="utf-8"
        )
    except OSError as errore:
        print(errore_scrittura_pulito(errore), file=sys.stderr)
        return 2

    corpus = profilo["corpus"]
    print(
        "Profilo calcolato su {} file, {} parole, {} frasi. Affidabilità: {}.".format(
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

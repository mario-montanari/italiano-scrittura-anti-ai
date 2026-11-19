#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Misura i tic ricorrenti in una cartella di testi.

Serve a verificare sul campo l'effetto delle regole della skill: si generano
gli stessi testi con due versioni diverse e si confrontano le misure, anche
con un campione di prosa umana estratto da PAISÀ con campiona_paisa.py.
Legge tutti i file .md della cartella, salta la prima riga (il titolo) e
ignora l'elenco «Da completare» che la regola 18 chiede in fondo al testo.
Scritto da Renato Romano nel suo fork, rivisto per la versione 1.7.0.

    python extras/misura_campione.py CARTELLA [CARTELLA ...]

Con più cartelle stampa una tabella di confronto, una colonna per cartella.
Le misure sono euristiche, pensate per confrontare campioni fra loro e non
per giudicare un testo singolo. Usa la sola libreria standard e non scrive
nessun file.
"""

import pathlib
import re
import statistics
import sys

# L'apostrofo è sia quello dritto sia quello tipografico (’).
LETTERA = r"A-Za-zÀ-ÿ'’"
# Il titolo dell'elenco «Da completare», da solo sulla riga, anche fra trattini bassi.
RX_DA_COMPLETARE = r"^[\W_]*da completare[\W_]*$"
# Una voce di elenco, e la riga rientrata che la continua.
RX_VOCE_DI_ELENCO = r"^\s*(?:[-*+]|\d+[.)])\s"
RX_CONTINUAZIONE = r"^\s+\S"

MISURE = {
    "virgola prima di e": rf",\s+e(?![{LETTERA}])",
    "due punti": r":",
    "punto e virgola": r";",
    "em-dash": r"—",
    "gerundio in coda": r", [a-zàèéìòù]+(?:ando|endo)\b",
    "non è X, è Y": r"\bnon è\b[^.;]{1,60}[,:;] è\b",
    "non solo X ma Y": r"\bnon solo\b[^.]{0,80}\bma\b",
    "suspense «è un altro»": r"\bè (?:un altro|un['’]altra|questo|questa)[.:]",
    "riga di elenco": r"(?m)^\s*[-*] ",
    "segnaposto [..]": r"\[[^\]\n]{1,40}\]",
    "grassetto": r"\*\*[^*]+\*\*",
}

PRIMA_PERSONA = r"\b(?:ho|avevo) (?:[a-zàèéìòù]+ )?[a-zàèéìòù]+(?:ato|uto|ito)\b"
# La soglia del periodo lungo della regola 15.
PERIODO_LUNGO = 35


def taglia_da_completare(righe):
    """Toglie l'elenco «Da completare» in fondo e dice se c'era.

    Come in scripts/controlla_testo.py: si taglia all'ultimo titolo solo se
    dopo viene almeno una voce di elenco, e ogni riga piena è una voce o la
    continuazione rientrata di una voce già vista. Un titolo seguito da
    prosa, o da sole righe rientrate, non taglia niente.
    """
    for i in range(len(righe) - 1, -1, -1):
        if re.match(RX_DA_COMPLETARE, righe[i], re.IGNORECASE):
            voce_vista = False
            for r in righe[i + 1:]:
                if not r.strip():
                    continue
                if re.match(RX_VOCE_DI_ELENCO, r):
                    voce_vista = True
                elif not (voce_vista and re.match(RX_CONTINUAZIONE, r)):
                    return righe, False
            return (righe[:i], True) if voce_vista else (righe, False)
    return righe, False


def corpo(testo):
    return "\n".join(taglia_da_completare(testo.splitlines()[1:])[0])


def lunghezze_frasi(testo):
    """Parole per frase, con le frasi di almeno tre parole."""
    return [len(s.split()) for s in re.split(r"(?<=[.!?])\s+", " ".join(testo.split()))
            if len(s.split()) > 2]


def misura(cartella):
    file = sorted(pathlib.Path(cartella).glob("*.md"))
    file = [f for f in file if f.name.upper() != "RAPPORTO.MD"]
    conteggi = dict.fromkeys(MISURE, 0)
    parole = e_tot = 0
    con_da_completare = 0
    blog_prima_persona = 0
    cv = []
    tutte_le_frasi = []
    for f in file:
        testo = f.read_text(encoding="utf-8")
        righe, con_elenco = taglia_da_completare(testo.splitlines()[1:])
        if con_elenco:
            con_da_completare += 1
        c = "\n".join(righe)
        parole += len(re.findall(rf"[{LETTERA}]+", c))
        e_tot += len(re.findall(rf"(?<![{LETTERA}])e(?![{LETTERA}])", c))
        for nome, rx in MISURE.items():
            conteggi[nome] += len(re.findall(rx, c))
        if f.name.startswith("blog") and re.search(PRIMA_PERSONA, c):
            blog_prima_persona += 1
        frasi = lunghezze_frasi(c)
        tutte_le_frasi.extend(frasi)
        if frasi:
            cv.append(statistics.pstdev(frasi) / statistics.mean(frasi))
    lunghe = sum(1 for n in tutte_le_frasi if n > PERIODO_LUNGO)
    return {
        "testi": len(file),
        "parole": parole,
        "e precedute da virgola (%)": round(100 * conteggi["virgola prima di e"] / e_tot, 1) if e_tot else 0,
        **{f"{k} (ogni 1000 parole)": round(1000 * v / parole, 2) if parole else 0
           for k, v in conteggi.items()},
        "blog con passato prossimo in 1a persona": blog_prima_persona,
        "testi con elenco Da completare": con_da_completare,
        "parole per frase, media": round(statistics.mean(tutte_le_frasi), 1) if tutte_le_frasi else 0,
        f"frasi oltre le {PERIODO_LUNGO} parole (%)":
            round(100 * lunghe / len(tutte_le_frasi), 1) if tutte_le_frasi else 0,
        "variazione lunghezza frasi (CV medio)": round(statistics.mean(cv), 2) if cv else 0,
    }


def main():
    cartelle = sys.argv[1:]
    if not cartelle:
        sys.exit(__doc__)
    risultati = [misura(c) for c in cartelle]
    nomi = [pathlib.Path(c).name for c in cartelle]
    larghezza = max(len(k) for k in risultati[0])
    print(" " * larghezza + "  " + "  ".join(f"{n:>10}" for n in nomi))
    for chiave in risultati[0]:
        print(f"{chiave:<{larghezza}}  " + "  ".join(f"{r[chiave]:>10}" for r in risultati))


if __name__ == "__main__":
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    main()

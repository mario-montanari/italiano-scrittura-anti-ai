#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Estrae da PAISÀ un campione di prosa umana da confrontare con i testi generati.

PAISÀ è un corpus di web italiano raccolto nel 2010, prima dei modelli
linguistici, con licenza CC BY-NC-SA 4.0. Si scarica a parte (paisa.raw.utf8.gz,
circa 520 MB, da http://hdl.handle.net/20.500.12124/3) e non sta nella repo:
nemmeno il campione estratto va messo nella repo. Lo script divide i
documenti in tre gruppi secondo l'indirizzo d'origine (Wikipedia e progetti
affini, blog, altro web), tiene quelli fra 250 e 800 parole e ne estrae a
caso lo stesso numero per gruppo, con un seme fisso.
Scritto da Renato Romano nel suo fork, rivisto per la versione 1.7.0.

    python extras/campiona_paisa.py paisa.raw.utf8.gz CARTELLA [--per-gruppo 300]

Ogni documento diventa un file .md con l'indirizzo d'origine in prima riga,
nel formato che extras/misura_campione.py legge. Se una delle tre cartelle
di uscita contiene già dei file .md, si ferma senza toccarli. Usa la sola
libreria standard e non accede alla rete.
"""

import argparse
import collections
import gzip
import pathlib
import random
import re
import sys

SEME = 19
GRUPPI = ("paisa-wikipedia", "paisa-blog", "paisa-altro-web")


def gruppo(url):
    if re.search(r"wiki(?:pedia|books|news|source|versity|voyage)", url):
        return "paisa-wikipedia"
    if "blog" in url:
        return "paisa-blog"
    return "paisa-altro-web"


def main(argomenti=None):
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("corpus", type=pathlib.Path)
    parser.add_argument("uscita", type=pathlib.Path)
    parser.add_argument("--per-gruppo", type=int, default=300)
    args = parser.parse_args(argomenti)

    occupate = [g for g in GRUPPI if any((args.uscita / g).glob("*.md"))]
    if occupate:
        sys.exit(f"In {args.uscita} le cartelle {', '.join(occupate)} contengono già dei testi: "
                 "non li sovrascrivo. Indica una cartella di uscita nuova.")

    random.seed(SEME)
    campioni = collections.defaultdict(list)
    visti = collections.Counter()

    def chiudi(url, righe):
        testo = "\n".join(righe).strip()
        if not 250 <= len(testo.split()) <= 800:
            return
        g = gruppo(url)
        visti[g] += 1
        scelti = campioni[g]
        if len(scelti) < args.per_gruppo:
            scelti.append((url, testo))
        else:
            j = random.randrange(visti[g])
            if j < args.per_gruppo:
                scelti[j] = (url, testo)

    documento, url = None, ""
    with gzip.open(args.corpus, "rt", encoding="utf-8", errors="replace") as f:
        for riga in f:
            if riga.startswith("<text "):
                if documento is not None:
                    chiudi(url, documento)
                trovato = re.search(r'url="([^"]*)"', riga)
                url, documento = (trovato.group(1) if trovato else ""), []
            elif riga.startswith("</text"):
                if documento is not None:
                    chiudi(url, documento)
                documento = None
            elif documento is not None and not riga.startswith("#"):
                documento.append(riga.rstrip("\n"))

    for g, scelti in sorted(campioni.items()):
        cartella = args.uscita / g
        cartella.mkdir(parents=True, exist_ok=True)
        for i, (u, testo) in enumerate(scelti, 1):
            (cartella / f"{g}-{i:03}.md").write_text(f"# {u}\n{testo}\n", encoding="utf-8")
        print(f"{g}: {len(scelti)} estratti su {visti[g]} documenti adatti")


if __name__ == "__main__":
    main()

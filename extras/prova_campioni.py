#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Prove automatiche di misura_campione.py e campiona_paisa.py.

    python extras/prova_campioni.py

Controlla anche che misura_campione.py e scripts/controlla_testo.py contino
le frasi allo stesso modo e che la media umana della regola 15 di SKILL.md
sia quella che controlla_testo.py mostra.
Scrive soltanto dentro una cartella temporanea, e la rimuove alla fine.
Esce con 0 se tutte le prove passano, con 1 altrimenti.
"""

import gzip
import importlib.util
import pathlib
import re
import sys
import tempfile

QUI = pathlib.Path(__file__).resolve().parent
RADICE = QUI.parent


def carica(nome, cartella=QUI):
    spec = importlib.util.spec_from_file_location(nome, cartella / f"{nome}.py")
    modulo = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(modulo)
    return modulo


misura_campione = carica("misura_campione")
campiona_paisa = carica("campiona_paisa")
controlla_testo = carica("controlla_testo", RADICE / "scripts")
fallite = []
totale = 0


def verifica(descrizione, condizione):
    global totale
    totale += 1
    if not condizione:
        fallite.append(descrizione)


def prova_misura(radice):
    cartella = radice / "campione"
    cartella.mkdir()
    breve = "Uno due tre quattro."
    lunga = " ".join(["parola"] * 39) + " fine."  # 40 parole
    # Una riga che comincia con «Da completare» dentro il testo non lo tronca;
    # la riga che contiene solo il titolo dell'elenco sì.
    (cartella / "a.md").write_text(
        "# Titolo\n" + breve + " " + lunga + "\n"
        "Da completare entro lunedì il modulo della domanda.\n"
        "## Da completare\n- " + lunga + "\n- " + lunga + "\n", encoding="utf-8")
    risultato = misura_campione.misura(cartella)
    # Frasi contate: 4, 40, 8 (la riga «Da completare entro...»); le due lunghe dopo il titolo no.
    verifica("frase media su 4, 40 e 8 parole", risultato["parole per frase, media"] == round((4 + 40 + 8) / 3, 1))
    verifica("una frase su tre oltre le 35 parole", risultato["frasi oltre le 35 parole (%)"] == round(100 / 3, 1))
    verifica("il testo con l'elenco conta come testo con Da completare",
             risultato["testi con elenco Da completare"] == 1)
    trattini = radice / "trattini"
    trattini.mkdir()
    (trattini / "b.md").write_text("# Titolo\n" + breve + "\n_Da completare_\n- " + lunga + "\n", encoding="utf-8")
    con_trattini = misura_campione.misura(trattini)
    verifica("«_Da completare_» fra trattini bassi tronca la misura",
             con_trattini["parole per frase, media"] == 4 and con_trattini["testi con elenco Da completare"] == 1)
    apostrofi = radice / "apostrofi"
    apostrofi.mkdir()
    (apostrofi / "c.md").write_text("# Titolo\nLa strada è un’altra. Poi il resto.\n", encoding="utf-8")
    verifica("la suspense con l'apostrofo tipografico si conta",
             misura_campione.misura(apostrofi)["suspense «è un altro» (ogni 1000 parole)"] > 0)
    vuota = radice / "vuota"
    vuota.mkdir()
    verifica("cartella vuota senza errori", misura_campione.misura(vuota)["parole per frase, media"] == 0)


def prova_da_completare_in_fondo(radice):
    # L'elenco «Da completare» si taglia solo se sta in fondo al testo: un
    # elenco in testa, un titolo seguito da prosa o il primo di due titoli non
    # tolgono il testo che viene dopo; la voce che va a capo rientrata sì.
    # Parole attese: le 40 della frase più quelle che restano del titolo
    # («Da completare», 2) e della voce («prezzo», 1) quando non si taglia.
    lunga = " ".join(["parola"] * 39) + " fine."  # 40 parole
    casi = {
        "elenco in testa": ("# T\n## Da completare\n- prezzo\n\n" + lunga + "\n", 43, 0),
        "titolo seguito da prosa": ("# T\n**Da completare**\n\n" + lunga + "\n", 42, 0),
        "due titoli": ("# T\n## Da completare\n\n" + lunga + "\n\n## Da completare\n- prezzo\n", 42, 1),
        "voce che va a capo": ("# T\n" + lunga + "\n\nDa completare:\n- prezzo del corso,\n  " + lunga + "\n", 40, 1),
        # Senza una voce non c'è elenco: niente taglio.
        "solo righe rientrate": ("# T\n## Da completare\n    " + lunga + "\n", 42, 0),
        "rientrata prima della voce": ("# T\n" + lunga + "\n\n## Da completare\n  prima riga\n- prezzo\n", 45, 0),
        "titolo senza voci": ("# T\n" + lunga + "\n\n## Da completare\n\n", 42, 0),
    }
    for nome, (testo, parole, con_elenco) in casi.items():
        cartella = radice / ("da-completare-" + nome.replace(" ", "-"))
        cartella.mkdir()
        (cartella / "e.md").write_text(testo, encoding="utf-8")
        risultato = misura_campione.misura(cartella)
        verifica(f"Da completare, {nome}: parole del testo contate",
                 risultato["parole"] == parole and risultato["testi con elenco Da completare"] == con_elenco)


def prova_frasi_come_controlla_testo(radice):
    # La media umana citata conta le frasi di almeno tre parole: se uno dei due
    # strumenti cambiasse modo di contare, il confronto con PAISÀ non reggerebbe.
    # Quindici frasi di 18 parole alternate a quindici di due: da tre parole in
    # su la media è 18, contate tutte scende a 10 e la regola 15 scatterebbe.
    lunga = " ".join(["parola"] * 17) + " fine."
    corta = " ".join(["parola"] * 9) + " fine."
    testo = "# Titolo\n" + " ".join([lunga + " Molto bene."] * 15) + "\n"
    cartella = radice / "frasi"
    cartella.mkdir()
    (cartella / "d.md").write_text(testo, encoding="utf-8")
    verifica("misura_campione salta le frasi sotto le tre parole",
             misura_campione.misura(cartella)["parole per frase, media"] == 18)
    verifica("controlla_testo salta le frasi sotto le tre parole",
             "frasi corte e uniformi" not in [t[2] for t in controlla_testo.controlla(testo)])
    con_corte = "# Titolo\n" + " ".join([corta + " Molto bene."] * 15) + "\n"
    verifica("controlla_testo segnala quindici frasi di 10 parole",
             "frasi corte e uniformi" in [t[2] for t in controlla_testo.controlla(con_corte)])
    skill = (RADICE / "SKILL.md").read_text(encoding="utf-8")
    citata = re.search(r"nei blog umani del corpus PAISÀ la frase media è di ([\d,]+) parole", skill)
    verifica("la media umana della regola 15 è quella di controlla_testo",
             bool(citata) and float(citata.group(1).replace(",", ".")) == controlla_testo.MEDIA_FRASE_UMANA)


def documento(url, parole):
    return f'<text id="x" url="{url}">\n' + " ".join(["parola"] * parole) + "\n</text>\n"


def prova_campiona(radice):
    corpus = radice / "paisa.raw.utf8.gz"
    with gzip.open(corpus, "wt", encoding="utf-8") as f:
        f.write(documento("http://esempio.blogspot.com/a", 300))
        f.write(documento("http://it.wikipedia.org/wiki/B", 400))
        f.write(documento("http://www.esempio.it/c", 500))
        f.write(documento("http://altro.blogspot.com/corto", 100))  # sotto le 250 parole: escluso
    uscita = radice / "riferimento"
    campiona_paisa.main([str(corpus), str(uscita), "--per-gruppo", "5"])
    blog = sorted((uscita / "paisa-blog").glob("*.md"))
    verifica("un solo blog estratto, quello lungo abbastanza", len(blog) == 1)
    verifica("prima riga con l'indirizzo d'origine",
             bool(blog) and blog[0].read_text(encoding="utf-8").startswith("# http://esempio.blogspot.com/a\n"))
    verifica("Wikipedia e altro web estratti",
             len(list((uscita / "paisa-wikipedia").glob("*.md"))) == 1
             and len(list((uscita / "paisa-altro-web").glob("*.md"))) == 1)
    prima = blog[0].read_bytes() if blog else b""
    if blog:
        blog[0].write_text("# mio\ntesto mio\n", encoding="utf-8")
    try:
        campiona_paisa.main([str(corpus), str(uscita), "--per-gruppo", "5"])
        fermato = False
    except SystemExit as uscita_anticipata:
        fermato = "non li sovrascrivo" in str(uscita_anticipata.code)
    verifica("cartella già piena: si ferma con un messaggio", fermato)
    verifica("cartella già piena: il file resta com'era",
             bool(blog) and blog[0].read_text(encoding="utf-8") == "# mio\ntesto mio\n" and prima != b"")
    verifica("gruppi secondo l'indirizzo",
             (campiona_paisa.gruppo("http://it.wikibooks.org/x"), campiona_paisa.gruppo("http://a.blog.it/y"),
              campiona_paisa.gruppo("http://www.comune.it/z")) == ("paisa-wikipedia", "paisa-blog", "paisa-altro-web"))


def main():
    with tempfile.TemporaryDirectory() as cartella:
        radice = pathlib.Path(cartella)
        prova_misura(radice)
        prova_da_completare_in_fondo(radice)
        prova_frasi_come_controlla_testo(radice)
        prova_campiona(radice)
    verifica("riepilogo concordato al numero",
             (riepilogo(20, 1), riepilogo(1, 0)) == ("20 prove, 1 fallita.", "1 prova, 0 fallite."))
    for descrizione in fallite:
        print("FALLITA:", descrizione)
    print(riepilogo(totale, len(fallite)))
    return 1 if fallite else 0


def riepilogo(totale, numero_fallite):
    """La riga finale, con il nome concordato al numero: «1 fallita», «0 fallite»."""
    prove = "prova" if totale == 1 else "prove"
    esito = "fallita" if numero_fallite == 1 else "fallite"
    return f"{totale} {prove}, {numero_fallite} {esito}."


if __name__ == "__main__":
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    sys.exit(main())

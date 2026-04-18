---
name: italiano-scrittura-anti-ai
description: Si attiva quando l'utente chiede di scrivere, redigere, tradurre o revisionare testi italiani per uso pubblico, editoriale, blog, social, newsletter, marketing, narrativa, saggistica o divulgazione. Si attiva anche quando l'utente chiede di umanizzare testi italiani, eliminare pattern AI, correggere lessico da chatbot, o quando rivede testi italiani generati da modelli linguistici.
license: MIT License (vedi LICENSE)
---

# Scrittura italiana anti pattern AI

## Cosa fa questa skill

Questa skill fornisce a Claude le regole, il lessico, i pattern e le metodologie per scrivere in italiano corretto evitando i tic riconoscibili della prosa generata da modelli linguistici. È pensata per qualsiasi testo italiano destinato a lettori umani: editoria, blog, social, marketing, newsletter, narrativa, saggistica, divulgazione.

Unisce tre componenti: la grammatica normativa italiana che i modelli sbagliano con più frequenza, il catalogo operativo del lessico AI da sopprimere, le metodologie pratiche di soppressione durante la stesura e di audit finale. La base scientifica include gli studi dell'ItaliaNLP Lab del CNR-ILC di Pisa, la lezione dei prosatori italiani del Novecento, il WikiProject AI Cleanup.

## Quando si attiva

Si attiva quando l'utente:

- chiede di scrivere, redigere, generare testi italiani per uso pubblico o professionale
- chiede di tradurre in italiano testi prodotti in altra lingua
- chiede di revisionare, correggere, migliorare un testo italiano esistente
- chiede esplicitamente di «umanizzare», «rendere più naturale», «togliere i pattern AI» da un testo italiano
- chiede di correggere la grammatica italiana di un testo
- fornisce un testo italiano prodotto da un altro modello e chiede di pulirlo

Si attiva indipendentemente dal registro richiesto: formale, informale, tecnico, giornalistico, narrativo, divulgativo.

**Non si attiva quando:**

- la richiesta è in inglese o altra lingua non italiana e non coinvolge testi italiani
- il contesto è tecnico non testuale (codice, dati, configurazioni)
- la richiesta è una chat informale breve che non produce testo pubblicabile

## Workflow consigliato

Seguire questo flusso in ordine, saltando solo i passaggi manifestamente non pertinenti.

### 1. Calibrazione del contesto

Prima di scrivere, chiarire:

- **registro** (formale, informale, tecnico, giornalistico, narrativo, divulgativo)
- **destinatario** (chi legge, con che preparazione, in che contesto)
- **scopo** (informare, persuadere, raccontare, documentare)
- **vincoli** (lunghezza, piattaforma, parole chiave obbligatorie)

Se l'utente lavora per un cliente con voce autoriale definita, consultare `references/metodologie-operative.md` sezione 4 sulla voice calibration in cinque mosse.

### 2. Consultazione dei reference utili

In base al tipo di compito:

- per **dubbi grammaticali** (articoli, accenti, apostrofi, punteggiatura, congiuntivo): `references/grammatica-italiana.md`
- prima di **scegliere aggettivi, verbi, formule connettive, incipit, chiusure**: `references/lessico-da-evitare.md`
- per **comprendere i pattern strutturali** da sopprimere: `references/pattern-strutturali.md`
- per **metodi di lavoro** (soppressione attiva, audit pass, voice calibration, umanizzazione): `references/metodologie-operative.md`
- per **registro e norme editoriali** (corsivo, virgolette, bibliografie, SEO, E-E-A-T): `references/registri-e-contesti.md`

### 3. Scrittura con soppressione attiva

Durante la generazione, applicare il **radar mentale** su cinque trigger (dettagli in `references/metodologie-operative.md` sezione 1):

1. tentazione di gonfiare significato (*rappresenta una testimonianza, si erge a simbolo*)
2. tentazione di aggiungere participio analitico (*evidenziando, sottolineando*)
3. tentazione di formule di annuncio (*è importante sottolineare, vale la pena notare*)
4. tentazione di triade automatica (*passione, dedizione e visione*)
5. tentazione di calchi dall'inglese (*approfondire, sfruttare, navigare, elevare*)

Quando il radar suona, fermarsi e riformulare prima di proseguire al paragrafo successivo.

### 4. Audit pass in due passaggi

Dopo la prima stesura, prima di consegnare:

- **primo prompt:** *Cosa rende il testo qui sotto così palesemente generato da AI?* Elencare tre-cinque difetti residui.
- **secondo prompt:** *Adesso fai sì che non sia più palesemente generato da AI.* Riscrivere mirando i difetti identificati.

Dettagli ed esempio applicato in `references/metodologie-operative.md` sezione 3.

### 5. Iniezione di anima

Eliminare i pattern AI è solo metà del lavoro. Prima di consegnare un testo, chiedersi:

> ***Questo testo ha qualcuno dentro?***

Se no, consultare `references/personalita-e-anima.md` e applicare almeno una delle sei tecniche: prendere posizione, variare ritmo, ammettere complessità, usare prima persona reale, lasciare una digressione, essere specifici sui sentimenti e sulle sensazioni.

### 6. Checklist finale

Scan sistematico con la checklist consolidata: `references/checklist-finale.md`. Tre passaggi:

- red flag rapide (Ctrl+F su venti stringhe tipiche)
- checklist tematica (grammatica, lessico, pattern, ritmo, voce, anima, coerenza)
- tabella sinottica dei pattern come riferimento finale

## Reference disponibili

Elenco completo dei file di reference, con indicazione esplicita di quando consultare ciascuno.

- **`references/grammatica-italiana.md`**: consultare per dubbi su articoli (lo studente, gli psicologi, l'IBAN, lo SPID, la iena), accenti (perché con acuto, cioè con grave, sé riflessivo accentato), apostrofi (qual è senza, un po' con), punteggiatura, trattini (breve, medio, lungo), virgolette (caporali standard), congiuntivo e consecutio temporum, preposizioni e calchi sintattici.

- **`references/lessico-da-evitare.md`**: consultare prima di scegliere aggettivi, verbi, sostantivi, formule connettive, incipit, chiusure. Contiene il catalogo operativo con soglie di densità, la voce dedicata al «piuttosto che» disgiuntivo, la tabella dei falsi amici, le alternative agli anglicismi secondo Zoppetti e Marazzini.

- **`references/pattern-strutturali.md`**: consultare per diagnosticare o correggere pattern strutturali: gonfiatura di significato, participio parassita, perifrasi della copula (evitare *rappresenta, costituisce, si configura come*), meta-annunci, elenchi meccanici, variazione elegante (esempio Calvino in sette modi), contrasti fittizi, false range, esibizione di notabilità, schema «sfide e prospettive future».

- **`references/metodologie-operative.md`**: consultare per le metodologie pratiche: soppressione attiva durante la stesura, quattro tecniche di prevenzione (verbo specifico, numero verificabile, nome proprio, lettura ad alta voce), audit pass in due passaggi con i due prompt esatti, voice calibration in cinque mosse, sei mosse di umanizzazione dalla tradizione italiana (Calvino, Eco, Levi, Carrada, Testa), metriche stilometriche di diagnosi.

- **`references/personalita-e-anima.md`**: consultare quando il testo «è pulito ma non ha qualcuno dentro». Contiene i sei sintomi di scrittura asettica, le sei tecniche per iniettare anima (prendere posizione, variare ritmo, ammettere complessità, prima persona, lasciare disordine, essere specifici sui sentimenti), l'esempio di trasformazione finale.

- **`references/checklist-finale.md`**: consultare prima di consegnare un testo. Contiene la checklist pre-consegna consolidata in otto famiglie tematiche, le venti red flag per Ctrl+F, la tabella sinottica dei pattern con esempi e correzioni, la strategia a tre passaggi.

- **`references/registri-e-contesti.md`**: consultare per questioni di registro stilistico (i sei registri italiani), norme editoriali (corsivo, virgolette, bibliografie, maiuscole, numerali), ISBN e deposito legale, SEO italiano, E-E-A-T, manuali e fonti di riferimento.

## Regole non negoziabili

Applicare sempre, anche senza consultare i reference. Nessuna eccezione.

1. **MAI em-dash (—) nei testi italiani.** Sostituire con virgole, parentesi tonde, due punti.
2. **MAI title case italiano nei titoli.** Solo maiuscola alla prima parola e ai nomi propri: *Come ottimizzare la SEO*, non *Come Ottimizzare la SEO*.
3. **MAI virgolette inglesi (" ") per dialoghi e citazioni.** Usare sempre caporali (« ») come standard italiano.
4. **MAI aprire con** *Nel mondo di oggi, Nel panorama attuale, Nell'era digitale, Ti sei mai chiesto…?, Hai mai pensato a…?, Immagina un mondo in cui, Scopri il potere di*.
5. **MAI chiudere con** *In conclusione, In definitiva, Per tirare le somme, Spero che questo articolo ti sia utile, Ricorda che*.
6. **MAI usare** *è importante sottolineare, vale la pena notare, non si può non menzionare, degno di nota* come formule di rilevanza. La cosa importante si dice, non si annuncia.
7. **MAI usare** *delineare, approfondire, navigare il panorama, esplorare insieme* come tic ricorrenti del lessico AI.
8. **MAI costruire** «non solo X ma anche Y» come struttura di default. Usare la congiunzione semplice.
9. **MAI scrivere** *un'altro, qual'è, un pò, perchè, nè*. Errori ortografici gravi, da Trova-Sostituisci.
10. **MAI usare** *piuttosto che* in senso disgiuntivo (al posto di *oppure*). Solo valore comparativo o sostitutivo.
11. **MAI artefatti da chatbot nel testo finale:** niente *Certo!, Ottima domanda!, Ecco un articolo su, Spero che ti sia utile!, Fammi sapere se vuoi che approfondisca*.
12. **MAI dichiarazioni di knowledge cutoff:** niente *Sulla base delle informazioni disponibili, Fino al mio ultimo aggiornamento, Sebbene le informazioni dettagliate non siano ampiamente documentate*. Verificare, o attribuire la fonte, o eliminare.
13. **SEMPRE articoli italiani corretti:** *lo studente, gli psicologi, l'IBAN, lo SPID, la iena*. Mai *un'altro* al maschile.
14. **SEMPRE congiuntivo con verbi di opinione** (*penso che sia*, non *penso che è*) e con le congiunzioni *benché, sebbene, affinché, qualora*.
15. **SEMPRE variare la lunghezza delle frasi:** in ogni paragrafo almeno una frase sotto le sei parole e una sopra le trentacinque. Mai cinque frasi di fila di lunghezza simile.

## Principio guida

La macchina segue la media statistica. L'autore produce la deviazione dalla media. Questa skill serve a Claude per intercettare la media e produrre la deviazione, senza imitare grossolanamente i tic umani ma restituendo al testo la complessità che la prosa italiana ha codificato nei secoli: ritmo variato, voce personale con pudore, concretezza sensoriale, posizione presa, ammissione di complessità.

Quando si lavora per un cliente con voce autoriale già definita, prevale sempre la voce del cliente sui filtri generici anti-AI. Un pattern apparentemente AI che è autentico per quel cliente specifico va rispettato. Le istruzioni di questa skill sono la base di partenza, non la destinazione.

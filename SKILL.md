---
name: italiano-scrittura-anti-ai
description: Si attiva quando l'utente chiede di scrivere, redigere, tradurre o revisionare testi italiani per uso pubblico, editoriale, blog, social, newsletter, marketing, narrativa, saggistica o divulgazione. Si attiva anche quando l'utente chiede di umanizzare testi italiani, eliminare pattern AI, correggere lessico da chatbot, catturare o calibrare la voce di un autore su un corpus di suoi testi, rispondere a un rilevatore automatico che ha segnalato come generato un testo scritto da una persona, o quando rivede testi italiani generati da modelli linguistici.
---

# Scrittura italiana anti pattern AI

## Cosa fa questa skill

Questa skill è una suite di lavoro sull'italiano scritto, e insieme un sistema avanzato contro la firma della prosa generata. Serve per cinque compiti distinti, e vale per qualsiasi testo destinato a lettori umani: editoria, blog, social, marketing, newsletter, narrativa, saggistica, divulgazione.

1. **Scrivere** un testo italiano nuovo secondo la norma, applicata durante la stesura invece che controllata dopo.
2. **Correggere e rivedere** un testo già scritto, da chiunque sia stato scritto: bozze, articoli, tesi, relazioni, capitoli.
3. **Tradurre** verso l'italiano senza i calchi lessicali e sintattici che l'originale suggerisce.
4. **Catturare e rispettare la voce** di chi firma il testo, propria o di un cliente.
5. **Difendere un testo umano** segnalato come generato da un rilevatore automatico.

Il materiale è lo stesso per tutti e cinque, ed è la ragione per cui la skill funziona su un testo umano esattamente come su un testo generato: la grammatica normativa che i modelli sbagliano più spesso, il catalogo operativo del lessico da sopprimere, i pattern strutturali, i sei registri con le loro norme editoriali, il ritmo e l'anima del testo, e i segnali stilometrici con base peer-reviewed. Togliere i tic della prosa generata è una conseguenza di questo lavoro, non il suo perimetro.

La base scientifica include gli studi dell'ItaliaNLP Lab del CNR-ILC di Pisa, la lezione dei prosatori italiani del Novecento, il WikiProject AI Cleanup.

## Quando si attiva

Si attiva quando l'utente:

- chiede di scrivere, redigere, generare testi italiani per uso pubblico o professionale
- chiede di tradurre in italiano testi prodotti in altra lingua
- chiede di revisionare, correggere, migliorare un testo italiano esistente
- chiede esplicitamente di «umanizzare», «rendere più naturale», «togliere i pattern AI» da un testo italiano
- chiede di correggere la grammatica italiana di un testo
- fornisce un testo italiano prodotto da un altro modello e chiede di pulirlo
- chiede aiuto per rispondere a un rilevatore automatico che ha segnalato come generato un testo scritto da lui, o riferisce un'accusa arrivata da un docente, un committente, una redazione
- chiede di catturare, documentare o calibrare la voce di un autore a partire da un corpus di suoi testi, propri o di un cliente

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

Se l'utente lavora per un cliente con voce autoriale definita, consultare `references/metodologie-operative.md` sezione 4 sulla voice calibration in cinque mosse. Quando la voce va catturata e documentata sul serio, con un corpus di testi veri, il metodo completo e il modello di scheda sono in `references/voce-personale.md`.

### 2. Consultazione dei reference utili

In base al tipo di compito:

- per **dubbi grammaticali** (articoli, accenti, apostrofi, punteggiatura, congiuntivo): `references/grammatica-italiana.md`
- prima di **scegliere aggettivi, verbi, formule connettive, incipit, chiusure**: `references/lessico-da-evitare.md`
- per **comprendere i pattern strutturali** da sopprimere: `references/pattern-strutturali.md`
- per **metodi di lavoro** (soppressione attiva, audit pass, voice calibration, umanizzazione): `references/metodologie-operative.md`
- per **registro e norme editoriali** (corsivo, virgolette, bibliografie, SEO, E-E-A-T): `references/registri-e-contesti.md`
- per **i segnali con base scientifica** (varietà lessicale, pronomi, emozioni, interiorità, sottotesto) quando serve qualcosa di più affidabile delle liste di parole: `references/segnali-misurabili.md`
- quando il testo **parla al lettore come se rispondesse in chat** (negazioni preventive, suspense inutile, riassunti di sé stesso): `references/leak-conversazionale.md`
- quando un **paragrafo suona piatto e non si capisce perché**, per diagnosticare quale canale del lettore si è rotto: `references/canali-lettore-saggistica.md`
- quando serve **imparare la deviazione fatta bene, oltre a evitare i tic**, con una galleria di mosse d'autore italiane da rubare: `references/maestri-della-deviazione.md`
- quando si scrive **per conto di una persona con una voce riconoscibile**, o si vuole documentare la propria: `references/voce-personale.md`
- quando un **testo dell'utente viene segnalato come generato** da un rilevatore automatico e serve costruire la risposta: `references/scudo-falsi-positivi.md`

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

- **`references/metodologie-operative.md`**: consultare per le metodologie pratiche: soppressione attiva durante la stesura, quattro tecniche di prevenzione (verbo specifico, numero verificabile, nome proprio, lettura ad alta voce), audit pass in due passaggi con i due prompt esatti, voice calibration in cinque mosse, sei mosse di umanizzazione dalla tradizione italiana (Calvino, Eco, Levi, Camilleri), metriche stilometriche di diagnosi.

- **`references/personalita-e-anima.md`**: consultare quando il testo «è pulito ma non ha qualcuno dentro». Contiene i sei sintomi di scrittura asettica, le sei tecniche per iniettare anima (prendere posizione, variare ritmo, ammettere complessità, prima persona, lasciare disordine, essere specifici sui sentimenti), l'esempio di trasformazione finale, e la guardia contro il finto-umano di plastica (over-humanizing).

- **`references/maestri-della-deviazione.md`**: consultare per imparare la deviazione dalla media dai maestri, oltre che per evitare il negativo. Galleria di sette scrittori italiani (Calvino, Eco, Levi, Ginzburg, Testa, Camilleri, Carrada), ognuno con una mossa-firma, un passo che la mostra e la regola per portarla via. Ribalta l'asse della sezione 5 di `metodologie-operative.md`, che indicizza le mosse per tecnica, partendo qui dall'autore. Include l'avvertenza a rubare la mossa, non a imitare l'autore.

- **`references/voce-personale.md`**: consultare quando la voce di chi firma il testo va catturata e rispettata, per un cliente o per sé stessi. Contiene il metodo di raccolta del corpus, i due livelli del profilo (misurato e osservato), il modello di scheda voce con un esempio compilato su dati reali, le istruzioni per usare il profilo mentre si scrive, e il confine oltre il quale la voce non prevale: le regole non negoziabili sono norma della lingua, non gusto, e nessuno ha una voce fatta di errori. Espande la sezione 4 di `metodologie-operative.md`.

- **`references/checklist-finale.md`**: consultare prima di consegnare un testo. Contiene la checklist pre-consegna consolidata in undici famiglie tematiche più la verifica finale, le venti red flag per Ctrl+F, la tabella sinottica dei pattern con esempi e correzioni, la strategia a tre passaggi.

- **`references/registri-e-contesti.md`**: consultare per questioni di registro stilistico (i sei registri italiani), norme editoriali (corsivo, virgolette, bibliografie, maiuscole, numerali), ISBN e deposito legale, SEO italiano, E-E-A-T, manuali e fonti di riferimento.

- **`references/segnali-misurabili.md`**: consultare quando le liste di parole non bastano e serve un criterio più solido. Contiene i segnali anti-AI con base peer-reviewed (varietà lessicale via MATTR, densità di pronomi personali, eccesso di emozioni positive, interiorità superficiale, basso sottotesto, template sintattici), come si riconoscono e si misurano, e il declassamento delle liste di parole a preferenza di gusto. Riporta le fonti scientifiche (Kobak 2024, Shaib 2024).

- **`references/leak-conversazionale.md`**: consultare quando il testo scivola nel registro della chat invece di stare in piedi come documento. Contiene il pattern di negazione che corregge un equivoco inesistente (*non è X, è Y*), la suspense inutile (*qui sta il punto*), i riassunti frattali, le domande messe in bocca al lettore, e la correzione alla radice (scrivere per chi legge, non per la conversazione).

- **`references/canali-lettore-saggistica.md`**: consultare come griglia diagnostica quando un paragrafo suona piatto. Contiene i quattro canali attraverso cui il lettore gode di un testo (fiducia nel lettore, piacere estetico, trasporto, fluidità), adattati alla saggistica e alla divulgazione, con la tabella per capire quale canale si è rotto. Riporta le fonti scientifiche (van Laer 2014, Thissen 2018).

- **`references/scudo-falsi-positivi.md`**: consultare quando un testo italiano scritto da una persona viene segnalato come generato da un rilevatore automatico. Contiene il confine d'uso della difesa, che cosa misura davvero un rilevatore, le evidenze pubblicate sui suoi errori (Liang 2023, Weber-Wulff 2023, il ritiro dell'AI Text Classifier di OpenAI, le cifre dichiarate da Turnitin, la scelta di Vanderbilt), il vuoto di misure sull'italiano documentato dai benchmark multilingue, i sette passaggi della difesa e i due modelli di documento: difesa argomentata per il testo dell'autore, dichiarazione d'uso per il testo assistito.

## Strumenti inclusi

La skill include uno strumento facoltativo e le sue prove automatiche. Chi non ha Python installato usa la skill per intero senza perdere nulla: i reference spiegano come ottenere gli stessi risultati a mano.

- **`scripts/profilo_voce.py`**: calcola il profilo quantitativo di una voce a partire da una cartella di testi dello stesso autore e dello stesso registro. Produce una scheda leggibile e i dati grezzi in JSON. Si invoca con `python scripts/profilo_voce.py CARTELLA --nome "Nome autore"` e non richiede librerie esterne. Le decisioni di conteggio, i limiti e il modo di leggere i numeri sono in `references/voce-personale.md`. Lo strumento misura e non giudica: non stabilisce se un testo sia stato generato da una macchina.

- **`scripts/prova_profilo_voce.py`**: le prove automatiche dello strumento, una per ogni difetto trovato durante l'audit e corretto, così che non torni. Si lanciano con `python scripts/prova_profilo_voce.py`, non richiedono librerie esterne, e girano anche in continua a ogni push e pull request. Servono a chi contribuisce, non all'uso quotidiano.

- **`extras/commands/calibra-voce.md`**: comando `/calibra-voce` da copiare in `.claude/commands/`. Conduce l'intera calibrazione: verifica del corpus, livello misurato con lo script, livello osservato con la lettura dei testi, scheda finale. Istruzioni di installazione in `extras/README.md`.

- **`extras/commands/difendi.md`**: comando `/difendi` da copiare in `.claude/commands/`. Raccoglie i fatti dell'accusa, distingue i tre casi, verifica i materiali dell'autore e compone il documento. Non esegue alcuno strumento sul testo contestato e non indica modifiche per abbassare un punteggio. Istruzioni di installazione in `extras/README.md`.

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

## Limite d'uso

Questa skill serve a scrivere in italiano senza i tic della prosa generata, e a difendere un testo umano accusato ingiustamente da un rilevatore automatico (`references/scudo-falsi-positivi.md`). Non serve a far passare per umano un testo generato, e non contiene niente che aiuti a farlo. Nessuno strumento certifica la paternità umana di un testo, nemmeno questo: la difesa si regge su prove esterne al testo, e chi volesse difendere un testo generato quei campi li troverebbe vuoti. Quel limite però tiene per la forma del documento, non per un controllo tecnico: niente qui verifica la data o la provenienza dei materiali che l'utente porta, e la parte che regge davvero è il colloquio dal vivo, dove si risponde riga per riga.

## Principio guida

La macchina segue la media statistica. L'autore produce la deviazione dalla media. Questa skill serve a Claude per intercettare la media e produrre la deviazione, senza imitare grossolanamente i tic umani ma restituendo al testo la complessità che la prosa italiana ha codificato nei secoli: ritmo variato, voce personale con pudore, concretezza sensoriale, posizione presa, ammissione di complessità.

Quando si lavora per un cliente con voce autoriale già definita, prevale sempre la voce del cliente sui filtri generici anti-AI. Un pattern apparentemente AI che è autentico per quel cliente specifico va rispettato. Le istruzioni di questa skill sono la base di partenza, non la destinazione.

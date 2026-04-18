# Metodologie operative

Questo file raccoglie le metodologie pratiche per produrre testi italiani che non suonino generati da AI. Diverso dai file sui pattern (`pattern-strutturali.md`) e sul lessico (`lessico-da-evitare.md`), qui si tratta di **come si lavora**, non di **cosa si evita**.

Le metodologie sono cinque: un workflow di soppressione durante la stesura, quattro tecniche di prevenzione attiva, l'audit pass in due passaggi, la voice calibration per allinearsi alla voce di un cliente, le sei mosse di umanizzazione dalla tradizione italiana. Chiude una sezione sulle metriche stilometriche che servono da diagnostica rapida.

Le fonti principali sono lo skill Humanizer del WikiProject AI Cleanup, *Le lezioni americane* di Calvino, *Come si fa una tesi di laurea* di Eco, *L'altrui mestiere* di Levi, le opere di Luisa Carrada e Annamaria Testa, lo studio dell'ItaliaNLP Lab del CNR-ILC di Pisa per le metriche italiane.

## Indice

1. [Soppressione attiva durante la stesura](#1-soppressione-attiva-durante-la-stesura)
2. [Quattro tecniche di prevenzione](#2-quattro-tecniche-di-prevenzione)
3. [Audit pass in due passaggi](#3-audit-pass-in-due-passaggi)
4. [Voice calibration in cinque mosse](#4-voice-calibration-in-cinque-mosse)
5. [Sei mosse di umanizzazione dalla tradizione italiana](#5-sei-mosse-di-umanizzazione-dalla-tradizione-italiana)
6. [Metriche stilometriche di diagnosi](#6-metriche-stilometriche-di-diagnosi)

---

## 1. Soppressione attiva durante la stesura

La strategia più efficace non è eliminare i pattern AI in fase di revisione, ma sopprimerli al momento del concepimento della frase. Una volta entrati nel registro AI gonfio, è difficile uscirne nello stesso testo.

Il workflow si articola in tre fasi.

### Fase uno: monitoraggio attivo

Mentre si scrive (o mentre si revisiona output AI in tempo reale), si tiene attivo un radar mentale per cinque famiglie di trigger:

1. **Tentazione di gonfiare significato** (*rappresenta una testimonianza, si erge a simbolo, lascia un'impronta*)
2. **Tentazione di aggiungere participio analitico** (*evidenziando, sottolineando, configurandosi come*)
3. **Tentazione di usare formule di annuncio** (*è importante sottolineare, è fondamentale ricordare, vale la pena notare*)
4. **Tentazione di costruire la triade automatica** (*passione, dedizione e visione*)
5. **Tentazione di calchi dall'inglese** (*approfondire, sfruttare, navigare, elevare*)

Quando il radar suona, ci si ferma a metà frase e si riformula.

### Fase due: riscrittura immediata

Quando si è scritto un pattern AI, prima di proseguire al prossimo paragrafo, si torna indietro:

- si cancella
- ci si chiede *che cosa volevo davvero dire?*
- si riscrive nella propria voce
- si prosegue

Aspettare la revisione finale è inefficiente perché i pattern si rinforzano paragrafo dopo paragrafo.

### Fase tre: controllo pre-consegna

Prima di consegnare al cliente o pubblicare, si esegue lo scan finale con la checklist consolidata (vedi `checklist-finale.md`). Non sostituisce le due fasi precedenti, le completa.

## 2. Quattro tecniche di prevenzione

Strumenti operativi per intercettare un pattern AI al momento della scrittura, prima che diventi parte del testo.

### Tecnica del verbo specifico

Quando si è tentati di scrivere *evidenzia, sottolinea, mette in luce, rivela, dimostra, configura*, ci si chiede se il soggetto della frase può davvero compiere quell'azione. Un decreto non *evidenzia*, un dato non *dimostra*, un evento non *sottolinea*. Sono il narratore artificiale che attribuisce intenzionalità a oggetti inanimati.

**Sostituzioni concrete:**

- il decreto *introduce, vieta, modifica, abroga*
- il dato *risulta, supera, scende, cresce*
- l'evento *coincide con, segue, anticipa*

### Tecnica del numero verificabile

Quando si è tentati di scrivere un aggettivo intensificatore (*significativo, notevole, sostanziale, importante*), ci si chiede se esiste un numero che lo sostituisca. Se c'è, lo si cerca e lo si inserisce.

- *crescita significativa* diventa *+18% sull'anno precedente*
- *notevole successo* diventa *terzo posto in classifica per quattro settimane*
- *un pubblico considerevole* diventa *12.000 spettatori paganti*

Se il numero non esiste, l'aggettivo era retorico e va eliminato.

### Tecnica del nome proprio

Quando si è tentati di scrivere *diversi esperti, alcuni studi, vari osservatori*, ci si chiede se si è in grado di citarne uno con nome e cognome.

- Se sì, si cita: *Lo studio di Goyal-Singh pubblicato su JAMA nel 2014…*
- Se no, si elimina la pseudo-attribuzione e si presenta l'affermazione come propria, oppure non la si fa

### Tecnica della lettura ad alta voce

Dopo ogni paragrafo, si rilegge a voce alta. I pattern AI italiani hanno un suono caratteristico: cadenza uniforme, periodi di lunghezza simile, mancanza di inciampi. Una prosa italiana umana ha esitazioni, affondi, pause inattese.

Se la lettura scorre senza sussulti per più di cinque frasi consecutive, c'è un problema di burstiness troppo bassa (vedi sezione 6). Si introduce volutamente una frase corta, una inversione marcata, una parentetica.

## 3. Audit pass in due passaggi

È il metodo operativo più potente dello skill Humanizer e merita di essere replicato su ogni testo di una certa importanza. Si articola in due prompt esatti da eseguire dopo aver scritto la prima bozza.

### Primo prompt

> *Cosa rende il testo qui sotto così palesemente generato da AI?*

Si elenca onestamente, in tre-cinque punti, cosa ancora suona artificiale:

- ritmo troppo uniforme
- citazioni sospette o placeholder
- chiusura un po' slogan
- congiunzioni meccaniche
- abuso di una parola
- schema retorico ripetuto
- mancanza di voce personale

### Secondo prompt

> *Adesso fai sì che non sia più palesemente generato da AI.*

Si riscrive correggendo specificamente i tre-cinque punti emersi nel primo passaggio.

### Perché funziona

La prima revisione tradizionale (rileggere e correggere) è troppo generica: si tende a vedere errori di battitura e refusi, non pattern strutturali. Il prompt esplicito *cosa lo rende AI* costringe a guardare con un occhio specifico per i tic algoritmici. La seconda riscrittura mirata è più chirurgica di una riscrittura generale.

### Esempio applicato

**Bozza iniziale:**

> «Scrivere un buon articolo di marketing digitale è un processo che richiede attenzione a diversi aspetti. È fondamentale curare il titolo, scegliere le parole chiave giuste e investire in una struttura chiara. Solo seguendo questi passaggi è possibile ottenere risultati significativi nel mercato italiano.»

**Risposta al primo prompt:**

1. ritmo uniforme con tre frasi della stessa lunghezza
2. *fondamentale, significativi* sono parole-spugna
3. *diversi aspetti* è quantificatore vago
4. la costruzione *solo seguendo… è possibile* è formula AI tipica
5. zero voce personale, zero numeri concreti

**Risposta al secondo prompt (riscrittura):**

> «Scrivere un buon articolo di marketing digitale non è difficile. Lo è farlo bene. Tre cose contano davvero: un titolo che superi i sei secondi di soglia attenzione (dati Microsoft 2022), le parole chiave nelle prime cento parole, una struttura a tre livelli massimi. Il resto è dettaglio. Lo dico dopo diversi anni di pubblicazioni con tassi di lettura molto diversi a seconda di quanto rispettavo questi tre punti.»

Differenze: ritmo variato (frase di sette parole, frase di quattro parole, periodo medio, periodo lungo), zero parole-spugna, numero verificabile con fonte, parentetica con tono diretto, prima persona dichiarativa con esperienza.

### Regola operativa

Integrare il doppio prompt come ultimo passaggio prima di consegnare o pubblicare. Non saltarlo mai sui testi importanti.

## 4. Voice calibration in cinque mosse

Quando si scrive per un cliente, prima di applicare qualsiasi tecnica anti-AI bisogna **calibrare la voce sul cliente specifico**. Le checklist generiche di umanizzazione, applicate senza calibrazione, producono testi neutri e impersonali quanto i testi AI puri. La voce del cliente è il vero anti-AI.

### Prima mossa: raccolta del corpus

Prima di scrivere una sola riga, raccogliere tre-cinque testi precedenti dell'autore o del cliente: post di blog, articoli, email lunghe, capitoli di libri. Vanno bene anche bozze non pubblicate purché autentiche. Servono almeno duemila parole totali.

### Seconda mossa: analisi quantitativa rapida

Misurare quattro parametri:

1. **Lunghezza media di frase** (contando le parole)
2. **Deviazione standard della lunghezza di frase**: alta (burstiness alta, stile variato) o bassa (burstiness bassa, stile monotono)
3. **Densità di subordinate**: paratattico (frasi brevi coordinate) o ipotattico (frasi lunghe con subordinate)
4. **Uso della prima persona**: io che dichiara opinioni, noi inclusivo, impersonale?

Sono numeri grezzi che restituiscono il «metro respiratorio» dell'autore.

### Terza mossa: analisi qualitativa

Annotare cinque tic riconoscibili. Esempi:

- usa molti incisi tra trattini medi?
- inizia spesso le frasi con *e* o *ma*?
- ha parole-feticcio (*sostanzialmente, di fatto, per davvero*)?
- apre i paragrafi con domande?
- chiude con sentenze brevi?
- usa metafore ricorrenti?
- cita sempre fonti per nome o resta sulle generalizzazioni?

### Quarta mossa: analisi del registro

Stabilire dove si colloca il testo del cliente fra quattro posizioni:

1. **Formale puro** (atti, accademia, normativa)
2. **Formale colloquiale** (saggistica divulgativa, giornalismo culturale)
3. **Informale colto** (blog di qualità, newsletter curate)
4. **Informale popolare** (social, intrattenimento)

Lo stesso autore può variare registro fra contesti, quindi calibrare per contesto specifico.

### Quinta mossa: applicazione coerente

Quando si scrive il nuovo testo, riprodurre i quattro parametri quantitativi e i cinque tic qualitativi.

- Se l'autore scrive frasi corte, non produrre periodi lunghi anche se sarebbero «più variati»
- Se l'autore usa *cosa* invece di *aspetto*, non fare upgrade lessicale a *elemento*
- Se l'autore non usa mai la prima persona, non introdurla

### Esempio applicato

**Cliente:** avvocato penalista cinquantenne che scrive newsletter mensili per i clienti.

**Analisi del corpus:**

- frasi medie 18-22 parole con bassa deviazione standard (cadenza uniforme professionale)
- alta ipotassi (subordinate causali e concessive frequenti)
- nessun uso della prima persona singolare (sempre *lo studio, l'avvocato, la nostra esperienza*)
- tic ricorrente *occorre sottolineare*: anche questo che sembra AI è un suo tic professionale autentico, verificato in cinque newsletter
- registro formale-colloquiale
- citazione sistematica di sentenze per esteso

**Risultato:** quando si scrive una nuova newsletter per lui, si rispetta tutto questo. *Occorre sottolineare* resta, perché è la sua voce. Le frasi corte e dirette in stile blog di startup andrebbero rifiutate dal cliente come fuori registro.

### Regola operativa

La voce del cliente prevale sempre sui filtri anti-AI generici. Un pattern apparentemente AI che è autentico per quel cliente specifico va rispettato. Un pattern apparentemente neutro che il cliente non userebbe mai va eliminato.

## 5. Sei mosse di umanizzazione dalla tradizione italiana

Umanizzare un testo non significa aggiungere errori controllati. Significa restituire al testo la complessità che la prosa italiana ha codificato nei secoli: oscillazione fra paratassi e ipotassi, uso degli incisi, voce personale modulata dal pudore, varietà di registri, concretezza delle immagini.

Le sei mosse derivano dalla lezione di Calvino, Eco, Levi, Carrada, Testa, Severgnini.

### Prima mossa: variazione della lunghezza delle frasi

In ogni paragrafo, almeno una frase sotto le sei parole e una sopra le trentacinque. La deviazione standard target è 8-12 parole; quella da fuggire è 3-5.

Calvino nelle *Città invisibili* scrive: «D'una città non godi le sette o settantasette meraviglie, ma la risposta che dà a una tua domanda». Diciassette parole, una sola frase, inquadrata da periodi più ampi. La «burstiness» applicata all'italiano è l'esplosività ritmica del periodo umano.

### Seconda mossa: uso degli incisi e delle parentesi

L'italiano colto predilige la sintassi a intarsio, con glosse racchiuse fra virgole, trattini medi o parentesi tonde (mai em-dash). Eco ne è il maestro.

Un paragrafo su due dovrebbe avere un inciso, uno su quattro una parentesi. Esempio:

> «Calvino, che pure non amava le definizioni rigide, propose nelle *Lezioni americane* sei valori (in realtà cinque, perché la sesta lezione, quella sulla *Consistency*, non fece in tempo a scriverla) destinati a diventare il manifesto involontario della scrittura italiana del nuovo millennio.»

Un periodo che il modello AI non scrive, perché evita per statuto la sintassi a scatole cinesi.

### Terza mossa: voce personale con pudore

L'italiano colto non si nasconde dietro l'impersonalità burocratica ma non esibisce l'io: fa capolino, si manifesta con formule attenuate.

**Formule di opinione misurata:**

*a mio avviso, mi pare, trovo che, direi, ho l'impressione che, se posso azzardare, non so se sbaglio ma, mi sono chiesto a lungo se*

In un testo di media lunghezza, due o tre formule di opinione distribuite senza concentrazione. Non di più, non di meno.

### Quarta mossa: espressioni idiomatiche con misura

**Esempi utilizzabili:**

*prendere la palla al balzo, non avere peli sulla lingua, mettere le carte in tavola, tagliare la testa al toro, gettare la spugna, darsela a gambe, cercare il pelo nell'uovo, fare buon viso a cattivo gioco, predicare bene e razzolare male, dormire sugli allori, battere il ferro finché è caldo, prendere due piccioni con una fava*

Uno o due per testo divulgativo di tremila parole sono il punto di equilibrio; cinque diventano caricatura; zero appiattiscono.

I proverbi (*Chi va piano va sano e va lontano, Il buongiorno si vede dal mattino, Tra il dire e il fare c'è di mezzo il mare*) con ancora maggiore parsimonia.

### Quinta mossa: rotture della struttura prevedibile

Inversioni marcate, dislocazioni, frasi nominali, aperture con congiunzione. Sono strutture perfettamente ammesse nella prosa italiana di qualità, nonostante i vecchi divieti scolastici, e registrate dalla Treccani come centrali nella sintassi dell'italiano contemporaneo. Calvino, Eco, Levi, Sciascia, Camilleri, Morante le usano sistematicamente.

**Inversione marcata:** *Semplice, la soluzione.*

**Dislocazione a sinistra:** *Questa cosa, non l'ho mai capita.*

**Dislocazione a destra:** *Non l'ho mai capita, questa cosa.*

**Frasi nominali:** *Silenzio. Attesa. Poi, finalmente, la risposta.*

**Domande retoriche nella prosa:** *E allora? Davvero? E che ne sappiamo, noi?*

**Aperture con congiunzione:** *E, Ma, Però, Anche, Eppure.*

### Sesta mossa: regionalismi misurati e riferimenti culturali

Parole come *magari, fregare, scocciare* sono ormai standard. Altre restano regionali ma espressive: *garbare* toscano, *uggia* toscano, *scugnizzo* napoletano, *schei* veneto, *taliare* siciliano, *camurrìa* siciliano, *pirla* milanese.

Camilleri mostra come il dialetto, integrato con misura, sia risorsa stilistica, non folclore. I riferimenti culturali italiani (letterari, artistici, storici) vivono sotto voce: *quel ramo del lago di Como* è citazione riconosciuta senza essere dichiarata; *il sistema periodico* evoca Levi senza nominarlo.

### Sintesi dalle *Lezioni americane* di Calvino

Le cinque proposte calviniane completate prima della morte del 1985 sono il manifesto involontario della scrittura italiana per il nuovo millennio:

- **Leggerezza:** sottrazione di peso. Eliminare gli aggettivi pesanti (*epocale, senza precedenti, fondamentale*) e sostituirli con dettagli concreti che illuminino.
- **Rapidità:** densità, non velocità. Tagliare le perifrasi (*è importante notare che, vale la pena sottolineare*).
- **Esattezza:** lessico preciso contro genericità. Non *cose, aspetti, questioni, elementi, fattori, dinamiche, tematiche*, ma *la lentezza dei tribunali, la confusione delle leggi, il costo degli avvocati*.
- **Visibilità:** capacità di mettere a fuoco immagini concrete. Dove il modello scrive *la situazione economica era difficile*, l'autore scrive *al supermercato, davanti agli scaffali, contava le monete*.
- **Molteplicità:** varietà di registri, voci, prospettive. Un testo lungo non ha un solo tono.

### Sintesi da Eco e Levi

Eco in *Come si fa una tesi di laurea* (Bompiani 1977) offre la regola lapidaria: «Non siete Proust. Non fate periodi lunghi. Non siete e.e. cummings. Non usate puntini di sospensione, punti esclamativi e non spiegate le ironie». Spezzare i periodi lunghi, ripetere il soggetto invece di accumulare pronomi, avere il coraggio dell'asserzione.

Levi in *Dello scrivere oscuro* (*L'altrui mestiere*, Einaudi 1985) denuncia lo stile oscuro come forma di arroganza: «Sta allo scrittore farsi capire da chi desidera capirlo: è il suo mestiere, scrivere è un servizio pubblico, e il lettore volonteroso non deve andare deluso». La scrittura è etica prima che estetica.

## 6. Metriche stilometriche di diagnosi

Dal punto di vista quantitativo, un testo italiano generato da un LLM presenta una firma statistica riconoscibile. Conoscerla aiuta a diagnosticare rapidamente un testo e a calibrare la revisione.

Le fonti sono gli studi dell'ItaliaNLP Lab del CNR-ILC di Pisa (Dell'Orletta, Montemagni, Venturi, Brunato) e la produzione CLiC-it 2024.

### Indice Gulpease

Elaborato nel 1988 da Lucisano e Piemontese (Sapienza) con la formula:

*Gulpease = 89 + (300 × frasi − 10 × lettere) / parole*

Misura la leggibilità. Valori tipici della prosa GPT generalista: 50-62, superiori al giornalismo italiano (48-55), inferiori alla divulgazione semplice (70-75).

Il marcatore decisivo non è il valore medio, ma la sua **omogeneità**: la deviazione standard del Gulpease fra passaggi di uno stesso articolo umano oscilla fra 6 e 10 punti, mentre nei testi AI scende sotto 3-4 punti.

Strumenti per calcolarlo: Corrige.it, Due Parole.

### Burstiness e lunghezza di frase

La **burstiness** misura la variazione della lunghezza di frase: umano alto, AI basso.

- Prosa italiana umana: deviazione standard 8-12 parole, coefficiente di variazione 0,55-0,75
- GPT-4 e GPT-5: deviazione standard 4-5 parole, coefficiente di variazione 0,25-0,35
- Claude: deviazione standard 5-6
- Gemini: posizione intermedia

Il test di normalità mostra che i testi umani seguono distribuzioni log-normali con coda pesante a destra (Shapiro-Wilk rifiuta la gaussiana), mentre i testi AI tendono a distribuzioni quasi-gaussiane.

### Type-Token Ratio e hapax

Il **Type-Token Ratio** (TTR) misura la ricchezza lessicale. Su campioni di mille parole:

- TTR umano colto: 0,52-0,62
- Testi GPT-4 italiani: 0,40-0,48
- Claude 3.5: leggermente superiore
- Gemini: intermedio

Il rapporto **hapax/vocabolario** (parole che compaiono una sola volta / vocabolario totale) nei testi narrativi italiani umani è 0,45-0,55, nei testi GPT 0,30-0,40. I modelli evitano sistematicamente le parole rare, per una «mode-seeking» strutturale del decoding.

### Firme specifiche dei tre grandi LLM in italiano

**GPT-4 e GPT-5:**

- frasi di 19-22 parole con σ 4-5
- densità di connettivi (*inoltre, tuttavia, pertanto*) al 3-5% dei token contro 1,5-2% umano
- uso massiccio di triadi asindetiche (*coerente, strutturato, chiaro*)
- elenchi puntati a tre voci
- incipit stereotipati e chiusure formulaiche

**Claude:**

- TTR lievemente superiore
- frasi più lunghe (21-24 parole) con σ 5-6
- preferenza per avverbi di modalità (*effettivamente, sostanzialmente, tendenzialmente*)
- tasso più alto di congiunzioni subordinanti complesse (*qualora, laddove*)

**Gemini:**

- profilo intermedio
- ricorrenza di hedging (*potrebbe, potrebbe essere considerato, in alcuni casi*)

**Comune a tutti i modelli:** abuso dell'em-dash. La prosa italiana tradizionale registra meno di 0,5 occorrenze per mille parole, i testi AI italiani arrivano a 2-5 per mille. È il singolo marcatore di superficie più discriminante.

### N-grammi ad alta frequenza differenziale

Bigrammi e trigrammi che compaiono nei testi AI italiani con frequenza da cinque a quindici volte superiore rispetto ai corpora giornalistici di riferimento (CORIS, PAISÀ, CHANGE-it, *la Repubblica*):

*è importante sottolineare, va notato che, in questo contesto, nel panorama attuale, d'altro canto, per concludere, offre numerosi vantaggi, un ruolo fondamentale, svolgere un ruolo, in costante evoluzione, al fine di, consente di ottenere, permette di massimizzare*

Quadrigrammi formulaici iperutilizzati per costruire parallelismi bilanciati:

*non solo… ma anche, tanto… quanto, sia… sia*

### Come usare le metriche nella pratica

- **Diagnosi rapida:** misurare il Gulpease su cinque passaggi diversi dello stesso testo. Se la deviazione standard è sotto 4 punti, probabile firma AI.
- **Correzione:** intervenire sulla burstiness, alternando frasi corte (sotto 6 parole) e lunghe (sopra 35).
- **Ricchezza lessicale:** se il TTR su mille parole è sotto 0,50, il vocabolario è impoverito; inserire termini rari, specifici, tecnici.
- **Sorveglianza em-dash:** Trova-Sostituisci e conteggio finale.

Le metriche non sostituiscono la lettura critica. Sono un termometro, non una diagnosi completa.

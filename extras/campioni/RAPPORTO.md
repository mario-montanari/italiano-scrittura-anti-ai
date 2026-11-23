# Tic rimasti nell'output con la skill attiva

> Questo rapporto è di Renato Romano e viene dal suo fork della skill, [`renatoromano-png/italiano-scrittura-anti-ai`](https://github.com/renatoromano-png/italiano-scrittura-anti-ai). Tutte le versioni citate, dalla 1.5.0 alla 1.12.0, sono quelle del fork e non coincidono con le release di questa repo: per questo nei titoli e nelle tabelle portano l'etichetta «fork». I 147 testi di campione restano nel fork, al commit [`a52bdc9`](https://github.com/renatoromano-png/italiano-scrittura-anti-ai/tree/a52bdc9a7ae3ca30545a9c399d955680e5d63222/extras/campioni), quindi i percorsi `extras/campioni/v…` citati nel testo vanno cercati lì. PAISÀ, il corpus usato come riferimento umano, ha licenza CC BY-NC-SA 4.0 e nessun suo testo compare qui. Le regole 15, 17, 18, 19 e 20 citate corrispondono a quelle con lo stesso numero nel `SKILL.md` di questa repo.

Campione: 21 testi, 7 per registro (blog divulgativo, marketing, professionale), 7.898 parole. Li hanno scritti tre agenti separati con la versione 1.5.0 del fork, senza sapere che i testi sarebbero stati analizzati. Lo script di misura è `extras/misura_campione.py`.

## Quello che la skill ha già risolto

Zero em-dash, zero *non è X, è Y*, zero incipit e chiusure formulaici, parole spia quasi assenti (7 in tutto il campione), frasi di lunghezza variabile (coefficiente di variazione tra 0,32 e 0,74). La qualità generale è alta.

## Tic rimasti, dal più grave

### 1. La virgola prima di *e* resiste

Il 34% delle *e* ha la virgola davanti (75 su 221), 9,5 ogni 1000 parole. Molte non rientrano nei tre casi ammessi: *Il fenomeno si chiama retrogradazione, e spiega perché…*, *Il fornaio cuoce pezzature grandi, e una pagnotta da un chilo…*.

La causa probabile è che la regola sta in `grammatica-italiana.md` §8, che chi scrive non sempre apre. Le regole del `SKILL.md`, che valgono sempre, non la contengono.

La proposta è promuoverla a regola non negoziabile numero 17, come era successo al *non è X, è Y*.

### 2. Esperienze personali inventate

Nei blog quattro testi su sette si aprono o si chiudono con un aneddoto in prima persona che il modello non può aver vissuto: *Ho cominciato a correre a quarantatré anni*, *ho comprato la mia attuale bici da città per novanta euro*, *La prima volta che ho sfornato una pagnotta decente*. Nei testi professionali compaiono confessioni costruite, come *Ho anche commesso errori, e uno mi ha insegnato parecchio*.

La causa probabile sta in `personalita-e-anima.md`, che consiglia la prima persona e l'ammissione di complessità. Il modello le applica inventando un vissuto. È il finto umano di plastica da cui la skill stessa mette in guardia, ma con un problema in più, perché è falso: spacciare per vere esperienze mai vissute danneggia chi pubblica.

La proposta è una regola esplicita. La prima persona si usa solo con fatti forniti dall'utente; altrimenti la voce si costruisce con posizioni e giudizi, senza biografia inventata. Dove serve un aneddoto, va chiesto all'utente oppure segnalato come esempio.

### 3. L'incipit scenico diventa uno schema

Tutti e sette i blog si aprono con una scena o un dettaglio concreto (*Sono le due e venti.*, *Il tabellone segna dieci minuti di ritardo, poi quindici, poi venticinque.*). Presa da sola, ognuna di queste aperture funziona. Ripetuta sempre uguale, la scena è diventata il nuovo *Nel mondo di oggi*. Quattro blog su sette si chiudono anche con un consiglio in prima persona (*Io consiglierei…*, *Il mio consiglio, da pendolare…*).

La proposta è che la guida agli incipit chieda di alternare i tipi di apertura (il fatto nudo, la tesi, il dato, una domanda vera) invece di usarne sempre uno. Lo stesso vale per le chiusure.

### 4. La suspense del «è un altro»

Cinque casi: *la strada più frequente è un'altra.* (e il paragrafo dopo comincia con *È quella civile.*), *Il risultato di cui vado più fiero è un altro.*, *Il motivo preciso è questo.*, *Il risultato è questo:*. È la stessa famiglia di *qui sta il punto*, già in `leak-conversazionale.md`, in una variante che il catalogo non nomina.

La variante andrebbe aggiunta al catalogo e alle stringhe da cercare: `è un altro.`, `è un'altra.`, `è questo.`, `è questa:`.

### 5. Gerundi in fila

*Ci sono arrivato passando molte ore in reparto, ascoltando chi guida i carrelli, cambiando i turni…, formando tre capisquadra…*: quattro gerundi in fila. Nel campione ci sono 9 gerundi in coda, concentrati nei testi professionali.

Nella sezione 2 di `pattern-strutturali.md` la catena di gerundi andrebbe segnalata come variante del gerundio parassita.

### 6. Il punto e virgola quasi assente

0,9 ogni 1000 parole, sette in tutto, tutti nei testi professionali. La skill dice di usarlo, ma è un'indicazione morbida. Per questo tic serve prima un riferimento umano (PAISÀ, Wikipedia) per sapere quale sarebbe la frequenza normale.

## Ordine consigliato

1 e 2 subito: il primo è misurabile e già normato, il secondo riguarda l'onestà del testo. Poi 4 e 5, che sono aggiunte piccole al catalogo. Il 3 richiede di riscrivere una parte della guida. Il 6 aspetta i corpora.

---

## Secondo campione: fork 1.6.0

Stesse 21 richieste, tre agenti nuovi, versione 1.6.0 del fork con le regole 17 e 18. 7.652 parole.

| Misura | fork 1.5.0 | fork 1.6.0 |
|---|---|---|
| *e* precedute da virgola | 34% (75 su 221) | 17% (38 su 220) |
| Aneddoti personali inventati nei blog | 4 testi su 7 | 0 |
| Segnaposto tipo `[prezzo]` | 0 | 41, in 8 testi |
| Righe di elenco puntato | 5 | 30 |
| Due punti ogni 1000 parole | 6,1 | 10,3 |
| Punto e virgola ogni 1000 parole | 0,9 | 2,1 |
| Gerundi in coda | 9 | 11 |

### Regola 17

La virgola davanti a *e* si è dimezzata, ma un'occorrenza su due fra quelle rimaste resta ingiustificata, compresa una virgola di Oxford (*sono lente, costose, e lasciano*).

### Regola 18

Gli aneddoti inventati sono spariti. L'effetto però è andato oltre il bersaglio. Tutti i testi di marketing e la lettera di candidatura ora hanno segnaposto anche per dati aziendali (prezzi, telefoni, date, nomi), che nella 1.5.0 venivano inventati. La lettera ne ha 13 e così non si usa senza riscriverla. Non inventare un prezzo è giusto, ma sette testi su sette pieni di parentesi sono troppi per una bozza.

### Effetti collaterali

I testi sono più strutturati, con più elenchi e più due punti. Alcune chiusure dei blog si sono appiattite in riassunti (*in sostanza, è un problema di rete e di investimenti*) o in avvertenze generiche (*è bene sentire un avvocato*). Le aperture sono più varie: tre blog su sette partono da un fatto invece che da una scena.

### Limite

Un solo campione per versione, e i modelli variano da un'esecuzione all'altra. Le differenze grandi (aneddoti, segnaposto, virgola) sono affidabili. Quelle piccole (gerundi, singole parole spia) no.

---

## Terzo campione: fork 1.7.0

Stesse richieste, tre agenti nuovi, regole 17 e 18 corrette. 7.207 parole. Misure prodotte con `python extras/misura_campione.py extras/campioni/v1.5.0 extras/campioni/v1.6.0 extras/campioni/v1.7.0`.

| Misura | fork 1.5.0 | fork 1.6.0 | fork 1.7.0 |
|---|---|---|---|
| *e* precedute da virgola | 33,9% | 17,3% | 10,6% |
| Virgole prima di *e* ogni 1000 parole | 9,5 | 5,0 | 2,8 |
| Aneddoti personali inventati nei blog | 4 su 7 | 0 | 0 |
| Segnaposto ogni 1000 parole | 0 | 5,0 | 1,4 |
| Testi con elenco *Da completare* | 0 | 0 | 13 |
| Suspense *è un altro* ogni 1000 parole | 0,51 | 0,26 | 0 |
| Gerundi in coda ogni 1000 parole | 1,14 | 1,44 | 0,56 |
| Righe di elenco ogni 1000 parole | 0,6 | 3,9 | 3,5 |
| Variazione della lunghezza delle frasi | 0,54 | 0,55 | 0,59 |

### Regola 17

La virgola prima di *e* è scesa a un terzo del valore iniziale. Delle 20 occorrenze rimaste quasi tutte segnano un cambio di soggetto (*resta una bici rubata, e il mercato dell'usato ne è pieno*). Ne restano poche ingiustificate, come *non posso disporre il rimborso, e preferisco dirglielo subito*, dove il soggetto è lo stesso.

### Regola 18

Niente vissuto inventato, segnaposto scesi da 41 a 14. In 13 testi i dati mancanti stanno ora nell'elenco *Da completare*, e il testo si legge senza parentesi. Un solo testo supera il limite di tre segnaposto: la lettera di candidatura, con quattro.

### Da tenere d'occhio

Gli elenchi puntati sono rimasti più frequenti che nella 1.5.0. Per un verbale o una circolare possono servire, ma vanno controllati nei prossimi campioni.

---

## Riferimento umano: PAISÀ

PAISÀ è un corpus del web italiano raccolto nel 2010, prima dei modelli linguistici (licenza CC BY-NC-SA 4.0, <http://hdl.handle.net/20.500.12124/3>). Circa due terzi dei documenti vengono da Wikipedia, quindi l'ho diviso in tre gruppi secondo l'indirizzo: blog, altro web, Wikipedia. Da ciascuno ho estratto 300 documenti fra 250 e 800 parole, circa 130.000 parole per gruppo, con `extras/campiona_paisa.py` (seme fisso, campione ripetibile). Il corpus non sta nella repo.

| Misura | PAISÀ blog | PAISÀ altro web | PAISÀ Wikipedia | Claude blog fork 1.5.0 | Claude blog fork 1.7.0 | Claude marketing e professionale fork 1.7.0 |
|---|---|---|---|---|---|---|
| *e* precedute da virgola | 7,0% | 6,8% | 9,3% | 32,9% | 15,8% | 7,1% |
| Punto e virgola ogni 1000 parole | 1,6 | 2,0 | 2,4 | 0 | 0 | 3,0 |
| Due punti ogni 1000 parole | 9,6 | 14,0 | 4,1 | 6,2 | 7,7 | 9,0 |
| Gerundi in coda ogni 1000 parole | 1,37 | 1,24 | 1,98 | 0,94 | 0,35 | 0,69 |
| *non solo X ma Y* ogni 1000 parole | 0,10 | 0,12 | 0,05 | 0 | 0 | 0 |
| Em-dash ogni 1000 parole | 0,04 | 0,10 | 0,39 | 0 | 0 | 0 |
| Variazione lunghezza frasi | 0,64 | 0,66 | 0,53 | 0,51 | 0,57 | 0,60 |

### Virgola prima di *e*

Chi scriveva sul web italiano la metteva davanti al 7% delle *e*. Claude partiva da quasi cinque volte tanto. Con la 1.7.0 del fork i testi di marketing e professionali sono in linea con la prosa umana, mentre i blog sono ancora al doppio. La regola 17 è confermata dai numeri; il registro blog resta da sorvegliare.

### Punto e virgola

Nei blog umani compare 1,6 volte ogni 1000 parole, nei blog di Claude mai. La skill dice già che i modelli lo usano poco: ora c'è la misura.

### Gerundio in coda

Nella prosa umana è più frequente che nei testi di Claude, che ne usano da un terzo alla metà. Non serve quindi una regola contro la catena di gerundi: l'uso in sé non è un tic, e conviene correggere solo i casi parassiti o irrelati.

### Variazione della lunghezza delle frasi

I blog di Claude sono un po' più regolari di quelli umani (0,57 contro 0,64): la differenza c'è, ma è piccola.

### Limiti

I blog di Claude sono solo sette per versione. PAISÀ ha sedici anni e alcuni documenti di blog uniscono più articoli o commenti. Le misure sono euristiche: servono a confrontare ordini di grandezza, non a giudicare un testo singolo.

---

## Quarto campione: fork 1.9.0

Stesse richieste, versione 1.9.0 con la regola 19 sul punto e virgola, la suspense *è un altro* nel catalogo e la guida alle aperture variate. 7.365 parole.

| Misura | fork 1.5.0 | fork 1.6.0 | fork 1.7.0 | fork 1.9.0 | PAISÀ blog |
|---|---|---|---|---|---|
| *e* precedute da virgola, tutti i registri | 33,9% | 17,3% | 10,6% | 5,4% | 7,0% |
| *e* precedute da virgola, solo blog | 32,9% | | 15,8% | 12,5% | 7,0% |
| Punto e virgola nei blog ogni 1000 parole | 0 | | 0 | 2,4 | 1,6 |
| Suspense *è un altro* ogni 1000 parole | 0,51 | 0,26 | 0 | 0 | 0,01 |
| Segnaposto ogni 1000 parole | 0 | 5,0 | 1,4 | 1,2 | |
| Grassetto ogni 1000 parole | 2,7 | 0 | 0 | 3,1 | 0,01 |
| Variazione lunghezza frasi, blog | 0,51 | | 0,57 | 0,53 | 0,64 |

### Punto e virgola

Dopo tre versioni senza nessun punto e virgola, i blog ne hanno 2,4 ogni 1000 parole, appena sopra il valore umano. Quelli letti a mano sono quasi tutti al posto giusto, fra due proposizioni legate (*è probabile che sia alluminio; se torna alla forma originale si tratta di…*). La regola 19 funziona senza essere forzata.

### Virgola prima di *e*

Su tutti i registri è scesa al 5,4%, sotto il 7% umano. Nei blog resta al 12,5%, quasi il doppio della prosa umana: è il punto dove insistere.

### Aperture

Nel primo campione tutti e sette i blog si aprivano con una scena. Ora i tipi sono quattro: il fatto (*Il pane comincia a invecchiare appena esce dal forno.*), la data e il luogo (*Torino, 1884.*), la domanda vera (*Quanto rumore deve sopportare chi vive in condominio?*) e una sola scena (*Ore 7.42, il binario di una stazione di provincia.*).

### Tic ricomparso: il titoletto in grassetto

Nei testi professionali tornano i paragrafi aperti da un'etichetta in grassetto (*Margine. Il margine lordo scende…*, *Valutazione. A nostro giudizio…*). È il pattern 7 di `pattern-strutturali.md`, le liste con header inline grassettato, che nella 1.6.0 e nella 1.7.0 del fork era sparito senza una regola dedicata. Va aggiunto al controllo automatico.

### Uso dello strumento

L'agente che scriveva i testi di marketing ha lanciato da solo `scripts/controlla_testo.py` sulle bozze, come chiede il `SKILL.md`, e ha giustificato le segnalazioni rimaste. Sul campione intero lo strumento trova 0 violazioni certe e 17 punti da verificare, contro gli 88 della 1.5.0.

---

## Quinto campione: fork 1.10.0

Stesse richieste, versione 1.10.0 con la regola 20 sui titoletti in grassetto e la soglia misurata della regola 17. 7.399 parole.

| Misura | fork 1.9.0 | fork 1.10.0 | PAISÀ blog |
|---|---|---|---|
| Titoletti in grassetto segnalati | 19 | 0 | |
| *e* precedute da virgola, solo blog | 12,5% | 3,9% | 7,0% |
| *e* precedute da virgola, tutti i registri | 5,4% | 8,4% | |
| Punto e virgola nei blog ogni 1000 parole | 2,4 | 5,2 | 1,6 |
| Righe di elenco ogni 1000 parole | 3,0 | 0,7 | 0,26 |
| Testi con troppe virgole prima di *e* | 3 | 3 | |

### Titoletti in grassetto

Spariti del tutto. Le relazioni, la circolare, il verbale e la nota condominiale usano ora titoli veri (`##`). Anche gli elenchi puntati sono scesi a un quarto.

### Virgola prima di *e* nei blog

Dal 12,5% al 3,9%, per la prima volta sotto la prosa umana. I tre testi che superano la soglia sono di marketing e brevi: due virgole in 265-308 parole, ciascuna con un cambio di soggetto. Per un testo così corto la soglia di una ogni 400 parole è forse troppo stretta.

### Punto e virgola: correzione eccessiva

I blog sono passati da 2,4 a 5,2 ogni 1000 parole, più di tre volte la prosa umana, con due o tre punti e virgola per articolo. Sono usati in modo corretto (*la catena allungata mangia gli ingranaggi; cambiare catena, pignoni e corona…*), ma la frequenza si fa notare. La regola 19 chiede *almeno uno*; il modello l'ha presa come una quota. Serve un tetto, oltre che un minimo.

---

## Sesto campione: fork 1.11.0

Stesse richieste, versione 1.11.0 con il tetto al punto e virgola. 7.114 parole.

| Misura | fork 1.5.0 | fork 1.10.0 | fork 1.11.0 | PAISÀ blog |
|---|---|---|---|---|
| Punto e virgola nei blog ogni 1000 parole | 0 | 5,2 | 2,5 | 1,6 |
| *e* precedute da virgola, solo blog | 32,9% | 3,9% | 0% | 7,0% |
| *e* precedute da virgola, tutti i registri | 33,9% | 8,4% | 1,8% | |
| Due punti nei blog ogni 1000 parole | 6,2 | 7,8 | 4,2 | 9,6 |
| Variazione lunghezza frasi, blog | 0,51 | 0,57 | 0,51 | 0,64 |
| Violazioni certe trovate dallo script | | 3 | 2 | |

### Punto e virgola

Il tetto ha funzionato: da 5,2 a 2,5 ogni 1000 parole. Ma ogni blog ne ha esattamente uno, né zero né due. Il valore medio è vicino a quello umano, la distribuzione no: il modello tratta la regola come una casella da spuntare.

### Virgola prima di *e*: ora troppo poche

Nei blog nessuna, su tutti i registri l'1,8%, contro il 7% della prosa umana. Il tic iniziale è scomparso. Al suo posto c'è l'eccesso opposto, perché il modello evita anche le virgole lecite (cambio di soggetto, stacco ritmico). Nessun lettore se ne accorgerebbe, ma l'assenza totale di un tratto comune è anch'essa un segnale statistico, come lo era l'assenza del punto e virgola.

### Cosa resta lontano dalla prosa umana

La variazione della lunghezza delle frasi (0,51 contro 0,64), che sei versioni non hanno spostato, e i due punti nei blog, scesi a meno della metà del valore umano.

### Conclusione dopo sei campioni

Le regole che vietano un tic (em-dash, contrasto fittizio, vissuto inventato, titoletti in grassetto, suspense) lo eliminano in una o due versioni e non producono effetti collaterali. Le regole di frequenza (virgola prima di *e*, punto e virgola) tendono invece a oscillare: prima troppo, poi troppo poco, poi un valore fisso. Stringerle ancora rischia di sostituire un tic con un altro. Il passo successivo è lavorare sulla variazione, con regole che chiedono di alternare invece di fissare quote.

---

## Settimo campione: fork 1.12.0

Stesse richieste, versione 1.12.0: le regole 15, 17 e 19 danno una misura della prosa umana invece di una quota.

| Misura, blog | fork 1.5.0 | fork 1.11.0 | fork 1.12.0 | PAISÀ blog |
|---|---|---|---|---|
| Parole per frase, media | 14,9 | 15,0 | 19,4 | 25,2 |
| Frasi oltre le 35 parole | 1,9% | 1,1% | 11,5% | 20,6% |
| Variazione lunghezza frasi | 0,51 | 0,51 | 0,59 | 0,64 |
| Punto e virgola ogni 1000 parole | 0 | 2,5 | 1,0 | 1,6 |
| Blog con un punto e virgola | 0 su 7 | 7 su 7 | 3 su 7 | |
| *e* precedute da virgola | 32,9% | 0% | 12,7% | 7,0% |

> Nota di questa repo: in questa tabella la frase media e la quota oltre le 35 parole di PAISÀ contano tutte le frasi, quelle delle colonne di Claude solo le frasi di almeno tre parole, come fanno `extras/misura_campione.py` e `scripts/controlla_testo.py`. Contato allo stesso modo, lo stesso campione di PAISÀ dà 26,5 parole e il 21,8% (misura del 2026-11-19). Nei blog di Claude il modo di contare sposta i valori di un decimale al massimo, perché frasi di una o due parole non ce ne sono quasi.

### Lunghezza delle frasi

È il primo spostamento dopo sei versioni ferme. La media sale da 15 a 19 parole, i periodi oltre le 35 parole passano dall'1% all'11,5% e la variazione da 0,51 a 0,59. La distanza dalla prosa umana si è più che dimezzata, anche se non è chiusa. Lo stesso effetto si vede in tutti i registri: media da 16 a 20 parole, periodi lunghi dal 4% al 10%.

### Punto e virgola

Non c'è più la quota fissa: tre blog ne hanno uno, quattro nessuno, 1,0 ogni 1000 parole contro l'1,6 umano. È la distribuzione che ci si aspetta da chi lo usa dove serve.

### Virgola prima di *e*

Risale al 12,7% nei blog, dopo lo zero della 1.11.0. Le occorrenze lette a mano sono quasi tutte cambi di soggetto dentro periodi lunghi (*il congelatore invece la ferma quasi del tutto, e una fetta congelata…*), cioè il caso che la regola 17 ammette. I periodi più lunghi portano con sé più coordinate e quindi più occasioni legittime. Il valore resta sopra quello umano e va seguito, ma il tic dei primi campioni, la virgola fra proposizioni con lo stesso soggetto, non è tornato.

### Conclusione

Chiedere variazione funziona meglio che fissare quote: il punto e virgola si distribuisce, i periodi si allungano senza una soglia per paragrafo. È la prima versione in cui tutte le misure si muovono nella direzione della prosa umana senza superarla.

---

## Ottavo campione: virgola prima di «e» e periodo lungo, sulla 1.7.0

Stesse 21 richieste, due campioni con tre agenti nuovi ciascuno. Il primo usa la 1.7.0 di questa repo così com'è. Il secondo usa la stessa versione con due modifiche: la sottosezione «Come si costruisce il periodo lungo» di `metodologie-operative.md` e la regola 17 riscritta, che con un soggetto nuovo ammette la virgola prima di *e* senza imporla. 8.049 e 7.998 parole.

| Misura | 1.7.0 | dopo le modifiche | PAISÀ blog |
|---|---|---|---|
| *e* precedute da virgola, tutti i registri | 16,1% | 9,6% | 7,0% |
| *e* precedute da virgola, blog | 15,5% | 8,8% | 7,0% |
| *e* precedute da virgola, marketing | 20,9% | 13,8% | |
| *e* precedute da virgola, professionale | 12,1% | 5,8% | |
| Virgola prima di *e* ogni 1000 parole | 4,35 | 2,75 | 1,84 |
| Parole per frase, media, blog | 25,1 | 24,7 | 26,5 |
| Frasi oltre le 35 parole, blog | 28,4% | 26,7% | 21,8% |
| Variazione lunghezza frasi (CV), blog | 0,55 | 0,56 | 0,64 |
| Gerundio in coda ogni 1000 parole | 0,75 | 1,38 | 1,39 |
| Punto e virgola ogni 1000 parole | 2,11 | 1,88 | 1,63 |
| Segnaposto ogni 1000 parole | 3,11 | 2,88 | 0,16 |

### La premessa che non reggeva più

Il lavoro era partito da una misura sulla 1.12.0 del fork: nei blog 19,4 parole per frase e l'11,5% di frasi oltre le 35 parole, contro le 26,5 e il 21,8% di PAISÀ. I blog della 1.7.0 di questa repo arrivano invece a 25,1 parole per frase e al 28,4% di periodi lunghi. Le frasi corte non erano più il problema.

La distanza netta rimasta era la virgola prima di *e*: 16,1% contro il 7% umano. La causa stava nella regola 17, che con un soggetto nuovo diceva che la virgola «resta». Il modello la metteva ogni volta che il soggetto cambiava, anche dopo una proposizione di poche parole. La regola riscritta la ammette solo se la prima proposizione è lunga o se senza virgola nascerebbe un equivoco.

La sottosezione sul periodo lungo resta come guida di mestiere. La sua verifica è più modesta: che i periodi lunghi tengano e che siano costruiti bene.

### Virgola prima di *e*

Su tutti i registri la quota scende dal 16,1% al 9,6%, nei blog dal 15,5% all'8,8%, vicino al 7% umano. Nei testi professionali arriva al 5,8%, appena sotto la prosa umana; quelli di marketing restano i più alti, al 13,8%. Le sequenze «, e » trovate con `grep` passano da 37 a 23.

Le stesse richieste producono testi diversi, quindi le frasi del primo campione non hanno una gemella nel secondo. Nel campione di base si vedono però le virgole che la regola nuova toglie, con una prima proposizione breve e nessun equivoco possibile:

- *Un caffè si giudica nella tazza, e quello che finisce nella tazza dipende in buona parte da quanti giorni sono passati…* (marketing-02)
- *Una bici troppo grande o troppo piccola affatica schiena e ginocchia, e nessun affare la rende comoda.* (blog-02)
- *L'impresa non può smontare beni privati, e quello che resta al suo posto rischia di rovinarsi…* (professionale-07)

### Periodo lungo

I periodi lunghi tengono: nei blog 24,7 parole per frase e il 26,7% oltre le 35, contro 25,1 e 28,4% della base. La variazione resta quasi ferma, 0,56 contro lo 0,64 umano.

### Lettura a mano

Nel secondo campione le frasi oltre le 35 parole sono 78. Lette una per una, 70 sono costruite bene e 8 sono gonfie, il 10,3%.

Un periodo riuscito, da blog-01, porta 49 parole su un solo filo causale e mette il verbo subito: *In cottura i granuli di amido assorbono l'acqua dell'impasto, si gonfiano e perdono la loro struttura ordinata; quando il pane si raffredda le catene di amido tornano piano piano ad allinearsi…*

Uno gonfio, da blog-06, accumula complementi e una parentesi di esempi prima del verbo: *Due volte alla settimana, a casa, dieci minuti di esercizi per polpacci, glutei e muscoli addominali (…) proteggono più di qualsiasi scarpa…* A voce alta non basta un fiato per arrivare a *proteggono*. Gli altri sette hanno quasi tutti lo stesso guasto: un inciso, una relativa o una serie di participi allontana il verbo o il pronome dalla parola a cui si lega. Chi legge deve tornare indietro.

### Gerundio in coda e segnaposto

Il gerundio in coda sale da 0,75 a 1,38 ogni 1000 parole, quasi il valore umano. Fra due campioni consecutivi del fork la stessa misura ha oscillato fino a 0,88: lo spostamento sta dentro questo rumore e non va attribuito alle modifiche.

I segnaposto stanno solo nei testi di marketing e professionali, dove la regola 18 li chiede al posto dei dati che la richiesta non dà. Nei blog non ce n'è nessuno.

### Limiti

Sette testi per registro e un solo campione per versione: gli spostamenti piccoli, come quello del gerundio, non dicono niente. La classificazione dei periodi lunghi è una lettura sola, non ripetuta da un secondo lettore. I 42 testi restano nel fork, `renatoromano-png/italiano-scrittura-anti-ai`, come quelli dei campioni precedenti.

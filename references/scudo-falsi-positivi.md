# Lo scudo contro i falsi positivi

Il resto della skill lavora su un testo. Questo file lavora su un'accusa.

Uno studente si vede respingere la tesi, una redazione contesta un pezzo al
collaboratore che l'ha scritto, un committente rifiuta la consegna. Il motivo
è sempre lo stesso: un programma ha prodotto un numero, e qualcuno ha letto
quel numero come una prova. Qui c'è come si risponde.

## Indice

1. [Il confine, prima di tutto il resto](#1-il-confine-prima-di-tutto-il-resto)
2. [Che cosa misura davvero un rilevatore](#2-che-cosa-misura-davvero-un-rilevatore)
3. [Quanto sbaglia, secondo chi lo ha misurato](#3-quanto-sbaglia-secondo-chi-lo-ha-misurato)
4. [Chi paga il falso positivo](#4-chi-paga-il-falso-positivo)
5. [La questione italiana](#5-la-questione-italiana)
6. [Costruire la difesa](#6-costruire-la-difesa)
7. [Il modello di difesa argomentata](#7-il-modello-di-difesa-argomentata)
8. [La zona grigia: la dichiarazione d'uso](#8-la-zona-grigia-la-dichiarazione-duso)
9. [Cosa questo file non fa](#9-cosa-questo-file-non-fa)

---

## 1. Il confine, prima di tutto il resto

Questo file serve a difendere un testo umano accusato ingiustamente. Non serve
a far passare per umano un testo generato, e non contiene niente che aiuti a
farlo.

La garanzia sta nel modo in cui la difesa è costruita, prima ancora che nella
buona fede di chi legge. È il motivo per cui questo file può stare in pubblico
senza diventare un manuale per barare.

**Nessuno strumento certifica la paternità umana di un testo. Nemmeno questo.**
Un rilevatore dichiara «l'ha scritto una macchina» senza poterlo sapere. Un
contro-rilevatore dichiarerebbe «l'ha scritto una persona» con la stessa
ignoranza, e venderebbe la medesima illusione con il segno invertito. La
sezione 8 di `segnali-misurabili.md` spiega perché il primo responso è un
segnale debole, e quella debolezza vale in tutte e due le direzioni.

La difesa quindi non risponde a un punteggio con un altro punteggio. Si regge
su prove che stanno fuori dal testo:

- bozze e versioni intermedie, con le loro date
- appunti, scalette, materiali preparatori
- le fonti consultate e il modo in cui sono state usate
- testi precedenti all'accusa, che mostrano la stessa voce
- la capacità dell'autore di spiegare le proprie scelte, riga per riga

Da qui viene la garanzia. Chi volesse difendere un testo generato trova quei
campi vuoti, e una difesa vuota non si porta davanti a nessuno. Il confine non
ha bisogno di un interrogatorio: lo tiene la forma stessa del documento.

Il caso più frequente sta in mezzo. Una persona pensa e scrive il testo, poi
usa la macchina per correggere la grammatica o accorciare un paragrafo, e viene
accusata lo stesso. Lì il documento cambia nome e natura: diventa una
dichiarazione d'uso, che elenca parte per parte cosa ha fatto lei e cosa ha
fatto la macchina. Se ne occupa la sezione 8.

## 2. Che cosa misura davvero un rilevatore

Un rilevatore non riconosce chi ha scritto. Misura quanto il testo è
prevedibile per un modello linguistico: quanto poco «sorprendente» risulta la
parola successiva, e quanto quella sorpresa varia lungo la pagina. Prosa poco
sorprendente e uniforme finisce sopra soglia.

Da qui discendono tre cose, e vanno dette a chi accusa.

**Il responso è una somiglianza, non una provenienza.** Lo strumento afferma
che il testo assomiglia a ciò che è stato addestrato a chiamare generato.
Della storia di quel testo non sa niente, perché non l'ha mai vista.

**La soglia è una decisione, non un fatto di natura.** Il numero grezzo è un
continuo; il verdetto nasce quando qualcuno decide dove tagliarlo. Chi vende
lo strumento sceglie quel punto bilanciando due errori, e la scelta favorisce
il proprio prodotto, non l'imputato.

**Quasi nessuno di questi strumenti è ispezionabile.** I modelli e i dati di
addestramento sono chiusi. Un'accusa fondata su uno strumento che non si può
esaminare ha un problema prima ancora di discutere il merito, ed è un problema
di chi accusa.

Sopra tutto questo sta un limite più profondo. Sadasivan e colleghi hanno
legato l'accuratezza massima raggiungibile da un rilevatore, per definizione,
alla distanza fra la distribuzione dei testi umani e quella dei testi generati.
Man mano che i modelli si avvicinano alla prosa umana, il tetto scende per
tutti. Il limite appartiene al problema, e nessun prodotto migliore lo aggira.

## 3. Quanto sbaglia, secondo chi lo ha misurato

Quattro dati pubblicati, una decisione istituzionale che in una discussione
pesa quanto un dato, e in fondo l'obiezione più seria, che va accolta in
parte. Nessuno dei quattro dati viene da chi vende il servizio, tranne
l'ultimo, che è il più interessante proprio per questo.

**Gli strumenti del 2023 non erano né accurati né affidabili.** Weber-Wulff e
colleghi hanno testato dodici strumenti pubblici più Turnitin e
PlagiarismCheck. La conclusione, testuale: «the available detection tools are neither accurate nor
reliable and have a main bias towards classifying the output as human-written
rather than detecting AI-generated text».

Quella seconda parte va letta con attenzione, perché è controintuitiva e
onesta. L'errore prevalente di questi strumenti va nella direzione opposta al
falso positivo: tendono a dire «umano» anche quando non lo è. Un'accusa non
diventa più solida per questo. Diventa più fragile lo strumento nel suo
complesso, e con esso l'idea che il suo responso valga come prova.

**Dove il falso positivo è stato misurato, è enorme.** Liang, Yuksekgonul,
Mao, Wu e Zou hanno dato in pasto ai rilevatori più diffusi dei saggi TOEFL
scritti da studenti non madrelingua inglesi. Tasso medio di falsi positivi:
**61,3 per cento**. Il 19,8 per cento di quei testi umani è stato indicato
come artificiale da tutti i rilevatori all'unanimità. Gli stessi strumenti,
sui saggi di studenti statunitensi madrelingua, funzionavano bene.

La spiegazione degli autori è la parte che conta: i rilevatori «may
unintentionally penalize writers with constrained linguistic expressions».
Puniscono chi scrive con mezzi espressivi limitati o sorvegliati.

**Chi costruisce i modelli ha ritirato il proprio rilevatore.** OpenAI ha messo
online il suo AI Text Classifier a gennaio 2023 e lo ha spento a luglio dello
stesso anno, con una nota secca: «As of July 20, 2023, the AI
classifier is no longer available due to its low rate of accuracy». Chi
addestra i modelli non è riuscito a costruire lo strumento che li riconosce.

**Il fornitore più usato nelle scuole dichiara circa quattro frasi umane
segnalate ogni cento.** Turnitin ha lanciato la propria rilevazione ad aprile
2023 annunciando meno dell'uno per cento di falsi positivi. A giugno la sua
chief product officer, Annie Chechitelli, ha precisato la cifra: quel valore
vale sul documento intero e solo per documenti con oltre il venti per cento di
scrittura artificiale, mentre a livello di singola frase il tasso è **circa il
quattro per cento**. Sotto la soglia del venti per cento l'azienda ha aggiunto
un avviso di cautela al proprio responso.

Tradotto per chi si difende: su un elaborato di cento frasi, quattro frasi
umane evidenziate in rosso sono il funzionamento previsto dello strumento,
dichiarato da chi lo vende. Non sono un indizio.

**C'è chi lo strumento lo ha spento.** Nell'agosto 2023 la Vanderbilt
University ha disattivato la rilevazione AI di Turnitin, spiegando pubblicamente
perché: nessuna trasparenza su come lo strumento decide, falsi positivi
documentati in altri atenei, e il fatto che «AI detectors have been found to be
more likely to label text written by non-native English speakers as AI-written».
La conclusione dell'ateneo, testuale: «we do not believe that AI detection
software is an effective tool that should be used». Nello stesso annuncio
l'università fa il conto che chiunque può rifare: sui 75.000 elaborati inviati
a Turnitin nel 2022, l'uno per cento dichiarato significa «around 750 student
papers could have been incorrectly labeled».

Va presentata per quello che è. Una decisione istituzionale motivata pesa meno
di una misura, e davanti a una commissione conta per altro: un ateneo ha
esaminato lo strumento con calma e ha scelto di non usarlo.

**L'obiezione più seria arriva dal 2025, e una parte va accolta.** Jabarian e
Imas, in un working paper NBER del settembre 2025, scrivono che «Independent
studies that examine AI detection are out of date and focus on a set of tools
that rely on antiquated techniques», e citano proprio Weber-Wulff.

Il loro risultato va riportato per intero, anche dove non conviene. Su un
corpus inglese di sei generi, i tre prodotti commerciali provati sbagliano
poco: falsi positivi fra lo 0,1 e lo 0,7 per cento. Chi si difende non può
quindi sostenere che ogni rilevatore sbagli sempre, perché sarebbe la stessa
disinvoltura di chi accusa.

Lo studio però autorizza a dire meno di quanto venga citato. Un prodotto solo,
su tre, rispetta il tetto che gli autori stessi propongono: «Pangram is the
only tool to satisfy a strict cap (FPR 0.005) without sacrificing accuracy».
GPTZero, il più diffuso nelle scuole, resta sopra quel tetto. E il corpus è
fatto di notizie, blog, curriculum, recensioni e romanzi inglesi anteriori al
2000: nessun elaborato scolastico, nessuno scrivente in una lingua non sua,
nessun testo italiano. La misura di Liang resta quindi in piedi, perché quella
popolazione qui non è stata misurata, e gli stessi autori mettono fra le
questioni aperte il caso di un modello che «rephrased a human-generated draft
written by a non-native speaker».

La domanda da portare a chi accusa diventa più precisa: quale prodotto avete
usato, con quale soglia, e con quale tasso di errore misurato sul mio genere e
sulla mia lingua.

## 4. Chi paga il falso positivo

L'errore non cade a caso. Si concentra, e questo lo rende una questione di
equità prima che di tecnica.

Il meccanismo riguarda la prevedibilità della prosa, non la nazionalità di chi
scrive. Sono più esposti, per misura diretta o per lo stesso meccanismo:

| Chi | Perché finisce sopra soglia |
|---|---|
| chi scrive in una lingua non sua | lessico più ristretto, costruzioni più regolari (misurato) |
| chi scrive in registro formale o burocratico | la forma è prescritta e ripetitiva per mestiere |
| chi scrive in un genere codificato | abstract accademici, atti, referti, relazioni tecniche |
| chi ha imparato a scrivere su un modello scolastico | il tema svolto è un formato, e il formato è prevedibile |
| chi rilegge molto e leviga | la revisione toglie le asperità che il rilevatore legge come umane |
| chi usa correttori, traduttori, dettatura | strumenti leciti che regolarizzano la superficie |

Il paradosso è tutto qui: la prosa ordinata paga. Chi scrive pulito, corregge
gli errori e mantiene un registro coerente produce un testo più prevedibile, e
la prevedibilità è l'unica cosa che il rilevatore sa vedere.

C'è un corollario amaro per gli studenti. A chi si difende viene spesso
consigliato di «scrivere in modo più naturale» la prossima volta. È un consiglio
che chiede a una persona di peggiorare la propria prosa per compiacere un
programma, e va rifiutato con la stessa fermezza dell'accusa.

## 5. La questione italiana

Qui serve una dichiarazione precisa, perché la tentazione di gonfiare
l'argomento è forte.

**Nessuno ha pubblicato una misura del tasso di falsi positivi sull'italiano.**
Le cifre della sezione 3 riguardano l'inglese. Chiunque affermi «sull'italiano
i falsi positivi sono alti» sta estendendo un dato, non citandolo, e va detto
apertamente. Questo file lo dice.

Ciò che si può sostenere con onestà è più solido, e più utile in una
discussione:

1. Dove l'errore è stato misurato, è grande (sezione 3).
2. Gli strumenti risultano nel complesso né accurati né affidabili sull'inglese, cioè sulla lingua su cui sono stati costruiti e ottimizzati.
3. Il meccanismo che genera il falso positivo, la prevedibilità della prosa, non dipende dalla lingua.
4. Il vuoto sull'italiano non è una mia impressione: lo dichiara la ricerca.

Su quest'ultimo punto c'è una fonte recente e netta. Macko e Kopal, presentando
nel settembre 2025 il benchmark multilingue CEAID, aprono così: «Machine-generated
text detection, as an important task, is predominantly focused on English in
research. This makes the existing detectors almost unusable for non-English
languages, relying purely on cross-lingual transferability». Quel trasferimento
da una lingua all'altra, aggiungono, «can have severely degraded performance».

Il loro benchmark copre sette lingue dell'Europa centrale: croato, ceco,
tedesco, ungherese, polacco, slovacco, sloveno. L'italiano non c'è.

Non è un caso isolato. MULTITuDE, il benchmark multilingue presentato da Macko
e colleghi a EMNLP 2023, ne copre undici: arabo, catalano, ceco, tedesco,
inglese, spagnolo, olandese, portoghese, russo, ucraino, cinese. Tre di queste
sono lingue romanze, e l'italiano non è fra loro. Gli stessi autori aprono
dichiarando che «there is a lack of research into capabilities of recent LLMs
to generate convincing text in languages other than English and into
performance of detectors of machine-generated text in multilingual settings».

Due benchmark, sedici lingue diverse in tutto, e l'italiano fuori da entrambi.
Il lavoro che misura la rilevazione oltre l'inglese esiste, e la nostra lingua
ne resta fuori.

Vale anche per il lavoro più recente e più favorevole ai rilevatori. Il
benchmark di Jabarian e Imas del 2025, quello che accusa gli studi precedenti
di essere invecchiati, misura sei generi testuali e sono tutti inglesi.

Nemmeno passare per l'inglese aiuta. Gli stessi autori riportano che tradurre
un testo per farlo analizzare da un rilevatore anglofono alza i falsi positivi,
e che la rilevazione va fatta direttamente nella lingua in cui il testo è
scritto.

Da qui l'argomento da portare a chi accusa, che non ha bisogno di cifre
inventate:

> Lo strumento che ha prodotto questo responso non ha una validazione
> pubblicata sulla lingua in cui è scritto il mio testo. Chiedo di conoscere
> il tasso di falsi positivi misurato sull'italiano, sul mio genere testuale e
> sulla lunghezza del mio elaborato. In assenza di quel dato, il responso non
> ha un margine di errore noto, e senza margine di errore non è una misura.

Nella maggior parte dei casi quel dato non esiste, e la richiesta sposta
l'onere dove deve stare. Chi accusa deve sostenere l'accusa.

## 6. Costruire la difesa

Sette passaggi, nell'ordine.

**1. Stabilire chi accusa e con che cosa.** Nome dello strumento, punteggio
esatto, soglia dichiarata, livello del responso: documento intero o singole
frasi. Molte accuse arrivano senza il nome dello strumento. Chiederlo è il
primo atto della difesa, e a volte l'unico necessario.

**2. Ricondurre il responso al suo statuto.** Con la sezione 2 di questo file:
somiglianza, non provenienza. Soglia decisa da chi vende. Strumento non
ispezionabile. Si espone il meccanismo senza attaccare la persona che ha
sollevato il caso, perché una difesa che offende perde.

**3. Portare i dati pubblicati.** Le quattro evidenze della sezione 3, con la
citazione completa. La più efficace davanti a una commissione scolastica è di
solito quella del fornitore stesso: quattro frasi umane segnalate ogni cento
sono il comportamento dichiarato del prodotto.

**4. Presentare la prova di processo.** Bozze, versioni intermedie, cronologia
del documento condiviso, appunti, scalette, messaggi in cui si discuteva il
lavoro, tempi di stesura. Si ordina per data. La cronologia è ciò che un testo
generato non può fabbricare all'indietro senza mentire in modo verificabile,
ed è la prova più forte che esista. Prima di portarla si controlla che le date
reggano fra loro e con il racconto dell'autore: una data che non torna non
toglie valore al resto, ma va messa in chiaro come riserva prima che la trovi
la controparte.

**5. Presentare la prova di voce.** Testi dell'autore precedenti all'accusa,
meglio se anteriori alla diffusione degli strumenti generativi, messi accanto
al testo contestato. Il metodo e la scheda sono in `voce-personale.md`, lo
strumento facoltativo è `scripts/profilo_voce.py`.

Attenzione al modo di formularlo, perché qui si sbaglia facilmente.
L'argomento **non** è «il profilo dice che è umano», che sarebbe il
contro-rilevatore escluso dalla sezione 1. L'argomento è la continuità:
*questo testo ha le stesse abitudini dei miei testi di prima, e quelle
abitudini sono documentate*.

**6. Offrire la prova di conoscenza.** L'autore sa dire perché ha scelto quella
parola, quell'esempio, quel taglio; sa dire cosa ha tolto e per quale motivo;
sa rispondere a domande sul contenuto senza rileggere. È l'unica prova che
regge in un colloquio dal vivo, ed è quella che le commissioni accettano più
volentieri. Nel documento si offre: *sono disponibile a discutere il testo di
persona*.

**7. Non riscrivere il testo.** Se l'autore chiede aiuto per abbassare il
punteggio, la risposta è no. Il motivo è anche pratico, prima che etico: una
riscrittura successiva all'accusa distrugge la prova di processo, cambia
l'oggetto della discussione e somiglia a una manomissione. Chi si difende bene
lascia il testo dov'è.

## 7. Il modello di difesa argomentata

Una pagina. Sobria, senza indignazione, senza punti esclamativi. Chi legge è
di solito una persona che deve decidere in fretta e che teme di sbagliare in
entrambe le direzioni.

```text
DIFESA ARGOMENTATA

Testo contestato: [titolo, data di consegna, lunghezza]
Autore: [nome]
Accusa ricevuta: [chi, quando, con quali parole]
Strumento citato: [nome, punteggio, soglia, livello del responso]
Se lo strumento non è stato indicato: chiederlo prima di proseguire.

1. CHE COSA DICE LO STRUMENTO
   Una frase asciutta, senza commento.

2. CHE COSA SIGNIFICA QUEL RESPONSO
   Somiglianza statistica, non provenienza. Soglia scelta dal fornitore.
   Nessuna validazione pubblicata sull'italiano.

3. QUANTO SBAGLIANO QUESTI STRUMENTI
   Da una a tre evidenze della sezione 3, con citazione completa.
   Meglio poche e verificabili che molte e generiche.

4. COME È NATO QUESTO TESTO
   Racconto cronologico, con i materiali allegati in ordine di data.

5. PERCHÉ È MIO
   Continuità con i testi precedenti: abitudini documentate, con esempi
   affiancati.

6. COSA CHIEDO
   Di norma: una valutazione umana del merito, o un colloquio sul testo.
   Non l'assoluzione automatica.

Allegati: [elenco numerato, ogni voce con la sua data]
```

Due avvertenze sul tono. La prima: si chiede una valutazione umana, non si
pretende di aver vinto. La seconda: si offre il colloquio invece di aspettare
che venga imposto, perché offrirlo è la mossa di chi non ha niente da
nascondere.

## 8. La zona grigia: la dichiarazione d'uso

Il testo pensato e scritto da una persona, poi rifinito con l'aiuto della
macchina, è il caso più comune di tutti. Trattarlo come se fosse puro sarebbe
disonesto. Trattarlo come se fosse generato sarebbe falso.

Per questo il documento cambia nome. La paternità qui non è in discussione:
idea, struttura e tesi sono dell'autore. Quello che serve è una dichiarazione
di che cosa è stato fatto, e da chi.

La cornice resta quella della sezione 7. Il documento è la stessa pagina, con
gli stessi sei punti e gli stessi allegati; cambiano il titolo e il punto 5,
dove la tabella qui sotto prende il posto di «Perché è mio», che in questo
caso non serve, perché la paternità non è in discussione.

```text
DICHIARAZIONE D'USO

| Fase | Chi | Strumento | Che cosa esattamente |
|---|---|---|---|
| idea e tesi | | | |
| ricerca e fonti | | | |
| struttura | | | |
| stesura | | | |
| revisione di lingua | | | |
| traduzione | | | |
| formattazione | | | |
```

Si compila riga per riga, con il nome dello strumento e l'intervento reale.
«Correzione ortografica e di concordanze sul testo già scritto» dice qualcosa.
«Uso di AI» non dice niente e insospettisce.

Questa distinzione è oggi pratica corrente, e in ambito scientifico è una
regola scritta. L'ICMJE, il comitato che fissa gli standard editoriali delle
riviste mediche, chiede a chi usa strumenti di AI di «describe, in both the
cover letter and the submitted work in the appropriate section if applicable,
how they used it», e stabilisce che un chatbot non può comparire fra gli autori
«because they cannot be responsible for the accuracy, integrity, and
originality of the work». Da lì discende la frase che qui conta di più:
«humans are responsible for any submitted material that included the use of
AI-assisted technologies».

Chi dichiara si prende la responsabilità, e proprio per questo si trova in una
posizione migliore di chi tace: la mancata dichiarazione, secondo le stesse
raccomandazioni, può essere trattata come scorrettezza. Portarla spontaneamente
vale più che aspettare la domanda.

Un dato tecnico utile proprio in questa zona. Turnitin ha rilevato che oltre
la metà delle frasi segnalate per errore si trovava accanto a frasi
effettivamente generate. In un documento misto lo strumento sbava sulle frasi
umane vicine a quelle assistite. Chi ha fatto correggere un paragrafo può
quindi vedersi segnalare anche le frasi che lo circondano, che ha scritto da
solo.

**Dove si ferma.** Se la tesi, la struttura o il contenuto vengono dalla
macchina e la richiesta è di presentarli come propri, non c'è dichiarazione da
compilare né difesa da scrivere. Vale la sezione 1.

## 9. Cosa questo file non fa

**Non è consulenza legale.** Serve a parlare con una commissione, una
redazione, un committente. Se la controversia diventa un procedimento
disciplinare o civile, serve un avvocato, e questo documento diventa al
massimo materiale da consegnargli.

**Non promette l'esito.** Una difesa costruita bene può non bastare. Chi
promettesse il contrario venderebbe la stessa certezza infondata dei
rilevatori, con il segno rovesciato.

**Non abbassa nessun punteggio.** Non contiene modifiche da fare al testo, e
il passaggio 7 della sezione 6 spiega perché farle sarebbe anche
controproducente.

**Non dimostra che un testo è umano.** La prova di voce dimostra continuità
con quello che l'autore scriveva prima. È molto, e non è la stessa cosa.

**Non invecchia bene da solo.** I rilevatori cambiano in fretta e le cifre
della sezione 3 vanno rilette fra un anno. Il metodo delle sezioni 6 e 7
regge, perché non dipende da quale strumento è di moda.

---

**Legami.** `segnali-misurabili.md` sezione 8 declassa le liste di parole e i
rilevatori a segnale debole, ed è la base teorica di questo file.
`metodologie-operative.md` sezione 6 raccoglie le metriche stilometriche: lì
servono a diagnosticare un testo proprio, qui la stessa materia si legge al
contrario, per difendere. `voce-personale.md` fornisce la prova di voce del
passaggio 5. `checklist-finale.md` contiene la voce di controllo sui detector.

**Fonti,** verificate una a una il 2026-07-22:

- Liang, Yuksekgonul, Mao, Wu, Zou (2023), *GPT detectors are biased against non-native English writers*, Patterns 4(7), 100779, doi:10.1016/j.patter.2023.100779. Tasso medio di falsi positivi del 61,3 per cento su saggi TOEFL di studenti non madrelingua; 19,8 per cento segnalato all'unanimità da tutti i rilevatori esaminati; accuratezza buona sugli stessi testi scritti da madrelingua.
- Weber-Wulff, Anohina-Naumeca, Bjelobaba, Foltýnek, Guerrero-Dib, Popoola, Šigut, Waddington (2023), *Testing of detection tools for AI-generated text*, International Journal for Educational Integrity 19, art. 26, doi:10.1007/s40979-023-00146-z. Dodici strumenti pubblici più Turnitin e PlagiarismCheck: né accurati né affidabili, con bias prevalente verso la classificazione come umano.
- Sadasivan, Kumar, Balasubramanian, Wang, Feizi, *Can AI-Generated Text be Reliably Detected?*, Transactions on Machine Learning Research (prima versione 2023). Quadro teorico che lega l'accuratezza massima del miglior rilevatore possibile alla distanza fra distribuzione umana e distribuzione generata.
- OpenAI, nota sul ritiro dell'AI Text Classifier, 20 luglio 2023: «As of July 20, 2023, the AI classifier is no longer available due to its low rate of accuracy».
- Turnitin, comunicazioni della chief product officer Annie Chechitelli, giugno 2023: falso positivo sotto l'uno per cento sul documento intero per documenti con oltre il venti per cento di scrittura artificiale, circa quattro per cento a livello di frase, avviso di cautela introdotto sotto la soglia del venti per cento.
- Macko, Kopal (30 settembre 2025), *CEAID: Benchmark of Multilingual Machine-Generated Text Detection Methods for Central European Languages*, arXiv:2509.26051. La rilevazione è concentrata sull'inglese e i rilevatori esistenti risultano «almost unusable for non-English languages»; il trasferimento da una lingua all'altra «can have severely degraded performance»; tradurre in inglese per far analizzare il testo alza i falsi positivi. Il benchmark copre croato, ceco, tedesco, ungherese, polacco, slovacco e sloveno: l'italiano non è fra le lingue misurate.
- Macko et al. (2023), *MULTITuDE: Large-Scale Multilingual Machine-Generated Text Detection Benchmark*, EMNLP 2023, ACL Anthology 2023.emnlp-main.616. Undici lingue misurate: arabo, catalano, ceco, tedesco, inglese, spagnolo, olandese, portoghese, russo, ucraino, cinese. L'italiano non è fra queste. Gli autori dichiarano «a lack of research into capabilities of recent LLMs to generate convincing text in languages other than English and into performance of detectors of machine-generated text in multilingual settings».
- ICMJE, *Recommendations: Use of Artificial Intelligence-Assisted Technology by Authors*. Dichiarazione obbligatoria dell'uso di strumenti di AI nella lettera di accompagnamento e nel manoscritto; nessun chatbot fra gli autori, «because they cannot be responsible for the accuracy, integrity, and originality of the work»; «humans are responsible for any submitted material that included the use of AI-assisted technologies».
- Jabarian, Imas (settembre 2025), *Artificial Writing and Automated Detection*, NBER Working Paper 34223, anche BFI Working Paper 2025-116. Sostengono che «Independent studies that examine AI detection are out of date and focus on a set of tools that rely on antiquated techniques (Weber-Wulff et al., 2023)». Corpus umano da sei fonti inglesi: notizie CC-News, blog del Blog Authorship Corpus, curriculum dal dataset Kaggle, recensioni Yelp e Amazon, romanzi anteriori al 2000 da Project Gutenberg; equivalenti artificiali generati con GPT-4.1, Claude Opus 4, Claude Sonnet 4 e Gemini 2.0 Flash. Falsi positivi dei tre prodotti commerciali fra 0,1 e 0,7 per cento; il modello aperto RoBERTa base sbaglia invece sulla maggior parte dei testi umani, con falsi positivi «di circa il 30-78 per cento a seconda dello scenario», e gli autori lo dichiarano inadatto agli usi che pesano. La cifra viene dalla sintesi del Becker Friedman Institute, l'istituto che ospita gli autori: il PDF del working paper non si è lasciato leggere dagli strumenti usati per la verifica, quindi la percentuale non è stata confermata sul primario. «Pangram is the only tool to satisfy a strict cap (FPR 0.005) without sacrificing accuracy». Nessun elaborato scolastico, nessuno scrivente non madrelingua e nessuna lingua diversa dall'inglese nel corpus.
- Vanderbilt University, *Guidance on AI Detection and Why We're Disabling Turnitin's AI Detector*, 16 agosto 2023. Decisione istituzionale motivata, non una misura: assenza di trasparenza, falsi positivi documentati altrove, maggiore esposizione di chi non è madrelingua inglese, e il conto dei 750 elaborati su 75.000.

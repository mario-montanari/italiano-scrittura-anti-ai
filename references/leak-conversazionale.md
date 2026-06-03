# Leak del registro conversazionale

Un modello linguistico nasce per rispondere in chat a un interlocutore. Quando gli si chiede di scrivere un documento (un articolo, un capitolo, una scheda prodotto, una newsletter), il riflesso della conversazione resta acceso e cola dentro il testo. Il risultato è una prosa che parla a un lettore come se rispondesse a una domanda che il lettore non ha fatto, in una conversazione a cui non ha partecipato.

Questo file isola quel riflesso. Diversi pattern già trattati altrove (i meta-annunci di `pattern-strutturali.md` sezione 5, il tono servile della sezione 19, i contrasti fittizi della sezione 11) sono casi particolari dello stesso fenomeno: il modello scrive in modalità chat dentro un testo che dovrebbe stare in piedi da solo. Inquadrarli come leak del registro conversazionale aiuta a riconoscerli tutti insieme e a correggerli alla radice con una sola domanda.

**La domanda da porsi.** Chi legge questo documento non era nella stanza quando l'ho scritto. Non ha visto il prompt, non ha posto domande, non ha equivoci da correggere. Sta solo leggendo. Allora perché il testo gli risponde?

## Indice

1. [La negazione che corregge un equivoco inesistente](#1-la-negazione-che-corregge-un-equivoco-inesistente)
2. [La suspense inutile «qui sta il punto»](#2-la-suspense-inutile-qui-sta-il-punto)
3. [I riassunti frattali di una conversazione mai avvenuta](#3-i-riassunti-frattali-di-una-conversazione-mai-avvenuta)
4. [Le domande poste al posto del lettore](#4-le-domande-poste-al-posto-del-lettore)
5. [Come si corregge alla radice](#5-come-si-corregge-alla-radice)

---

## 1. La negazione che corregge un equivoco inesistente

Il pattern più subdolo è la struttura «non è X, è Y». Sembra precisione. In realtà corregge un malinteso che nessun lettore aveva, perché il lettore non aveva ancora pensato a X. La negazione introduce X solo per poterla smentire, e così crea il problema che finge di risolvere.

In chat ha senso: l'utente ha appena detto X, e il modello lo corregge. In un documento no: il lettore arriva vergine, e la negazione gli pianta in testa un'idea sbagliata un istante prima di toglierla.

**Esempio negativo:**

> «La SEO non è una formula magica, è un lavoro di mesi. Le parole chiave non sono semplici parole, sono segnali di domanda. Il self-publishing non è un arricchimento rapido, è un mestiere.»

Tre negazioni di fila, ognuna delle quali evoca un'idea sciocca (formula magica, semplici parole, arricchimento rapido) solo per smentirla. Il lettore non aveva nessuna di quelle idee.

**Correzione:** affermare direttamente, senza la stampella della negazione.

> «La SEO è un lavoro di mesi. Le parole chiave sono segnali della domanda reale del pubblico. Il self-publishing è un mestiere, e come ogni mestiere si impara col tempo.»

**Quando la negazione è legittima.** Se l'equivoco esiste davvero ed è diffuso, smentirlo è giusto: *Molti credono che pubblicare su KDP costi, ma l'iscrizione è gratuita.* Qui la falsa credenza è reale e nominata come tale. La regola: negare solo ciò che il lettore pensa davvero, non ciò che serve a costruire una frase a effetto.

## 2. La suspense inutile «qui sta il punto»

Formule come *qui sta il punto, ecco la cosa, ed è proprio questo il bello, e qui viene il difficile* costruiscono attesa per un lettore che vuole solo l'informazione. Sono battute da conversazione, dove l'attesa di un istante è naturale. In un testo scritto rallentano e basta: chi legge può andare alla riga dopo da solo, non ha bisogno di un rullo di tamburi.

**Esempio negativo:**

> «Esistono molti strumenti per le parole chiave. Ma ecco la cosa: quasi nessuno guarda il dato che conta davvero. E qui sta il punto: il numero di concorrenti.»

Due annunci di rivelazione per dire una cosa sola, che si poteva dire subito.

**Correzione:**

> «Esistono molti strumenti per le parole chiave, ma quasi nessuno guarda il dato che conta: il numero di concorrenti.»

**Variante da sorvegliare.** Anche *la verità è che, il fatto è che, diciamoci la verità, sia chiaro* appartengono alla stessa famiglia. Nove volte su dieci si tagliano e la frase migliora.

## 3. I riassunti frattali di una conversazione mai avvenuta

Il modello tende a ricapitolare. In chat è utile, perché tiene il filo di uno scambio lungo. In un documento diventa un riassunto frattale: ogni sezione si apre ricapitolando quella prima e si chiude annunciando quella dopo, e il testo passa più tempo a parlare di sé stesso che a dire qualcosa. È la versione strutturale del meta-annuncio.

**Segni.** Un paragrafo che riassume cosa è stato detto *finora*. Una sezione che si apre con *come abbiamo visto* e si chiude con *vedremo ora come*. Una chiusura che ripete i punti già esposti invece di aggiungere qualcosa (vedi anche le chiusure stereotipate in `lessico-da-evitare.md` sezione 8).

**Esempio negativo:**

> «Come abbiamo visto nel paragrafo precedente, la scelta della nicchia è decisiva. Ora che abbiamo chiarito questo aspetto, possiamo passare alle parole chiave. Nel prossimo paragrafo vedremo invece come si analizza la concorrenza.»

Tre frasi, zero contenuto: il testo descrive il proprio indice.

**Correzione:** togliere le impalcature e attaccare il contenuto. Un buon testo scritto non ha bisogno di annunciare i suoi snodi, perché il lettore può tornare indietro quando vuole, cosa che in una conversazione parlata non potrebbe fare.

> «Scelta la nicchia, restano le parole chiave. La domanda è una sola: quante persone cercano questa cosa, e quanti libri già rispondono?»

## 4. Le domande poste al posto del lettore

*Ti starai chiedendo come fare. Ma cosa significa davvero tutto questo? Andiamo a scoprirlo insieme.* Sono domande che il testo mette in bocca al lettore per poi rispondere. Riproducono il botta e risposta della chat in un monologo. Il lettore non si stava chiedendo niente: stava leggendo.

**Esempio negativo:**

> «Ti starai chiedendo: conviene davvero pubblicare in inglese? E quante royalty si guadagnano? Bene, andiamo a vedere insieme.»

**Correzione:** entrare nel merito senza la finta domanda.

> «Pubblicare in inglese allarga il mercato ma alza la concorrenza. Sulle royalty il calcolo cambia a seconda del prezzo di copertina e del peso del file: ecco i numeri.»

Questo pattern coincide in parte con le aperture interrogative generiche già bandite (vedi `lessico-da-evitare.md` sezione 7, *Ti sei mai chiesto…?*). Qui la radice è la stessa: il dialogo che invade il monologo.

## 5. Come si corregge alla radice

Tutti i pattern di questo file si curano con un'unica operazione mentale, da fare prima della revisione di dettaglio.

Rileggere il testo immaginando un lettore che non ha mai parlato con chi scrive. Non ha letto il prompt. Non ha posto domande. Non ha equivoci da sciogliere. Ha in mano solo il documento, magari trovato online sei mesi dopo. A quel lettore le negazioni preventive, i rulli di tamburi, i riassunti di sé stesso e le domande messe in bocca non servono a niente: gli tolgono tempo.

Tre mosse pratiche:

- Cercare le aperture *non è… è…, qui sta il punto, ecco la cosa, ti starai chiedendo, come abbiamo visto, andiamo a vedere insieme* e valutare ogni occorrenza con la domanda: il lettore aveva davvero bisogno di questo, o sto rispondendo a una conversazione?
- Affermare invece di negare, salvo quando l'equivoco è reale e diffuso.
- Tagliare i ponti meta-testuali fra le sezioni: in un testo scritto il lettore naviga da solo.

La regola di fondo è quella della fonte: quando scrivi un documento, scrivi per chi legge. Non ha nessun contesto della conversazione che ha prodotto il documento.

---

*Concetti adattati dal repo `creative-writing-skills` di haowjy, licenza Apache 2.0.*

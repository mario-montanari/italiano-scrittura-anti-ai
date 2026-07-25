# Segnali misurabili

I cataloghi di parole sospette degli altri file (`lessico-da-evitare.md`, `pattern-strutturali.md`) sono uno strumento di gusto, non un rilevatore. Questo file raccoglie i segnali di prosa AI che hanno una base nella ricerca peer-reviewed, cioè misurabili su un testo e confrontabili con la prosa umana di pari lunghezza e genere.

La distinzione conta perché cambia il modo di lavorare. Una parola spia si cerca con Trova nel testo e si valuta a occhio. Un segnale misurabile si conta: varietà del lessico, densità di pronomi personali, distribuzione delle emozioni, profondità dell'interiorità, presenza di sottotesto. Nessuno di questi, da solo, prova che un testo sia stato generato da una macchina. Insieme, e su un campione di paragrafi, orientano meglio di qualsiasi lista di vocaboli.

Importante: la ricerca citata sotto studia in prevalenza la narrativa e l'inglese. Per la saggistica e la divulgazione italiane i meccanismi reggono, ma i numeri di soglia vanno presi come ordine di grandezza, non come verdetto.

## Indice

1. [Perché i segnali misurabili battono le liste di parole](#1-perché-i-segnali-misurabili-battono-le-liste-di-parole)
2. [Minore varietà lessicale](#2-minore-varietà-lessicale)
3. [Meno pronomi personali](#3-meno-pronomi-personali)
4. [Eccesso di emozioni positive](#4-eccesso-di-emozioni-positive)
5. [Interiorità superficiale](#5-interiorità-superficiale)
6. [Basso sottotesto](#6-basso-sottotesto)
7. [Template sintattici ripetuti](#7-template-sintattici-ripetuti)
8. [Il punto chiave: le liste di parole non sono un rilevatore](#8-il-punto-chiave-le-liste-di-parole-non-sono-un-rilevatore)

---

## 1. Perché i segnali misurabili battono le liste di parole

Una lista di parole sospette (*delve, tappeto, testimonianza, sfaccettato*) ha tre debolezze strutturali che un segnale misurabile non ha.

Dipende dalla versione del modello: le frequenze cambiano a ogni aggiornamento, e una parola tipica di un modello sparisce dal successivo. Dipende dal prompt: un'istruzione di stile cambia il vocabolario in modo radicale. È confusa dal genere: *approfondire* compare in moltissima prosa accademica umana, *orizzonte* in moltissima divulgazione umana.

Un segnale misurabile, invece, descrive una proprietà strutturale del modo in cui la macchina genera testo, non una sua moda lessicale passeggera. La varietà del lessico cala perché il modello tende verso l'esito statisticamente più probabile. I pronomi personali calano perché la prosa è riferita più che vissuta. Sono effetti del meccanismo, non della stagione.

La conseguenza pratica è semplice: quando si revisiona, conviene misurare i segnali di questo file e usare le liste degli altri file solo come preferenza di gusto, non come prova.

## 2. Minore varietà lessicale

La prosa AI tende a riusare un vocabolario di lavoro più ristretto rispetto alla prosa umana di lunghezza e genere comparabili. È il segnale più solido e il più studiato.

**Come si misura.** Con il MATTR (Moving Average Type-Token Ratio): si fa scorrere una finestra di lunghezza fissa (per esempio 50 parole) lungo il testo, si calcola in ogni finestra il rapporto fra parole diverse e parole totali, si fa la media. Il MATTR è preferibile al type-token ratio grezzo, che è inaffidabile perché cala automaticamente al crescere della lunghezza del testo e quindi non permette di confrontare testi di taglia diversa.

**Come si riconosce a occhio, senza strumenti.** Stesso sostantivo astratto che torna a distanza di poche righe (*approccio… approccio… approccio*). Lo stesso verbo di servizio che regge tre frasi su quattro (*permette di… consente di… consente di*). Un ventaglio di aggettivi che pesca sempre dallo stesso registro valutativo (*importante, significativo, rilevante, fondamentale*).

**Esempio.**

> «L'analisi delle parole chiave è un approccio fondamentale. Questo approccio permette di individuare nicchie rilevanti. Un approccio strutturato permette risultati significativi.»

Tre volte *approccio*, due volte *permette*, la coppia *fondamentale / rilevante / significativi*. La finestra mobile crollerebbe. Riscrittura:

> «L'analisi delle parole chiave serve a trovare le nicchie dove c'è domanda e manca offerta. Si parte dal volume di ricerca, si incrocia con il numero di concorrenti, si scartano le code troppo affollate.»

**Nota.** Varietà lessicale alta non vuol dire infilare sinonimi rari. Quello è un altro tic, la variazione elegante (vedi `pattern-strutturali.md` sezione 10). La varietà sana nasce dal dire cose diverse, non dal travestire la stessa cosa con parole diverse.

Riferimento: Kobak et al. (2024) misurano in oltre quattordici milioni di abstract biomedici PubMed un aumento brusco e senza precedenti di alcune parole di stile dopo l'uscita di ChatGPT, con un metodo del vocabolario in eccesso ispirato agli studi sull'eccesso di mortalità.

## 3. Meno pronomi personali

I testi generati da modelli usano meno pronomi di prima e seconda persona (*io, mi, mio; tu, ti, tuo*) in rapporto al totale delle parole. La prosa suona più riferita che vissuta: qualcuno racconta i fatti dall'esterno invece di attraversarli.

**Come si misura.** Si conta la frequenza dei pronomi di prima persona singolare e di seconda persona rispetto al totale delle parole, e si confronta con quella attesa per il genere. In un pezzo in prima persona, un conteggio anomalo di *io / mi / mio* è un segnale da indagare.

**Come si riconosce.** Un testo che dovrebbe parlare di un'esperienza diretta e invece scivola sempre nell'impersonale (*si nota che, è possibile osservare, va considerato*). Una pagina di blog firmata da un autore reale in cui l'autore non compare mai come soggetto.

**Esempio (saggistica in prima persona).**

> «È possibile osservare che il self-publishing richiede costanza. Si nota inoltre che i primi mesi sono i più difficili. Va considerato che molti abbandonano presto.»

Tre impersonali di fila, zero *io*, in un pezzo che dovrebbe essere testimonianza. Riscrittura:

> «Il self-publishing chiede costanza, e i primi mesi me li ricordo come i più duri. Ho visto parecchi mollare prima del sesto libro. Io stesso, all'inizio, ci ho pensato.»

**Attenzione al registro.** Questo segnale vale per testi dove la persona ha senso: blog, opinione, testimonianza, lettera, divulgazione con autore visibile. Nella prosa tecnica, scientifica o normativa l'impersonale è corretto e atteso, e l'assenza di *io* non è un difetto. Il segnale si applica solo dove l'esperienza diretta giustificherebbe la prima persona.

## 4. Eccesso di emozioni positive

La prosa AI pende verso il sentimento positivo, anche in passaggi che dovrebbero essere neutri o cupi. La macchina addolcisce. È lo stesso meccanismo della neutralità artificiale (vedi `pattern-strutturali.md` sezione 17), visto però dal lato del tono emotivo invece che da quello della posizione.

**Come si riconosce.** Una difficoltà raccontata e subito ricomposta nello stesso paragrafo, con la morale consolatoria già pronta. Una situazione dura descritta cercando comunque il lato buono. Reazioni emotive che si risolvono troppo in fretta e troppo bene, senza lasciare residuo.

**Esempio (divulgazione su un tema duro).**

> «Perdere il lavoro è stato un colpo, ma si è rivelata un'occasione preziosa per reinventarsi e scoprire nuove opportunità di crescita personale.»

La frase non lascia respirare il colpo: lo trasforma subito in opportunità. È il riflesso consolatorio della macchina. Riscrittura, che tiene la durezza:

> «Perdere il lavoro è stato un colpo. Per qualche mese non ho saputo cosa fare. La reinvenzione è arrivata dopo, e non perché fosse scritta da qualche parte che dovesse arrivare.»

**Regola pratica.** Non aggiungere il lato positivo per dovere. Se il fatto è cupo, può restare cupo. Una complessità ammessa (vedi `personalita-e-anima.md` sezione 2, tecnica tre) vale più di un finale rassicurante.

## 5. Interiorità superficiale

Quando il testo dà accesso al pensiero di qualcuno (un personaggio in narrativa, l'autore in un saggio, un caso esemplare in divulgazione), la macchina tende a riassumere il pensiero invece di farlo accadere. Il pensiero risulta sempre completo, ordinato, già concluso. Manca il pensiero reale, che è associativo, interrotto, a volte sgangherato.

**Segni.** I pensieri sono sempre frasi grammaticalmente complete e logicamente ordinate. Non ci sono pensieri intrusi, divagazioni, correzioni a metà. Gli stati d'animo vengono nominati invece che fatti provare (*provò una ondata di determinazione* invece di mostrare cosa fa chi è determinato).

**Esempio (caso in un testo divulgativo).**

> «Giulia capì che doveva cambiare strategia. Provò un senso di rinnovata motivazione e decise con sicurezza di puntare su una nicchia diversa.»

Il pensiero è un riassunto pulito, l'emozione è etichettata (*senso di rinnovata motivazione*). Riscrittura:

> «Giulia riaprì il file delle vendite per la terza volta quella sera. Sempre quei numeri. La nicchia non tirava, lo sapeva da settimane e aveva fatto finta di niente. Forse il problema non era il libro. Forse era la categoria. Chiuse il portatile senza decidere niente, e l'indomani aprì lo strumento delle parole chiave su un'altra nicchia.»

Pensiero che procede a strappi, dubbio reale, decisione che matura invece di essere annunciata.

## 6. Basso sottotesto

Nelle conversazioni e nei dialoghi, la macchina fa dire ai personaggi esattamente quello che pensano. Il sottotesto, cioè lo scarto fra ciò che si dice e ciò che si intende, è raro. I dialoghi sono efficienti invece che realistici.

**Segni.** I personaggi dichiarano i propri sentimenti in modo chiaro. I disaccordi vengono enunciati invece di essere mostrati attraverso l'evasione, il cambio di argomento, il gesto. Non esistono scambi in cui il vero tema non viene mai nominato.

**Esempio (dialogo in un libro o in un caso narrato).**

> «Sono arrabbiato perché non mi hai consultato prima di pubblicare», disse Marco. «Hai ragione, avrei dovuto. Mi dispiace di averti ferito», rispose Anna.

Tutto detto, niente sottinteso. Nella realtà le persone girano intorno alle cose. Riscrittura:

> «Bel lavoro», disse Marco senza alzare gli occhi dallo schermo. «L'hai già messo online, vedo». Anna posò il caffè. «Volevo dirtelo». «Certo». Tornò a scorrere la pagina. «Comodo, deciderlo da soli».

Nessuno dei due nomina il problema. Si capisce lo stesso, anzi si capisce meglio.

**Per la saggistica.** Il sottotesto puro è una faccenda da narrativa. Nella divulgazione l'equivalente è la fiducia nel lettore: non spiegare la conclusione che il lettore può trarre da solo dai fatti che gli hai dato (vedi `canali-lettore-saggistica.md` sezione 1).

## 7. Template sintattici ripetuti

Oltre alle parole, si ripete la struttura. I modelli producono sequenze sintattiche ricorrenti (per esempio lo stesso schema di soggetto, verbo di servizio e completiva) a una frequenza più alta di quella della prosa umana di riferimento. È una ripetizione invisibile a chi cerca solo le parole, perché le parole cambiano mentre lo scheletro resta uguale.

**Come si riconosce.** Cinque frasi che, tolte le parole, hanno lo stesso disegno: *[soggetto] + [verbo modale] + [verbo all'infinito] + [complemento]*. Aperture di paragrafo tutte sullo stesso calco. Elenchi in cui ogni voce ripete la medesima architettura.

**Esempio.**

> «Questo strumento permette di analizzare i dati. Questa funzione consente di esportare i report. Questa opzione permette di filtrare i risultati.»

Tre frasi, un solo scheletro. Riscrittura che varia la struttura:

> «Con questo strumento analizzi i dati. I report si esportano in un clic. E se i risultati sono troppi, basta un filtro.»

Riferimento: Shaib, Elazar, Li, Wallace (2024) definiscono i template sintattici come sequenze di categorie grammaticali e mostrano che i modelli li producono a un tasso più alto dei testi umani di riferimento, e che questi template risalgono ai dati di pre-addestramento e sopravvivono al fine-tuning.

## 8. Il punto chiave: le liste di parole non sono un rilevatore

Le liste di parole sospette (*delve, tappeto di, testimonianza, sfaccettato, navigare il panorama*) circolano come se fossero un test di paternità del testo. Non lo sono.

Sono inaffidabili per quattro ragioni. Dipendono dalla versione del modello: le frequenze cambiano a ogni rilascio, e una parola spia di oggi è un falso negativo domani. Dipendono dal prompt: basta un'istruzione di stile a riscrivere il vocabolario. Sono confuse dal genere: parole additate come AI compaiono in abbondanza nella prosa umana accademica e di genere. E sono quasi casuali per un modello specifico: un'euristica costruita sull'output di un modello non si trasferisce a un altro.

Un dettaglio che lo dimostra: dopo che nel 2024 alcune parole tipiche (come *delve*) sono state additate pubblicamente, la loro frequenza è calata, segno che chi scrive con l'AI ha imparato a selezionare o correggere l'output. La lista, appena diventa nota, smette di funzionare come rilevatore.

Questo non rende le liste inutili. Restano un'ottima **preferenza di gusto editoriale**: «non voglio che la mia prosa suoni così» è una scelta legittima e in molti casi giusta. Ma è una scelta di stile, non una prova di autorialità artificiale. Chi usa le liste deve essere onesto su questo punto: gusto, non diagnosi.

I detector automatici basati su queste euristiche meritano la stessa cautela. Dove il falso positivo è stato misurato, cioè sull'inglese, è risultato grande; sull'italiano nessuno lo ha misurato, e i due benchmark multilingue che coprono sedici lingue lasciano fuori la nostra. Il loro responso è un segnale debole da incrociare con i segnali misurabili di questo file, non un verdetto. Quando quel responso diventa un'accusa, il metodo per rispondere è in `scudo-falsi-positivi.md`.

Riferimenti scientifici principali di questo file:

- Kobak, González-Márquez, Horvát, Lause (2024), *Delving into LLM-assisted writing in biomedical publications through excess vocabulary*, arXiv:2406.07016. Vocabolario in eccesso e parole di stile come marcatori d'uso degli LLM nella scrittura scientifica; calo di *delve* dopo la sua segnalazione pubblica.
- Shaib, Elazar, Li, Wallace (2024), *Detection and Measurement of Syntactic Templates in Generated Text*, EMNLP 2024, arXiv:2407.00211. Template sintattici ripetuti come tratto strutturale del testo generato, tracciabili ai dati di addestramento.
- Covington, McFall (2010), *Cutting the Gordian Knot: The Moving-Average Type-Token Ratio (MATTR)*, Journal of Quantitative Linguistics. Metrica a finestra mobile per la varietà lessicale, robusta rispetto alla lunghezza del testo.

---

*Concetti adattati dal repo `creative-writing-skills` di haowjy, licenza Apache 2.0. Le citazioni scientifiche sono state verificate e dove necessario corrette rispetto al materiale sorgente.*

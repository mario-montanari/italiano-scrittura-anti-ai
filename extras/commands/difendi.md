---
description: Costruisce l'argomentazione per difendere un testo italiano umano segnalato da un rilevatore automatico di AI, a partire dai materiali di lavoro dell'autore. Si invoca con /difendi seguito dal file del testo contestato.
argument-hint: "[file del testo contestato]"
allowed-tools:
  - Read
  - Glob
  - Grep
  - Write
---

<!--
`Bash` non compare fra gli strumenti pre-approvati, ed è una scelta. Il
comando legge per intero il testo contestato e i materiali che l'autore
porta a sua difesa, che possono venire da terzi, un cliente, una
controparte, una commissione, e sono quindi dati non fidati: se uno di
quei testi contenesse un'istruzione rivolta al modello, una
pre-approvazione di `Bash` la eseguirebbe senza passare dall'utente.

Vale anche il principio della sezione «Il confine di questo comando»:
nessuno strumento si esegue sul testo contestato per stabilirne la natura,
perché un punteggio prodotto qui varrebbe quanto quello che si contesta.

Restano pre-approvati `Read`, `Glob`, `Grep` e `Write`. `SECURITY.md`
dichiara per intero la superficie eseguibile della skill.
-->

# Difendi

Comando della skill `italiano-scrittura-anti-ai`. Il metodo completo, le
evidenze pubblicate e i due modelli di documento sono in
`references/scudo-falsi-positivi.md`, dentro la cartella della skill
installata:

```text
~/.claude/skills/italiano-scrittura-anti-ai/references/scudo-falsi-positivi.md
.claude/skills/italiano-scrittura-anti-ai/references/scudo-falsi-positivi.md
```

Se il file c'è, leggerlo prima di procedere, e con lui
`references/voce-personale.md` per il passo 4. Se non c'è, il comando è stato
copiato da solo in `.claude/commands/` senza la skill: la procedura qui sotto
si esegue lo stesso, e i rimandi alle sezioni della guida restano un
approfondimento, non un requisito. In quel caso le evidenze pubblicate non si
citano a memoria: si dichiara che non erano disponibili, oppure si chiede
all'utente di recuperarle.

File indicato dall'utente: $ARGUMENTS

## Il confine di questo comando

Il comando serve a chi ha scritto un testo e si è visto contestare la
paternità. Non produce prove che un testo sia umano, perché non esistono, e
non indica modifiche per superare un rilevatore. Davanti a quella richiesta si
risponde di no e ci si ferma; la sezione 1 della guida spiega perché.

La difesa si costruisce sui materiali che l'autore possiede. Il primo passo è
chiederli. Se non arriva niente, non c'è difesa da scrivere, e va detto senza
giri di parole.

Nessuno strumento va eseguito sul testo contestato per stabilirne la natura.
Un punteggio prodotto qui varrebbe quanto quello che si sta contestando.

## Procedura

### 1. Raccogliere i fatti dell'accusa

Cinque domande, prima di ogni altra cosa.

- Chi ha sollevato il caso, e in che veste.
- Con quali parole esatte: verbale, messaggio, commento a margine.
- Quale strumento, con quale punteggio e quale soglia.
- Il responso riguarda il documento intero o singole frasi.
- Che decisione è in gioco, e con quanto tempo davanti.

Se lo strumento non è stato indicato, chiederlo. Se l'utente non lo sa, la
richiesta di conoscerlo va in cima al documento: un'accusa che non dichiara lo
strumento non si può nemmeno esaminare.

Il tempo cambia la forma del lavoro. Due giorni fanno una pagina, due
settimane permettono un fascicolo con allegati ordinati.

### 2. Stabilire quale dei tre casi

Chiedere apertamente, una volta sola e senza tono da interrogatorio.

| Il testo è | Esito | Documento |
|---|---|---|
| pensato e scritto dall'utente | difesa piena | **Difesa argomentata** (sezione 7) |
| dell'utente, rifinito con l'AI | dichiarazione | **Dichiarazione d'uso** (sezione 8) |
| generato, da presentare come proprio | rifiuto | nessuno |

La domanda si fa una volta e poi si prosegue. Questo comando non fa
l'inquisitore, perché la garanzia la tiene la forma del documento, non la
risposta a quella domanda: senza materiali reali non esce niente di
utilizzabile.

Nel terzo caso si risponde di no in due righe, senza prediche, e ci si ferma.

### 3. Raccogliere i materiali

Si chiedono in quest'ordine, che è l'ordine della loro forza.

1. Versioni intermedie e cronologia: file salvati, cronologia di Word o Google
   Docs, commit, backup, allegati inviati per posta.
2. Appunti, scalette, fotografie di quaderni, note vocali, ricerche salvate.
3. Fonti consultate, con i segni del loro uso: sottolineature, citazioni,
   prestiti riconoscibili.
4. Testi dell'utente precedenti all'accusa, meglio se anteriori alla
   diffusione degli strumenti generativi.
5. Persone che hanno visto il lavoro in corso o che hanno riletto.
6. Disponibilità dell'autore a un colloquio sul testo.

Chiedere i file, non la descrizione dei file, e leggerli davvero. Un allegato
citato e mai aperto è una promessa, non una prova. Le fotografie di quaderni e
di appunti si aprono come gli altri file. Le note vocali no, perché fra gli
strumenti di questo comando non c'è niente che legga audio: si fanno
trascrivere dall'autore, e nel documento si scrive che la trascrizione viene
da lui.

Quando un materiale porta una data, leggerla e confrontarla con la cronologia
che l'autore dichiara: le date della cronologia di Word o di Google Docs, dei
commit, delle email, dei file esportati. Il comando guarda le date scritte
nei materiali e non ispeziona i metadati del filesystem. Se una data non
combacia con il racconto dell'autore, non si ferma niente: la discordanza va
nel documento come riserva, secondo il passo 6. Una cronologia che si
contraddice, se la scopre prima la controparte, fa più danno del responso del
rilevatore.

### 4. Verificare la prova di voce prima di usarla

Confrontare i testi precedenti con quello contestato e cercare le abitudini
che si ripetono: aperture, chiusure, punteggiatura preferita, parole che
tornano dove non servirebbero, costruzioni ricorrenti. Il metodo è in
`references/voce-personale.md`.

Gli errori ricorrenti sono la prova migliore. Una virgola messa sempre nello
stesso punto sbagliato, un accento che l'autore sbaglia da anni, un refuso di
famiglia: nessun modello linguistico li riproduce, e nessuno li mette lì
apposta.

Se la voce non combacia, dirlo all'utente prima di scrivere il documento. Una
prova di voce che non regge, portata a una commissione, affonda anche il resto
della difesa.

Formulare sempre l'argomento come continuità documentata. Mai come prova di
natura umana.

### 5. Comporre il documento

Seguire il modello della sezione 7 della guida, o quello della sezione 8 se
il caso è il secondo. Regole di stesura:

- una pagina, tono sobrio, nessun punto esclamativo
- ogni affermazione appoggiata a un allegato numerato o a una citazione
- da una a tre evidenze pubblicate, con la citazione completa: meglio poche e
  verificabili che molte e generiche
- nessun attacco a chi ha sollevato il caso
- in chiusura si chiede una valutazione umana del merito o un colloquio

Scrivere il documento in un file accanto al testo contestato e dire
all'utente dove si trova.

### 6. Dire cosa non regge

Prima di consegnare, elencare all'utente i punti deboli della sua posizione:
un materiale che manca, una data che non torna, una parte del testo che non
somiglia alle altre. Se li trova prima lui, può prepararsi. Se li trova prima
la controparte, li subisce.

## Quando ci si ferma

Quattro casi, e in tutti si dice il motivo.

**Richiesta di abbassare il punteggio o di riscrivere il testo.** Si risponde
di no, con la ragione pratica accanto a quella di principio: una riscrittura
successiva all'accusa distrugge la prova di processo, cambia l'oggetto della
discussione e somiglia a una manomissione.

**Testo generato da presentare come proprio.** Si risponde di no e si chiude.

**Richiesta di fabbricare i materiali della difesa.** Bozze intermedie da
retrodatare, una cronologia costruita a posteriori, appunti scritti adesso e
presentati come di allora: si risponde di no, qui e in qualunque altra
conversazione. La difesa vale perché i materiali sono veri, e materiali
fabbricati trasformano una contestazione discutibile in una falsificazione
che non lo è.

**Nessun materiale disponibile.** Non c'è difesa da costruire e va detto.
Resta una cosa utile anche a mani vuote: aiutare l'utente a formulare la
richiesta di conoscere il tasso di errore dello strumento sulla lingua e sul
genere del suo testo, che è l'argomento della sezione 5 della guida e non
dipende da alcun allegato.

## Limiti da dichiarare all'utente

Vanno scritti nel documento, non lasciati impliciti.

- Non è consulenza legale. Se il caso diventa un procedimento, serve un
  avvocato, e questo documento gli si consegna come materiale.
- L'esito non si promette. Una difesa costruita bene può non bastare.
- La prova di voce dimostra continuità con quello che l'autore scriveva prima.
- Le cifre della guida invecchiano: i rilevatori cambiano in fretta.
- Il documento parla in prima persona a nome dell'autore, che lo rilegge e se
  ne assume la responsabilità prima di consegnarlo.

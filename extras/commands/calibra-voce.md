---
description: Cattura la voce di chi scrive a partire da un corpus di suoi testi italiani e produce una scheda voce in due livelli, misurato e osservato. Si invoca con /calibra-voce seguito dalla cartella dei testi.
argument-hint: "[cartella dei testi]"
allowed-tools:
  - Read
  - Glob
  - Grep
  - Write
---

<!--
`Bash` non compare fra gli strumenti pre-approvati, ed è una scelta. Il
passo 3 impone di leggere per intero i testi del corpus, che possono venire
da un cliente e sono quindi dati non fidati: se uno di quei testi contenesse
un'istruzione rivolta al modello, una pre-approvazione di `Bash` la
eseguirebbe senza passare dall'utente.

Restringere il pattern non basterebbe. In `Bash(python *profilo_voce.py *)`
l'asterisco attraversa spazi e separatori di cartella, quindi quel pattern
vincola il nome del file e non il percorso: un file omonimo messo altrove vi
rientrerebbe.

Lo strumento si lancia lo stesso, con la conferma dell'utente a ogni
esecuzione. Chi calibra spesso e vuole togliere quella conferma trova un
hook `PreToolUse` facoltativo in `extras/hooks/`, che pre-approva quel solo
comando dopo aver risolto il percorso e verificato che stia sotto una cartella
dove le skill si installano davvero.

Restano pre-approvati `Read`, `Glob`, `Grep` e `Write` senza restrizione di
percorso: la cartella del corpus e quella di uscita cambiano a ogni uso, e
`allowed-tools` non sa esprimere «solo quelle indicate adesso dall'utente».
`SECURITY.md` lo dichiara per intero.
-->

# Calibra voce

Comando della skill `italiano-scrittura-anti-ai`. Il metodo completo, le
decisioni di conteggio e il modello di scheda sono in
`references/voce-personale.md`, dentro la cartella della skill installata:

```text
~/.claude/skills/italiano-scrittura-anti-ai/references/voce-personale.md
.claude/skills/italiano-scrittura-anti-ai/references/voce-personale.md
```

Se il file c'è, leggerlo prima di procedere. Se non c'è, il comando è stato
copiato da solo in `.claude/commands/` senza la skill: si procede lo stesso,
perché ogni passo qui sotto porta con sé quello che serve, e si dichiara nella
scheda che il metodo esteso non era disponibile.

Cartella indicata dall'utente: $ARGUMENTS

## Cosa produce

Una scheda voce che tiene separati due livelli, e li dichiara come tali.

- **Misurato**: conteggi riproducibili. Chiunque, con lo stesso corpus,
  ottiene gli stessi numeri.
- **Osservato**: gesti, tic, rifiuti, postura verso il lettore. Nasce dalla
  lettura, e ogni affermazione porta con sé il passo che la dimostra.

Un'affermazione senza numero e senza citazione non entra nella scheda.

## Procedura

### 1. Verificare il corpus prima di misurarlo

Se l'utente non ha indicato una cartella, chiederla. Poi controllare tre
condizioni. Solo la prima può fermare il lavoro; le altre due non lo
fermano, ma vanno dichiarate nella scheda.

**Un solo registro.** I testi devono venire dalla stessa voce nello stesso
contesto. Un saggio e una newsletter sono due voci; i testi scritti per un
cliente sono la voce del cliente. Mescolarli produce la media di due persone,
che non somiglia a nessuna delle due. Elencare i file trovati e chiedere
conferma all'utente che appartengano tutti allo stesso registro. Se non è
così, fermarsi: si separano i registri e si calibra su uno solo.

**Almeno duemila parole.** Sotto quella soglia i numeri ballano. Si può
procedere, dichiarando il profilo come indicativo.

**Voce reale o voce desiderata.** Chiedere quale delle due si sta catturando:
come l'autore scrive oggi, o come vorrebbe scrivere. Sono documenti diversi.
La risposta va scritta in cima alla scheda.

### 2. Calcolare il livello misurato

Cercare lo strumento nei percorsi consueti di installazione della skill:

```text
~/.claude/skills/italiano-scrittura-anti-ai/scripts/profilo_voce.py
.claude/skills/italiano-scrittura-anti-ai/scripts/profilo_voce.py
```

Se lo si trova, eseguirlo:

```bash
python <percorso>/profilo_voce.py <cartella> --nome "<nome autore>" --out <cartella-di-uscita>
```

Su Windows il comando è `python`, altrove di solito `python3`. Claude Code
chiede conferma prima di eseguirlo: è voluto, e vale per ogni lancio.

Conviene indicare sempre `--out`. Senza, la scheda e i dati finiscono accanto
ai testi. Nessun file dell'utente viene però sovrascritto: lo strumento firma
le proprie uscite e riscrive senza chiedere soltanto quelle. Davanti a un file
omonimo che non riconosce come proprio si ferma senza toccarlo, dice quale ha
trovato e esce con codice 3. Sa anche escludere le proprie uscite dal corpus,
quindi un secondo lancio non si contamina, ma tenere separati corpus e
risultati resta la strada pulita.

Se lo strumento non c'è, o Python non è installato, dirlo all'utente senza
drammi e misurare a mano. È la procedura della sezione «Senza strumento» di
`references/voce-personale.md`, riportata qui perché serve proprio quando il
reference potrebbe mancare. Su un campione di cinquanta frasi consecutive,
prese da un punto qualsiasi del corpus:

1. contare le parole di ogni frase, calcolare la media, e contare quante
   stanno sotto sei parole e quante sopra trentacinque;
2. contare le frasi che finiscono con un punto interrogativo;
3. contare *io, mi, mio* e *tu, ti, tuo* in mille parole;
4. segnare le prime due parole di ogni frase e vedere quali si ripetono;
5. cercare i connettivi *inoltre, tuttavia, pertanto, quindi* e contarli.

Cinque conteggi, mezz'ora di lavoro, e si ha già il grosso del livello
misurato. Con meno di duemila parole i numeri ballano, e il profilo va
dichiarato indicativo: è la stessa soglia che usa lo strumento. Lo strumento è
facoltativo e non è mai un requisito.

### 3. Leggere il corpus per il livello osservato

Questa parte non si delega a nessuno script. Leggere i testi e rispondere a
cinque domande, ognuna con il passo che la sostiene:

1. Quali gesti si ripetono in apertura e in chiusura?
2. Quali parole tornano dove non servirebbero?
3. Dove rompe la regola in modo ricorrente?
4. Che cosa non fa mai?
5. In quale punto si sente di più che c'è qualcuno dentro?

Citare sempre il passo, mai riassumerlo. Un'osservazione senza citazione è
un'impressione, e un'impressione non entra in una scheda.

### 4. Comporre la scheda

Seguire il modello di `references/voce-personale.md` sezione 6, quando il
reference è disponibile. La forma essenziale è comunque questa: la scheda sta
in una pagina, si apre con registro, tipo di voce e affidabilità, e si chiude
con le istruzioni operative: fai questo, non fare questo, nel dubbio.

Le istruzioni sono la parte che serve davvero. «Il tono è caldo» non aiuta
nessuno. «Apri da un problema concreto di chi legge, chiudi con un'immagine,
non spiegare la morale» si può eseguire.

### 5. Distinguere i tic dagli errori

Prima di consegnare, passare le ricorrenze al vaglio della sezione 8 di
`references/voce-personale.md`, quando c'è. I tre criteri sono questi.

Un tratto ricorrente resta nella scheda se è documentato in più testi, se è
coerente con il registro e se non viola una norma della lingua. Se una delle
tre risposte è no, va segnalato come da correggere invece che come voce. I
trattini lunghi, le virgolette inglesi, *qual'è*, *un pò* e *piuttosto che* in
senso disgiuntivo restano errori in qualunque scheda, e vanno detti.

## Limiti da dichiarare all'utente

Vanno scritti nella scheda, non lasciati impliciti.

- Il profilo descrive un corpus in un registro, non una persona.
- Non misura la qualità: un testo scritto male e uno scritto bene possono
  dare lo stesso profilo.
- Non serve a far passare per umano un testo generato. Chi cerca quello ha
  frainteso l'intera skill.
- La varietà lessicale, da sola, non distingue un umano da una macchina: nel
  collaudo dello strumento un testo generato ha ottenuto varietà più alta di
  un corpus umano.
- Una voce cambia negli anni. Un profilo vecchio descrive chi si era.

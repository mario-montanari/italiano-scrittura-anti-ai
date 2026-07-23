---
description: Cattura la voce di chi scrive a partire da un corpus di suoi testi italiani e produce una scheda voce in due livelli, misurato e osservato. Si invoca con /calibra-voce seguito dalla cartella dei testi.
argument-hint: "[cartella dei testi]"
allowed-tools:
  - Read
  - Glob
  - Grep
  - Write
  - Bash(python *)
  - Bash(python3 *)
---

# Calibra voce

Comando della skill `italiano-scrittura-anti-ai`. Il metodo completo, le
decisioni di conteggio e il modello di scheda sono in
`references/voce-personale.md`: leggerlo prima di procedere.

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
condizioni e fermarsi se una non regge.

**Un solo registro.** I testi devono venire dalla stessa voce nello stesso
contesto. Un saggio e una newsletter sono due voci; i testi scritti per un
cliente sono la voce del cliente. Mescolarli produce la media di due persone,
che non somiglia a nessuna delle due. Elencare i file trovati e chiedere
conferma all'utente che appartengano tutti allo stesso registro.

**Almeno duemila parole.** Sotto quella soglia i numeri ballano. Si può
procedere, dichiarando il profilo come indicativo.

**Voce reale o voce desiderata.** Chiedere quale delle due si sta catturando:
come l'autore scrive oggi, o come vorrebbe scrivere. Sono documenti diversi.
La risposta va scritta in cima alla scheda.

### 2. Calcolare il livello misurato

Cercare lo strumento nei percorsi consueti di installazione della skill:

```
~/.claude/skills/italiano-scrittura-anti-ai/scripts/profilo_voce.py
.claude/skills/italiano-scrittura-anti-ai/scripts/profilo_voce.py
```

Se lo si trova, eseguirlo:

```
python <percorso>/profilo_voce.py <cartella> --nome "<nome autore>"
```

Su Windows il comando è `python`, altrove di solito `python3`.

Se lo strumento non c'è, o Python non è installato, dirlo all'utente senza
drammi e passare alle misure a mano descritte in `references/voce-personale.md`
sezione 4: cinque conteggi su cinquanta frasi consecutive danno già il grosso
del profilo. Lo strumento è facoltativo e non è mai un requisito.

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

Seguire il modello di `references/voce-personale.md` sezione 6. La scheda sta
in una pagina, si apre con registro, tipo di voce e affidabilità, e si chiude
con le istruzioni operative: fai questo, non fare questo, nel dubbio.

Le istruzioni sono la parte che serve davvero. «Il tono è caldo» non aiuta
nessuno. «Apri da un problema concreto di chi legge, chiudi con un'immagine,
non spiegare la morale» si può eseguire.

### 5. Distinguere i tic dagli errori

Prima di consegnare, passare le ricorrenze al vaglio della sezione 8 di
`references/voce-personale.md`.

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

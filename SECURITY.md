# Politica di sicurezza

## Versioni supportate

| Versione | Supportata |
| -------- | ---------- |
| ultima   | sì         |

## Segnalare un problema

Questa skill è fatta quasi tutta di testo, e il testo non esegue niente. Il codice sta in tre file, tutti facoltativi e tutti di sola libreria standard di Python, senza accesso alla rete e senza niente da installare:

- `scripts/profilo_voce.py`, lo strumento che calcola il profilo. Scrive due soli file, `scheda-voce.md` e `profilo-voce.json`, nella cartella di uscita indicata da chi lo lancia. Senza l'opzione `--out` quella cartella è la stessa del corpus. Riscrive senza chiedere solo i file che riconosce come propri, cioè quelli che portano la sua firma in testa; se in quella cartella esiste già un file omonimo che non ha scritto lui, si ferma senza toccarlo e invita a scrivere altrove con `--out`.
- `scripts/prova_profilo_voce.py`, che verifica il comportamento dello strumento. Scrive soltanto dentro una cartella temporanea, e la rimuove alla fine.
- `extras/hooks/consenti-solo-profilo-voce.py`, l'hook facoltativo descritto qui sotto. Legge un evento su standard input e scrive una decisione su standard output. Non tocca il disco.

Va dichiarata anche una seconda superficie. I tre comandi in `commands/` portano nel frontmatter una riga `allowed-tools`, che **pre-approva** alcuni strumenti: li lascia agire senza la conferma dell'utente per quel turno.

**Nessuno dei tre pre-approva `Bash`.** Il lancio dello strumento passa quindi dai permessi della sessione: nella modalità predefinita Claude Code chiede la conferma a ogni esecuzione, mentre con una regola che consente `Bash` o in una modalità che approva da sé, come `bypassPermissions`, la conferma può mancare. Un pattern ristretto non basterebbe: in `Bash(python *profilo_voce.py *)` l'asterisco attraversa spazi e separatori di cartella, quindi vincola il nome del file e non il percorso, e un file omonimo messo altrove vi rientrerebbe.

`/calibra-voce` e `/difendi` pre-approvano `Read`, `Glob`, `Grep` e `Write`, **senza restrizione di percorso**, e va detto per intero: servono per leggere i testi che l'utente indica e scrivere la scheda o il documento di difesa, ma la pre-approvazione non sa distinguere quei percorsi da altri, perché cambiano a ogni uso e `allowed-tools` non ha modo di esprimere «solo quelli indicati adesso». Chi vuole pre-approvare il solo lancio dello strumento trova l'hook `PreToolUse` facoltativo in `extras/hooks/`: rifiuta i comandi concatenati e pretende che il percorso finisca con quello dello strumento e che, una volta risolto, stia sotto una cartella dove le skill si installano davvero. Il controllo sulla sola coda del percorso non basta, perché una cartella qualunque, anche di rete, può imitarne gli ultimi nomi.

`/traduci` pre-approva soltanto `Read` e `Glob`, anch'essi senza restrizione di percorso. Il testo da tradurre viene spesso da terzi ed è un dato non fidato, quindi il comando non pre-approva `Write`, e una scrittura chiesta da un'istruzione nascosta nel testo passa dai permessi della sessione. Nella modalità predefinita Claude Code chiede la conferma; con `acceptEdits` o `bypassPermissions`, o con una regola che consente `Write`, la conferma può mancare. Le pre-approvazioni dei comandi caricati nello stesso turno si sommano: un testo incollato che comincia con un altro comando della skill, come `/italiano-scrittura-anti-ai:difendi`, lo carica insieme a `/traduci` con il suo `Write`, e anche Claude può invocare da sé un comando che pre-approva `Write`. Un testo di terzi passato come file evita il primo caso; contro il secondo resta la difesa scritta che segue. Il comando mette il testo in fondo, fra i marcatori `<testo-da-tradurre>` e `</testo-da-tradurre>`, dopo le istruzioni che chiedono di tradurre ogni ordine contenuto nel testo, senza eseguirlo, e di non aprire i file che vi sono nominati. È solo una difesa scritta. Un modello può non rispettarla: la lettura di un file e la ricerca dei percorsi con `Glob` restano possibili senza conferma, e ciò che il modello legge finirebbe nella traduzione o nella nota. Chi traduce testi di terzi rilegge la traduzione e la nota prima di consegnarle o pubblicarle.

Restano possibili problemi da segnalare: un difetto dello strumento che lo porti a leggere o scrivere fuori dalla cartella dichiarata o a consumare risorse fuori misura, un modo per allargare la pre-approvazione oltre quanto dichiarato qui, un comando che l'hook facoltativo lasci passare senza doverlo, un file che espone dati non voluti, un link malevolo, un contenuto che viola la licenza di una fonte.

Se trovi un problema di sicurezza, segnalalo **in privato**, non aprire una issue pubblica.

- Usa il **private vulnerability reporting** di GitHub: scheda **Security** del repository, poi «Report a vulnerability».

Descrivi il problema, i passi per riprodurlo e l'impatto possibile. Ricevi una risposta entro sette giorni. Se il problema è confermato, la correzione arriva appena possibile e ti viene dato credito nel changelog, salvo tua richiesta di restare anonimo.

## Ambito

La politica copre i file e la configurazione di questo repository. I problemi in dipendenze di terze parti vanno segnalati ai rispettivi manutentori.

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

Va dichiarata anche una seconda superficie. I due comandi in `commands/` portano nel frontmatter una riga `allowed-tools`, che **pre-approva** alcuni strumenti: li lascia agire senza la conferma dell'utente per quel turno.

**Nessuno dei due pre-approva `Bash`.** Lo strumento si lancia con la conferma dell'utente, a ogni esecuzione. Un pattern ristretto non basterebbe: in `Bash(python *profilo_voce.py *)` l'asterisco attraversa spazi e separatori di cartella, quindi vincola il nome del file e non il percorso, e un file omonimo messo altrove vi rientrerebbe.

Restano pre-approvati `Read`, `Glob`, `Grep` e `Write`, **senza restrizione di percorso**, e va detto per intero: i due comandi servono per leggere i testi che l'utente indica e scrivere la scheda o il documento di difesa, ma la pre-approvazione non sa distinguere quei percorsi da altri, perché cambiano a ogni uso e `allowed-tools` non ha modo di esprimere «solo quelli indicati adesso». Chi vuole pre-approvare il solo lancio dello strumento trova l'hook `PreToolUse` facoltativo in `extras/hooks/`: rifiuta i comandi concatenati e pretende che il percorso finisca con quello dello strumento e che, una volta risolto, stia sotto una cartella dove le skill si installano davvero. Il controllo sulla sola coda del percorso non basta, perché una cartella qualunque, anche di rete, può imitarne gli ultimi nomi.

Restano possibili problemi da segnalare: un difetto dello strumento che lo porti a leggere o scrivere fuori dalla cartella dichiarata o a consumare risorse fuori misura, un modo per allargare la pre-approvazione oltre quanto dichiarato qui, un comando che l'hook facoltativo lasci passare senza doverlo, un file che espone dati non voluti, un link malevolo, un contenuto che viola la licenza di una fonte.

Se trovi un problema di sicurezza, segnalalo **in privato**, non aprire una issue pubblica.

- Usa il **private vulnerability reporting** di GitHub: scheda **Security** del repository, poi «Report a vulnerability».

Descrivi il problema, i passi per riprodurlo e l'impatto possibile. Ricevi una risposta entro sette giorni. Se il problema è confermato, la correzione arriva appena possibile e ti viene dato credito nel changelog, salvo tua richiesta di restare anonimo.

## Ambito

La politica copre i file e la configurazione di questo repository. I problemi in dipendenze di terze parti vanno segnalati ai rispettivi manutentori.

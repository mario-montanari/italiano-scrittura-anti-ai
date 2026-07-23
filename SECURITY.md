# Politica di sicurezza

## Versioni supportate

| Versione | Supportata |
| -------- | ---------- |
| ultima   | sì         |

## Segnalare un problema

Questa skill è fatta quasi tutta di testo, e il testo non esegue niente. L'unica parte eseguibile è `scripts/profilo_voce.py`, uno strumento facoltativo: usa la sola libreria standard di Python, non accede alla rete, non installa niente, e scrive due soli file, `scheda-voce.md` e `profilo-voce.json`, nella cartella di uscita indicata da chi lo lancia.

Restano possibili problemi da segnalare: un difetto dello script che lo porti a scrivere fuori da quella cartella o a consumare risorse fuori misura, un file che espone dati non voluti, un link malevolo, un contenuto che viola la licenza di una fonte.

Se trovi un problema di sicurezza, segnalalo **in privato**, non aprire una issue pubblica.

- Usa il **private vulnerability reporting** di GitHub: scheda **Security** del repository, poi «Report a vulnerability».

Descrivi il problema, i passi per riprodurlo e l'impatto possibile. Ricevi una risposta entro sette giorni. Se il problema è confermato, la correzione arriva appena possibile e ti viene dato credito nel changelog, salvo tua richiesta di restare anonimo.

## Ambito

La politica copre i file e la configurazione di questo repository. I problemi in dipendenze di terze parti vanno segnalati ai rispettivi manutentori.

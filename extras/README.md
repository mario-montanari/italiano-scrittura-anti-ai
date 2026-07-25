# Extras

Questa cartella contiene **risorse complementari** alla skill `italiano-scrittura-anti-ai`: **template di esempio**, esterni alla skill, che chi la installa può scegliere di usare per estendere la copertura delle regole italiane anche ai contesti dove la skill non si attiva automaticamente.

## Cosa c'è dentro

- **`CLAUDE.md.example`**: template per il file di memoria persistente di Claude Code, da posizionare a livello globale (`~/.claude/CLAUDE.md`) o di progetto.
- **`user-preferences.example.md`**: template per le user preferences di claude.ai, da incollare in Settings, Profile, User Preferences.
- **`commands/calibra-voce.md`**: comando da copiare in `.claude/commands/` per avere `/calibra-voce` in Claude Code. Guida la raccolta del corpus, calcola il profilo con lo script della skill e produce la scheda voce. Istruzioni sotto.
- **`commands/difendi.md`**: comando da copiare in `.claude/commands/` per avere `/difendi`. Prepara la risposta a un rilevatore automatico che ha segnalato come generato un testo scritto da una persona. Istruzioni sotto.
- **`hooks/consenti-solo-profilo-voce.py`**: hook `PreToolUse` facoltativo, per chi calibra spesso e vuole togliere la conferma al solo lancio dello strumento. Istruzioni sotto.

## Il comando `/calibra-voce`

I comandi personalizzati di Claude Code sono ormai unificati con le skill: un file in `.claude/commands/nome.md` e una skill in `.claude/skills/nome/SKILL.md` creano entrambi `/nome`. Una repo che distribuisce una skill singola, come questa, mette quindi a disposizione il proprio comando come file da copiare.

Copiare `extras/commands/calibra-voce.md` in una di queste posizioni:

- `~/.claude/commands/calibra-voce.md` per averlo in ogni progetto;
- `.claude/commands/calibra-voce.md` nella radice di un progetto, per averlo solo lì.

Poi si invoca con `/calibra-voce cartella-dei-miei-testi`. Il comando cerca lo script `scripts/profilo_voce.py` dentro la skill installata; se non lo trova, o se Python non è presente, ricade sulle misure a mano, che il comando porta scritte al proprio interno proprio perché funzionino anche quando è stato copiato da solo, senza la skill. Il risultato non cambia di natura, cambia la precisione.

## Il comando `/difendi`

Stessa installazione. Copiare `extras/commands/difendi.md` in `~/.claude/commands/difendi.md` per averlo ovunque, oppure in `.claude/commands/difendi.md` dentro un progetto.

Si invoca con `/difendi file-del-testo-contestato.md`. Serve a chi ha scritto un testo e se lo vede contestare da un rilevatore automatico di AI: il comando raccoglie i fatti dell'accusa, chiede i materiali di lavoro dell'autore e compone il documento da consegnare a chi ha sollevato il caso. Il metodo completo e le evidenze pubblicate sono in `references/scudo-falsi-positivi.md`.

Due cose che il comando non fa, per scelta. Non esegue alcuno strumento sul testo contestato per stabilirne la natura, perché un punteggio prodotto lì varrebbe quanto quello che si sta contestando. Non indica modifiche per abbassare il punteggio di un rilevatore: una riscrittura successiva all'accusa distrugge la prova di processo e somiglia a una manomissione.

## L'hook facoltativo per lo strumento

Serve a una cosa sola, e conviene dire subito a chi non serve: se calibri la
voce una volta ogni tanto, lascia perdere e conferma il lancio quando Claude
Code te lo chiede.

Il comando `/calibra-voce` non pre-approva `Bash`. Ogni esecuzione dello
strumento passa quindi dalla conferma dell'utente, che è la scelta più sicura:
il comando legge per intero testi che possono venire da un cliente, e una
pre-approvazione larga eseguirebbe senza chiedere anche un comando suggerito
da quei testi.

Restringere il pattern non risolverebbe. In `Bash(python *profilo_voce.py *)`
l'asterisco attraversa spazi e separatori di cartella: vincola il nome del
file, non il percorso, e un file omonimo messo altrove vi rientrerebbe.

L'hook fa il lavoro che `allowed-tools` non sa fare. Guarda il comando prima
che parta e risponde `allow` solo quando ricorrono tutte queste condizioni: il
comando comincia con un interprete Python chiamato per nome (`python`,
`python3`, `python3.12`, con o senza `.exe`), il percorso dello script finisce
con `italiano-scrittura-anti-ai/scripts/profilo_voce.py`, quel percorso una
volta risolto sta sotto una cartella dove le skill si installano davvero
(`~/.claude/skills/` oppure il `.claude/skills/` del progetto in corso), non
compare alcun metacarattere di shell e le opzioni sono solo quelle dello
strumento. In ogni altro caso non decide niente e lascia che il permesso lo
chieda Claude Code, come farebbe senza hook. Non nega mai: un hook che nega
spegnerebbe comandi legittimi che con questa skill non c'entrano.

Le condizioni sono nate da due giri di audit, e ognuna chiude un varco vero.
La sola coda di tre nomi si imita: bastava una cartella qualunque, o anche una
condivisione di rete, che finisse con quei tre nomi per farsi approvare senza
conferma. E guardare il solo secondo argomento lasciava aperto il primo, che è
quello che viene eseguito: un file chiamato `python` messo in una cartella
qualsiasi passava, e con lui qualunque cosa contenesse. Chi lancia l'interprete
di un ambiente virtuale scrivendone il percorso completo resta quindi alla
conferma manuale.

Due limiti dichiarati, perché un hook di sicurezza che nasconde i propri buchi
vale meno di nessun hook. Il primo: fra le radici fidate c'è il
`.claude/skills/` del progetto aperto, quindi un repository ostile clonato e
aperto come progetto potrebbe portarsi dietro un proprio `profilo_voce.py` in
quella posizione. Per questo l'hook si installa **per progetto**, come qui
sotto, e non una volta per tutte a livello personale. Il secondo: l'hook decide
sul comando, non sul contenuto del file; verificare che quel file sia davvero
lo strumento della skill, e non una copia manomessa, resta fuori dalla sua
portata.

Quando la skill sta altrove, l'hook tace e la conferma torna all'utente, che
è il verso giusto in cui sbagliare.

**Installazione.** Copiare il file in `.claude/hooks/` dentro il progetto, poi
aggiungere in `.claude/settings.json`:

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "command",
            "command": "python ${CLAUDE_PROJECT_DIR}/.claude/hooks/consenti-solo-profilo-voce.py"
          }
        ]
      }
    ]
  }
}
```

**Verifica prima di fidarsi.** L'hook porta con sé la propria prova e si
controlla senza installarlo:

```bash
python extras/hooks/consenti-solo-profilo-voce.py --prova
```

Elenca ventidue casi con l'esito atteso, fra cui il comando concatenato, lo
script omonimo messo altrove, la cartella che imita gli ultimi tre nomi, il
percorso di rete, l'eseguibile chiamato `python` messo in una cartella
qualunque e le opzioni non previste. Leggerli è il modo più rapido per capire
che cosa l'hook lascia passare.

## Filosofia: tre livelli di copertura

La skill `italiano-scrittura-anti-ai` da sola copre il caso d'uso più importante: **produrre testo italiano destinato a uso pubblico, professionale, editoriale o di marketing**. La skill si attiva quando rileva una richiesta di questo tipo e fornisce a Claude tutto l'arsenale di regole, pattern, metodologie.

Però ci sono casi in cui la skill **non si attiva** ma vorresti comunque le regole base sempre rispettate:

- chat informali brevi (esempio: «riassumimi questa cosa», «aiutami a capire X»)
- commenti tecnici dentro codice
- risposte conversazionali rapide
- domande su altri argomenti dove però Claude risponde in italiano

Per coprire anche questi casi, esistono due meccanismi complementari alla skill:

1. **CLAUDE.md globale** (per chi usa Claude Code): vale per ogni sessione, su ogni progetto.
2. **User preferences** (per chi usa claude.ai web o app): valgono per ogni conversazione.

I tre livelli insieme danno copertura completa:

| Livello | Quando interviene | Dove vive |
|---|---|---|
| Skill | Testi importanti | Cartella `.claude/skills/` o `~/.claude/skills/` |
| CLAUDE.md | Sempre, su Claude Code | `~/.claude/CLAUDE.md` (globale) o radice progetto |
| User preferences | Sempre, su claude.ai | Settings → Profile → User Preferences |

Non serve usarli tutti e tre: dipende dalle interfacce che usi e da quanto rigorose vuoi le tue regole base.

## Quale combinazione scegliere

- **Uso solo claude.ai web**: skill + user preferences
- **Uso solo Claude Code**: skill + CLAUDE.md
- **Uso entrambi**: skill + CLAUDE.md + user preferences
- **Voglio solo provare la skill**: solo skill, gli altri due sono opzionali

## Note importanti

- I template sono **esempi generici**, pensati per chiunque scarichi la skill. Se vuoi aggiungere informazioni personali (professione, contesto di lavoro, preferenze stilistiche), inseriscile **prima** delle regole linguistiche, non al posto.
- Le user preferences hanno un limite pratico di lunghezza intorno ai 2-3 KB. Il template è dimensionato per stare dentro il limite e lasciare spazio a tue aggiunte.
- Il CLAUDE.md non ha limiti tecnici stretti, ma più è lungo più appesantisce ogni sessione di Claude Code. Mantieni l'essenziale.
- Per personalizzazioni più sofisticate (cambio di stile, aggiunta di pattern specifici al tuo settore), considera di **creare una skill derivata** invece di sovraccaricare CLAUDE.md o preferences.

## Domande frequenti

**Posso usare CLAUDE.md o user preferences senza installare la skill?**

Sì. I template sono autonomi: contengono le 20 regole essenziali estratte dalla skill, formulate come istruzioni dirette. Funzionano anche senza la skill. Il vantaggio della skill è che fornisce in più tutto il contesto profondo (grammatica avanzata, catalogo lessicale completo, metodologie operative come l'audit pass in due passaggi, voice calibration, sei mosse di umanizzazione, eccetera).

**Cosa succede se le tre fonti dicono cose diverse?**

In generale: la skill quando si attiva ha la parola finale (è il livello più informato), seguita da CLAUDE.md di progetto, poi CLAUDE.md globale, poi user preferences. Le tre fonti di questi template sono allineate fra loro, quindi non dovrebbero esserci conflitti.

**Posso modificare i template?**

Sì, sono pensati proprio per questo. La licenza MIT della skill copre anche i template: sono tuoi, falli evolvere come ti serve.

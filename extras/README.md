# Extras

Questa cartella contiene **risorse complementari** alla skill `italiano-scrittura-anti-ai`. Non sono parte della skill stessa: sono **template di esempio** che chi installa la skill può scegliere di usare per estendere la copertura delle regole italiane anche ai contesti dove la skill non si attiva automaticamente.

## Cosa c'è dentro

- **`CLAUDE.md.example`** — template per il file di memoria persistente di Claude Code, da posizionare a livello globale (`~/.claude/CLAUDE.md`) o di progetto.
- **`user-preferences.example.md`** — template per le user preferences di claude.ai, da incollare in Settings → Profile → User Preferences.

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

Assolutamente sì. Sono pensati per essere personalizzati. La licenza MIT della skill copre anche i template: sono tuoi, falli evolvere come ti serve.

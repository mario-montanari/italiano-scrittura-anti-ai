# italiano-scrittura-anti-ai

![License: MIT](https://img.shields.io/badge/license-MIT-green)
![Version: 1.0.0](https://img.shields.io/badge/version-1.0.0-blue)
![Language: Italian](https://img.shields.io/badge/language-italiano-red)

Skill Claude per scrivere in italiano corretto evitando i pattern tipici della prosa generata da modelli linguistici.

## Il problema

I modelli linguistici (GPT, Claude, Gemini, altri) scrivono in italiano con una firma riconoscibile. Non è solo una questione estetica: è un problema pratico. Un lettore italiano colto percepisce immediatamente i tic algoritmici, e chi pubblica testi così rischia di perdere credibilità professionale, ranking SEO, rapporto di fiducia con clienti e lettori.

La firma include pattern come l'abuso dell'em-dash (—), i calchi dall'inglese («navigare le complessità», «elevare il tuo business»), la gonfiatura retorica («si configura come un punto di svolta»), i meta-annunci («è importante sottolineare che», «andiamo a vedere»), la sinonimia forzata (Calvino chiamato in sette modi diversi nello stesso paragrafo), i contrasti fittizi («non solo X ma anche Y»), gli artefatti da chatbot («Certo! Spero ti sia utile!»). Ciascuno preso da solo è svista; la loro compresenza densa produce il «profumo dell'AI».

## Cosa fa questa skill

Fornisce a Claude tre cose:

1. **Le regole di grammatica italiana normativa** che i modelli sbagliano con più frequenza (articoli davanti a consonanti speciali, accenti acuti e gravi, congiuntivo, trattino breve/medio/lungo, virgolette caporali)
2. **Il catalogo operativo del lessico AI italiano** da sopprimere, con alternative concrete
3. **Le metodologie pratiche** di lavoro: soppressione attiva durante la stesura, audit pass in due passaggi, voice calibration per la voce del cliente, sei mosse di umanizzazione tratte dalla tradizione italiana (Calvino, Eco, Levi, Carrada, Testa)

La base scientifica include gli studi dell'ItaliaNLP Lab del CNR-ILC di Pisa sulla stilometria italiana, le pubblicazioni CLiC-it 2024, lo skill open source Humanizer del WikiProject AI Cleanup.

## A chi serve

- A chi **scrive professionalmente in italiano** (copywriter, giornalisti, saggisti, autori, studenti, ricercatori) e usa Claude come assistente
- A chi **pubblica testi online** (blog, newsletter, social, landing page) e vuole evitare la firma AI
- A chi **revisiona testi italiani** prodotti da altri modelli linguistici
- A chi **traduce in italiano** e vuole evitare i calchi dall'inglese
- A chi **lavora per clienti con voce autoriale definita** e deve allinearsi al loro stile

Non serve per la scrittura in inglese o altre lingue. Non serve per testi puramente tecnici senza esigenze di registro (codice, dati, configurazioni).

## Installazione

### In Claude Code (progetto specifico)

Copiare la cartella `italiano-scrittura-anti-ai/` dentro la cartella `.claude/skills/` del proprio progetto:

```
progetto/
├── .claude/
│   └── skills/
│       └── italiano-scrittura-anti-ai/
│           ├── SKILL.md
│           ├── references/
│           └── ...
└── ...
```

### In Claude Code (globale, tutti i progetti)

Copiare la cartella in `~/.claude/skills/` (su Linux e macOS) o nel percorso equivalente Windows.

### Via claude.ai (app desktop o web)

Le skill personali si caricano dalle Impostazioni → Capabilities → Skills, seguendo le istruzioni ufficiali Anthropic.

### Via API

Il meccanismo di caricamento delle skill via API è documentato nella documentazione Anthropic ufficiale.

## Come si attiva

La skill si attiva automaticamente quando l'utente chiede a Claude di:

- scrivere, redigere, generare testi italiani per uso pubblico o professionale
- tradurre in italiano testi prodotti in altre lingue
- revisionare, correggere, migliorare un testo italiano
- «umanizzare» un testo italiano prodotto da AI
- correggere grammatica e stile italiani

Non si attiva per chat informali brevi né per contesti non testuali.

## Esempio prima e dopo

**Versione AI non revisionata:**

> «Nel panorama editoriale in continua evoluzione, è fondamentale sottolineare come l'intelligenza artificiale stia rivoluzionando il modo in cui scriviamo. Diversi studi dimostrano che l'AI offre numerosi vantaggi, tra cui la possibilità di ottimizzare i processi creativi e sbloccare il potenziale degli autori. Non si tratta solo di uno strumento, ma di un vero e proprio punto di svolta. In conclusione, l'AI rappresenta una risorsa imprescindibile per chiunque voglia approfondire il proprio percorso editoriale.»

Quattro frasi, quindici pattern AI, zero informazioni verificabili.

**Versione umanizzata:**

> «L'intelligenza artificiale è entrata nei processi editoriali italiani nel 2023, due anni dopo il boom anglofono. Gli editori che la usano oggi la impiegano soprattutto per tre cose: editing di prima passata, traduzioni grezze da rifinire, generazione di varianti di copy per A/B test. Non ha sostituito nessuno, ma ha cambiato il mestiere di chi sta davanti al testo. Continuo a pensare a quello che mi disse un editor cinque mesi fa: «Adesso lavoro meno con Word, lavoro più con domande».»

Data verificabile, tre casi d'uso concreti, posizione presa, prima persona, citazione datata con virgolette caporali. Stesso argomento, testo che respira.

## Struttura della skill

```
italiano-scrittura-anti-ai/
├── SKILL.md                           # File indice con frontmatter YAML
├── README.md                          # Questo file
├── LICENSE                            # Licenza MIT
├── .gitignore                         # File ignorati da git
├── references/                        # Reference caricati on-demand da Claude
│   ├── grammatica-italiana.md         # Articoli, accenti, apostrofi, punteggiatura, congiuntivo
│   ├── lessico-da-evitare.md          # Aggettivi, verbi, sostantivi, calchi, falsi amici, anglicismi
│   ├── pattern-strutturali.md         # 20 pattern AI con esempi e correzioni
│   ├── metodologie-operative.md       # Workflow, audit pass, voice calibration, sei mosse di umanizzazione
│   ├── personalita-e-anima.md         # Sei sintomi, sei tecniche, esempio di trasformazione
│   ├── checklist-finale.md            # Checklist pre-consegna, red flag, tabella sinottica
│   └── registri-e-contesti.md         # Sei registri, norme editoriali, SEO, E-E-A-T
└── extras/                            # Risorse complementari opzionali (vedi sezione successiva)
    ├── README.md                      # Spiega la filosofia dei tre livelli di copertura
    ├── CLAUDE.md.example              # Template per Claude Code
    └── user-preferences.example.md    # Template per claude.ai
```

## Risorse complementari (cartella `extras/`)

Oltre ai file della skill, la repo include una cartella `extras/` con due **template opzionali** che estendono le regole italiane anche ai contesti dove la skill non si attiva (chat informali, commenti tecnici, risposte conversazionali).

- **`extras/CLAUDE.md.example`** — file di memoria persistente per Claude Code, da posizionare in `~/.claude/CLAUDE.md` (globale) o nella radice di un progetto specifico.
- **`extras/user-preferences.example.md`** — testo da incollare nelle user preferences di claude.ai (Settings → Profile → User Preferences).

I template contengono le 20 regole linguistiche essenziali estratte dalla skill, formulate come istruzioni dirette sempre attive. La filosofia è quella dei **tre livelli di copertura**: la skill come bisturi (interviene sui testi importanti), CLAUDE.md e user preferences come igiene quotidiana (valgono sempre). Vedi `extras/README.md` per i dettagli e per le istruzioni di installazione.

## Crediti e fonti

La skill consolida e organizza materiale di documenti sorgente redatti dall'autore, che a loro volta si basano su fonti accademiche, editoriali e tecniche pubblicamente disponibili.

**Fonti grammaticali e linguistiche:**

- Accademia della Crusca (consulenze linguistiche di Patota, Della Valle, Setti, Cainelli)
- Treccani, *Enciclopedia dell'Italiano*, *Vocabolario*
- Luca Serianni, *Grammatica italiana*
- *Vademecum sull'accento* del 2002, DOP, Gabrielli, Canepari

**Fonti stilistiche e di scrittura professionale:**

- Italo Calvino, *Lezioni americane* (Garzanti 1988)
- Umberto Eco, *Come si fa una tesi di laurea* (Bompiani 1977), *Dire quasi la stessa cosa* (Bompiani 2003)
- Primo Levi, *L'altrui mestiere* (Einaudi 1985)
- Luisa Carrada, *Il mestiere di scrivere*, collana Zanichelli
- Annamaria Testa, *Farsi capire* (Rizzoli 2000)

**Fonti tecniche e stilometriche:**

- ItaliaNLP Lab del CNR-ILC di Pisa (Dell'Orletta, Montemagni, Venturi, Brunato): pipeline AnIta, modello READ-IT, studi sull'indice Gulpease
- CLiC-it 2024 (atti CEUR Vol. 3878, ACL Anthology): contributi di Esuli, Falchi, Puccetti, Ciaccio, Miaschi
- Sarti, Bisazza, Occhipinti, Nissim, HED-IT, ACL 2024 Findings
- Edward Tian, GPTZero (perplessità e burstiness)

**Fonti per gli anglicismi:**

- Antonio Zoppetti, *AAA Alternative Agli Anglicismi*
- Claudio Marazzini per l'Accademia della Crusca

**Fonte fondamentale per i pattern Humanizer:**

- **WikiProject AI Cleanup**, pagina *Signs of AI writing* di Wikipedia
- **Skill Humanizer open source**, basato sul WikiProject AI Cleanup

A tutti questi autori, istituzioni e progetti va il riconoscimento per aver fornito la base su cui questa skill è costruita.

## Licenza

MIT License. Vedere il file `LICENSE` per il testo completo.

Significa: puoi usare, modificare, integrare questa skill in qualsiasi progetto, anche commerciale, mantenendo l'attribuzione. Non ci sono restrizioni particolari. La licenza è scelta per massimizzare la riutilizzabilità da parte della comunità italiana.

## Contributi

I contributi sono benvenuti.

- **Segnalazioni:** aprire un issue su GitHub con descrizione chiara del problema o del suggerimento
- **Pull request:** per modifiche ai reference, allegare la motivazione e, se possibile, una fonte o un esempio concreto
- **Nuovi pattern:** se trovate un pattern AI italiano che la skill non copre, proponetelo con parole spia, esempio negativo, spiegazione del problema, correzione

Le discussioni stilistiche sono ammesse e incoraggiate, purché ancorate a fonti (Crusca, Treccani, Serianni, manuali editoriali) o a corpora verificabili.

## Autore

**Mario Montanari**

Sito personale: [mariomontanari.it](https://mariomontanari.it)

Il progetto nasce dall'esperienza di scrittura professionale e di osservazione sistematica dell'italiano AI. È pensato come contributo alla comunità italiana di utenti Claude e LLM in generale.

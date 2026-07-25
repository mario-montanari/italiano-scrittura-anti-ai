# italiano-scrittura-anti-ai

![License: MIT](https://img.shields.io/badge/license-MIT-green)
![Version: 1.3.0](https://img.shields.io/badge/version-1.3.0-blue)
![Language: Italian](https://img.shields.io/badge/language-italiano-red)

Skill Claude per scrivere in italiano corretto evitando i pattern tipici della prosa generata da modelli linguistici.

## Il problema

I modelli linguistici (GPT, Claude, Gemini, altri) scrivono in italiano con una firma riconoscibile. Un lettore italiano colto percepisce immediatamente i tic algoritmici, e chi pubblica testi così rischia di perdere credibilità professionale, ranking SEO, rapporto di fiducia con clienti e lettori.

La firma include pattern come l'abuso dell'em-dash (—), i calchi dall'inglese («navigare le complessità», «elevare il tuo business»), la gonfiatura retorica («si configura come un punto di svolta»), i meta-annunci («è importante sottolineare che», «andiamo a vedere»), la sinonimia forzata (Calvino chiamato in sette modi diversi nello stesso paragrafo), i contrasti fittizi («non solo X ma anche Y»), gli artefatti da chatbot («Certo! Spero ti sia utile!»). Ciascuno preso da solo è svista; la loro compresenza densa produce il «profumo dell'AI».

## Cosa fa questa skill

Fornisce a Claude cinque cose:

1. **Le regole di grammatica italiana normativa** che i modelli sbagliano con più frequenza (articoli davanti a consonanti speciali, accenti acuti e gravi, congiuntivo, trattino breve/medio/lungo, virgolette caporali)
2. **Il catalogo operativo del lessico AI italiano** da sopprimere, con alternative concrete
3. **Le metodologie pratiche** di lavoro: soppressione attiva durante la stesura, audit pass in due passaggi, voice calibration per la voce del cliente, sei mosse di umanizzazione tratte dalla tradizione italiana (Calvino, Eco, Levi, Camilleri), ampliate in una galleria di sette maestri da cui rubare la mossa-firma
4. **I segnali misurabili e i canali del lettore**: i marcatori anti-AI con base peer-reviewed (varietà lessicale, pronomi personali, emozioni, interiorità, sottotesto, template sintattici), più affidabili delle liste di parole; il riconoscimento del leak del registro conversazionale; i quattro canali attraverso cui un lettore gode di un testo, usati come griglia diagnostica
5. **La difesa contro le accuse dei rilevatori automatici**: che cosa misura davvero un rilevatore, quanto sbaglia secondo le misure pubblicate, il vuoto di dati sull'italiano, e come si costruisce la risposta quando un testo scritto da una persona viene segnalato come generato. Serve a difendere un testo umano accusato ingiustamente, non a far passare per umano un testo generato

La base scientifica include gli studi dell'ItaliaNLP Lab del CNR-ILC di Pisa sulla stilometria italiana, le pubblicazioni CLiC-it 2024, la skill open source Humanizer del WikiProject AI Cleanup.

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

```text
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
- rispondere a un rilevatore automatico che ha segnalato come generato un testo scritto da una persona
- catturare o calibrare la voce di un autore a partire da un corpus di suoi testi

Non si attiva per chat informali brevi né per contesti non testuali.

## Esempio prima e dopo

**Versione AI non revisionata:**

> «Nel panorama editoriale in continua evoluzione, è fondamentale sottolineare come l'intelligenza artificiale stia rivoluzionando il modo in cui scriviamo. Diversi studi dimostrano che l'AI offre numerosi vantaggi, tra cui la possibilità di ottimizzare i processi creativi e sbloccare il potenziale degli autori. Non si tratta solo di uno strumento, ma di un vero e proprio punto di svolta. In conclusione, l'AI rappresenta una risorsa imprescindibile per chiunque voglia approfondire il proprio percorso editoriale.»

Quattro frasi, quindici pattern AI, zero informazioni verificabili.

**Versione umanizzata:**

> «L'intelligenza artificiale è entrata nei processi editoriali italiani nel 2023, due anni dopo il boom anglofono. Gli editori che la usano oggi la impiegano soprattutto per tre cose: editing di prima passata, traduzioni grezze da rifinire, generazione di varianti di copy per A/B test. Non ha sostituito nessuno, ma ha cambiato il mestiere di chi sta davanti al testo. Continuo a pensare a quello che mi disse un editor cinque mesi fa: «Adesso lavoro meno con Word, lavoro più con domande».»

Data verificabile, tre casi d'uso concreti, posizione presa, prima persona, citazione datata con virgolette caporali. Stesso argomento, testo che respira.

## Struttura della skill

```text
italiano-scrittura-anti-ai/
├── SKILL.md                           # File indice con frontmatter YAML
├── README.md                          # Questo file
├── CHANGELOG.md                       # Storia delle versioni, formato Keep a Changelog
├── CITATION.cff                       # Metadati per citare la skill
├── CONTRIBUTING.md                    # Le tre vie del contributo, formato di un pattern
├── CODE_OF_CONDUCT.md                 # Contributor Covenant 3.0 in italiano
├── SECURITY.md                        # Superficie eseguibile e segnalazione privata
├── LICENSE                            # Licenza MIT
├── .gitignore                         # File ignorati da git
├── .github/                           # Automazioni e modelli della repo
│   ├── workflows/codeql.yml           # Analisi statica del solo script Python
│   ├── workflows/prove.yml            # Suite dello strumento e autoprova dell'hook a ogni push
│   ├── dependabot.yml                 # Aggiornamento settimanale delle action
│   ├── ISSUE_TEMPLATE/                # Segnalazione e proposta di un pattern
│   └── PULL_REQUEST_TEMPLATE.md       # Checklist con fonti citate
├── references/                        # Reference caricati on-demand da Claude
│   ├── grammatica-italiana.md         # Articoli, accenti, apostrofi, punteggiatura, congiuntivo
│   ├── lessico-da-evitare.md          # Aggettivi, verbi, sostantivi, calchi, falsi amici, anglicismi
│   ├── pattern-strutturali.md         # 20 pattern AI con esempi e correzioni
│   ├── metodologie-operative.md       # Workflow, audit pass, voice calibration, sei mosse di umanizzazione
│   ├── voce-personale.md              # Profilo di voce in due livelli, scheda compilabile, confine con le norme
│   ├── maestri-della-deviazione.md    # Galleria di 7 autori italiani, la mossa-firma di ognuno da rubare
│   ├── personalita-e-anima.md         # Sei sintomi, sei tecniche, esempio di trasformazione, anti over-humanizing
│   ├── checklist-finale.md            # Checklist pre-consegna, red flag, tabella sinottica
│   ├── registri-e-contesti.md         # Sei registri, norme editoriali, SEO, E-E-A-T
│   ├── segnali-misurabili.md          # Segnali anti-AI con base peer-reviewed (MATTR, pronomi, sottotesto)
│   ├── leak-conversazionale.md        # Il testo che parla come una chat: negazioni, suspense, riassunti frattali
│   ├── canali-lettore-saggistica.md   # I quattro canali del lettore come griglia diagnostica
│   └── scudo-falsi-positivi.md        # Difesa di un testo umano segnalato da un rilevatore automatico
├── scripts/                           # Strumenti facoltativi, sola libreria standard Python
│   ├── profilo_voce.py                # Calcola il profilo quantitativo di una voce da un corpus di testi
│   └── prova_profilo_voce.py          # Prove automatiche dello strumento, una per ogni difetto corretto
└── extras/                            # Risorse complementari opzionali (vedi sezione successiva)
    ├── README.md                      # Spiega la filosofia dei tre livelli di copertura
    ├── CLAUDE.md.example              # Template per Claude Code
    ├── user-preferences.example.md    # Template per claude.ai
    ├── commands/
    │   ├── calibra-voce.md            # Comando /calibra-voce da copiare in .claude/commands/
    │   └── difendi.md                 # Comando /difendi da copiare in .claude/commands/
    └── hooks/
        └── consenti-solo-profilo-voce.py  # Hook PreToolUse facoltativo, pre-approva il solo lancio dello strumento
```

## Risorse complementari (cartella `extras/`)

Oltre ai file della skill, la repo include una cartella `extras/` con due **template opzionali** che estendono le regole italiane anche ai contesti dove la skill non si attiva (chat informali, commenti tecnici, risposte conversazionali), più i **comandi** di Claude Code.

- **`extras/CLAUDE.md.example`**: file di memoria persistente per Claude Code, da posizionare in `~/.claude/CLAUDE.md` (globale) o nella radice di un progetto specifico.
- **`extras/user-preferences.example.md`**: testo da incollare nelle user preferences di claude.ai (Settings → Profile → User Preferences).
- **`extras/commands/calibra-voce.md`** e **`extras/commands/difendi.md`**: i due comandi della skill, da copiare in `.claude/commands/` per avere `/calibra-voce` e `/difendi`. Il primo costruisce il profilo di una voce a partire da un corpus di testi, il secondo prepara la risposta a un rilevatore che ha segnalato un testo come generato.

I template contengono le 20 regole linguistiche essenziali estratte dalla skill, formulate come istruzioni dirette sempre attive. La filosofia è quella dei **tre livelli di copertura**: la skill come bisturi (interviene sui testi importanti), CLAUDE.md e user preferences come igiene quotidiana (valgono sempre). Vedi `extras/README.md` per i dettagli e per le istruzioni di installazione.

## Crediti e fonti

La skill consolida e organizza materiale di documenti sorgente redatti dall'autore, che a loro volta si basano su fonti accademiche, editoriali e tecniche pubblicamente disponibili.

**Fonti grammaticali e linguistiche:**

- Accademia della Crusca (consulenze linguistiche di Patota, Della Valle, Setti, Cainelli)
- Treccani, *Enciclopedia dell'Italiano*, *Vocabolario*
- Luca Serianni, *Grammatica italiana*
- *Vademecum sull'accento* del 2002, DOP, Gabrielli, Canepari

**Fonti stilistiche e di scrittura professionale:**

- Italo Calvino, *Lezioni americane* (Garzanti 1988), *Le città invisibili* (Einaudi 1972)
- Umberto Eco, *Come si fa una tesi di laurea* (Bompiani 1977), *Dire quasi la stessa cosa* (Bompiani 2003)
- Primo Levi, *L'altrui mestiere* (Einaudi 1985)
- Natalia Ginzburg, *Le piccole virtù* (Einaudi 1962)
- Luisa Carrada, *Il mestiere di scrivere*, collana Zanichelli
- Annamaria Testa, *Farsi capire* (Rizzoli 2000)

**Fonti tecniche e stilometriche:**

- ItaliaNLP Lab del CNR-ILC di Pisa (Dell'Orletta, Montemagni, Venturi, Brunato): pipeline AnIta, modello READ-IT, studi sull'indice Gulpease
- CLiC-it 2024 (atti CEUR Vol. 3878, ACL Anthology): contributi di Esuli, Falchi, Puccetti, Ciaccio, Miaschi
- Sarti, Bisazza, Occhipinti, Nissim, HED-IT, ACL 2024 Findings
- Edward Tian, GPTZero (perplessità e burstiness)

**Fonti sui falsi positivi dei rilevatori** (per esteso, con DOI e citazioni testuali, in `references/scudo-falsi-positivi.md`):

- Liang, Yuksekgonul, Mao, Wu, Zou (2023), *GPT detectors are biased against non-native English writers*, Patterns 4(7)
- Weber-Wulff e colleghi (2023), *Testing of detection tools for AI-generated text*, International Journal for Educational Integrity 19
- Sadasivan, Kumar, Balasubramanian, Wang, Feizi, *Can AI-Generated Text be Reliably Detected?*, TMLR
- Jabarian, Imas (2025), *Artificial Writing and Automated Detection*, NBER Working Paper 34223
- Macko, Kopal (2025), benchmark CEAID, arXiv:2509.26051; Macko e colleghi (2023), benchmark MULTITuDE, EMNLP 2023
- OpenAI, nota sul ritiro dell'AI Text Classifier (2023); Turnitin, dichiarazioni di Annie Chechitelli (2023); Vanderbilt University, disattivazione del rilevatore (2023)
- ICMJE, raccomandazioni sull'uso di strumenti di AI da parte degli autori

**Fonti per gli anglicismi:**

- Antonio Zoppetti, *AAA Alternative Agli Anglicismi*
- Claudio Marazzini per l'Accademia della Crusca

**Fonte fondamentale per i pattern Humanizer:**

- **WikiProject AI Cleanup**, pagina *Signs of AI writing* di Wikipedia
- **Skill Humanizer open source**, basato sul WikiProject AI Cleanup

**Fonte dell'upgrade 1.1.0 (segnali misurabili, leak conversazionale, canali del lettore):**

- **`creative-writing-skills` di haowjy**, licenza Apache 2.0. I tre nuovi reference adattano in italiano concetti tratti da questo repository (antipatterns, leak del registro conversazionale, canali di ricompensa del lettore). L'attribuzione è riportata anche in fondo a ciascuno dei tre file.

**Fonti scientifiche aggiunte con l'upgrade 1.1.0:**

- Kobak, González-Márquez, Horvát, Lause (2024), *Delving into LLM-assisted writing in biomedical publications through excess vocabulary*, arXiv:2406.07016: vocabolario in eccesso e parole di stile come marcatori d'uso degli LLM
- Shaib, Elazar, Li, Wallace (2024), *Detection and Measurement of Syntactic Templates in Generated Text*, EMNLP 2024, arXiv:2407.00211: template sintattici ripetuti
- Covington, McFall (2010), *Cutting the Gordian Knot: The Moving-Average Type-Token Ratio (MATTR)*, Journal of Quantitative Linguistics: metrica della varietà lessicale robusta rispetto alla lunghezza
- van Laer, de Ruyter, Visconti, Wetzels (2014), *The Extended Transportation-Imagery Model*, Journal of Consumer Research 40(5), doi:10.1086/673383: il trasporto narrativo come costrutto misurabile
- Thissen, Menninghaus, Schlotz (2018), *Measuring optimal reading experiences: The reading flow short scale*, Frontiers in Psychology, doi:10.3389/fpsyg.2018.02542: il flusso di lettura
- Hemingway, *Death in the Afternoon* (1932), capitolo 16: la teoria dell'iceberg

A tutti questi autori, istituzioni e progetti va il riconoscimento per aver fornito la base su cui questa skill è costruita.

## Licenza

MIT License. Vedere il file `LICENSE` per il testo completo.

Significa: puoi usare, modificare, integrare questa skill in qualsiasi progetto, anche commerciale, mantenendo l'attribuzione. Non ci sono restrizioni particolari. La licenza è scelta per massimizzare la riutilizzabilità da parte della comunità italiana.

L'upgrade 1.1.0 incorpora concetti adattati dal repository `creative-writing-skills` di haowjy, distribuito con licenza Apache 2.0. Le due licenze sono compatibili: si può integrare materiale Apache 2.0 in un progetto MIT mantenendo l'attribuzione, che è riportata sia in fondo ai tre nuovi reference sia nella sezione crediti. La licenza della skill resta MIT.

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

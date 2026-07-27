# italiano-scrittura-anti-ai

![Suite per la lingua italiana e sistema avanzato anti AI: una macchina da scrivere meccanica con i tasti illuminati al neon, un foglio manoscritto nel rullo e pagine di scrittura a mano sullo sfondo.](assets/banner.png)

[![Licenza MIT](https://img.shields.io/badge/licenza-MIT-green?style=for-the-badge)](LICENSE)
[![Versione 1.4.0](https://img.shields.io/badge/versione-1.4.0-blue?style=for-the-badge)](CHANGELOG.md)
[![Prove](https://img.shields.io/github/actions/workflow/status/mario-montanari/italiano-scrittura-anti-ai/prove.yml?style=for-the-badge&label=prove)](.github/workflows/prove.yml)
[![Lingua italiano](https://img.shields.io/badge/lingua-italiano-red?style=for-the-badge)](SKILL.md)
[![Stelle](https://img.shields.io/github/stars/mario-montanari/italiano-scrittura-anti-ai?style=for-the-badge)](https://github.com/mario-montanari/italiano-scrittura-anti-ai/stargazers)

**Suite per la lingua italiana e sistema avanzato anti AI, in Claude e non solo.** Scrive secondo la norma, corregge e rivede testi già scritti, traduce senza calchi, cattura la voce di un autore e la misura, riconosce e smonta la firma della prosa generata, difende un testo umano segnalato da un rilevatore automatico.

<details>
<summary><strong>Indice</strong></summary>

- [Che cos'è](#che-cosè)
- [I cinque lavori che sa fare](#i-cinque-lavori-che-sa-fare)
- [Che cosa contiene](#che-cosa-contiene)
- [Lo strumento eseguibile](#lo-strumento-eseguibile)
- [Prerequisiti](#prerequisiti)
- [Installazione](#installazione)
- [Come si attiva](#come-si-attiva)
- [Un esempio, prima e dopo](#un-esempio-prima-e-dopo)
- [Le regole che non si negoziano](#le-regole-che-non-si-negoziano)
- [Struttura della skill](#struttura-della-skill)
- [Risorse complementari](#risorse-complementari)
- [Prossimi passi](#prossimi-passi)
- [Contributi](#contributi)
- [Licenza](#licenza)
- [Crediti e fonti](#crediti-e-fonti)
- [Autore](#autore)

</details>

## Che cos'è

Una biblioteca di lavoro sull'italiano scritto, in forma di skill: tredici guide operative, oltre trentasettemila parole di regole, esempi e correzioni, più uno strumento eseguibile che misura la voce di un autore.

Il nome dice «anti ai» perché da lì è nata, dalla firma riconoscibile che i modelli linguistici lasciano nei testi italiani. Ma il materiale che serve a togliere quella firma è lo stesso che serve a scrivere bene: la grammatica normativa dell'Accademia, il lessico giusto al posto di quello comodo, il ritmo della frase, i sei registri dell'italiano e le loro norme editoriali, la lezione dei prosatori del Novecento. Su un testo scritto da una persona funziona esattamente come su un testo generato, e nella metà dei casi è così che viene usata.

Il principio sta in una riga. La macchina produce la media statistica, l'autore produce la deviazione dalla media: questa skill serve a intercettare la prima e a costruire la seconda.

**In Claude e non solo.** Il formato è quello aperto delle Agent Skills, un file indice con frontmatter e una cartella di guide in Markdown: si installa in Claude Code, su claude.ai e via API. Le regole però sono testo, e restano leggibili da qualunque altro modello a cui si passi la cartella, o da una persona che voglia usarle come manuale. L'unico pezzo che chiede un interprete è lo strumento facoltativo, e serve a misurare, non a scrivere.

<p align="right"><a href="#italiano-scrittura-anti-ai">torna in alto</a></p>

## I cinque lavori che sa fare

### 1. Scrivere in italiano corretto

Un testo nuovo, dalla prima riga, con la norma applicata mentre si scrive e non controllata dopo: articoli davanti alle consonanti difficili (*lo studente*, *gli psicologi*, *l'IBAN*, *lo SPID*, *la iena*), accenti acuti e gravi al posto giusto, apostrofi che rispondono a una regola e non all'orecchio (*qual è* senza, *un po'* con), congiuntivo e consecutio, trattino breve, medio e lungo distinti per funzione, caporali come standard per dialoghi e citazioni.

### 2. Correggere e rivedere un testo già scritto

Bozze, articoli, tesi, relazioni, capitoli: la skill lavora su testo altrui senza chiedere chi lo ha scritto. Ha una checklist pre-consegna in undici famiglie tematiche, venti stringhe da cercare con il Trova, una tabella sinottica dei difetti con la correzione accanto, e un metodo di revisione in due passaggi che prima elenca i difetti e poi li corregge, invece di riscrivere tutto a occhio. Gli errori che tolgono credibilità in una riga (*un'altro*, *qual'è*, *un pò*, *perchè*, il *piuttosto che* usato al posto di *oppure*) hanno una voce dedicata ciascuno.

### 3. Tradurre verso l'italiano

I calchi dall'inglese sono il difetto più difficile da sentire, perché suonano familiari a chi ha appena letto l'originale. La skill porta il catalogo dei calchi lessicali e sintattici (*navigare le complessità*, *elevare il tuo business*, *approfondire*, *sfruttare*), la tabella dei falsi amici, e le alternative agli anglicismi secondo Zoppetti e Marazzini.

### 4. Catturare la voce di chi firma

Quando si scrive per un cliente, o per sé stessi, la voce dell'autore prevale sui filtri generici: un tratto che sembra artificiale ma è autentico per quella persona va rispettato. La skill porta il metodo per catturarla da un corpus di testi veri, con due livelli tenuti separati (il misurato, riproducibile da chiunque; l'osservato, dove ogni affermazione porta il passo che la dimostra), il modello di scheda da compilare, e il confine oltre il quale la voce non vince: la norma della lingua non è gusto, e nessuno ha una voce fatta di errori.

### 5. Difendere un testo umano accusato da un rilevatore

Se un docente, un committente o una redazione contesta la paternità di un testo, la skill costruisce la risposta: che cosa misura davvero quel punteggio, quanto sbagliano quegli strumenti secondo le misure pubblicate (Liang 2023, Weber-Wulff 2023, il ritiro dell'AI Text Classifier di OpenAI, la disattivazione decisa da Vanderbilt), il vuoto di dati sull'italiano documentato dai benchmark multilingue, i sette passaggi della difesa e due modelli di documento.

Serve a difendere un testo umano accusato ingiustamente. Non serve a far passare per umano un testo generato, e non contiene niente che aiuti a farlo.

<p align="right"><a href="#italiano-scrittura-anti-ai">torna in alto</a></p>

## Che cosa contiene

Tredici guide, caricate da Claude quando servono, più le quindici regole che valgono sempre.

| Guida | Che cosa porta |
| --- | --- |
| `grammatica-italiana.md` | articoli, accenti, apostrofi, punteggiatura, trattini, virgolette, congiuntivo, consecutio, preposizioni |
| `lessico-da-evitare.md` | catalogo del lessico con soglie di densità, calchi, falsi amici, anglicismi con alternative |
| `pattern-strutturali.md` | venti pattern smontati: gonfiatura, participio parassita, perifrasi della copula, meta-annunci, variazione elegante, contrasti fittizi |
| `metodologie-operative.md` | soppressione durante la stesura, quattro tecniche di prevenzione, revisione in due passaggi, calibrazione della voce, sei mosse di umanizzazione |
| `personalita-e-anima.md` | sei sintomi della scrittura asettica, sei tecniche per rimettere qualcuno dentro il testo, guardia contro il finto umano |
| `maestri-della-deviazione.md` | sette autori italiani, la mossa-firma di ognuno, il passo che la mostra, la regola per portarla via |
| `voce-personale.md` | profilo di voce in due livelli, scheda compilabile, confine fra voce e norma |
| `registri-e-contesti.md` | sei registri, norme editoriali, bibliografie, ISBN e deposito legale, SEO italiano, E-E-A-T |
| `segnali-misurabili.md` | segnali con base peer-reviewed: MATTR, pronomi, emozioni, interiorità, sottotesto, template sintattici |
| `leak-conversazionale.md` | il testo che parla come una chat: negazioni preventive, suspense inutile, riassunti di sé stesso |
| `canali-lettore-saggistica.md` | i quattro canali attraverso cui un lettore gode di un testo, come griglia diagnostica |
| `checklist-finale.md` | undici famiglie di controllo, venti red flag per il Trova, tabella sinottica |
| `scudo-falsi-positivi.md` | difesa di un testo umano segnalato, con le fonti per esteso |

<p align="right"><a href="#italiano-scrittura-anti-ai">torna in alto</a></p>

## Lo strumento eseguibile

`scripts/profilo_voce.py` calcola il profilo quantitativo di una voce da una cartella di testi dello stesso autore e dello stesso registro.

```bash
python scripts/profilo_voce.py cartella-dei-testi --nome "Nome autore" --out cartella-di-uscita
```

Misura il respiro della frase (lunghezza media, oscillazione, quota di domande), il respiro del paragrafo, la leggibilità Gulpease su blocchi separati, la varietà lessicale, la punteggiatura come firma involontaria, la persona a cui l'autore si rivolge, e le ricorrenze che tornano dove non servirebbero. Produce una scheda leggibile e i dati grezzi in JSON, e ogni misura dichiara che cosa non dice.

Lo strumento misura e non giudica: non stabilisce se un testo sia stato generato da una macchina, e nessuno strumento al mondo lo fa in modo affidabile. Sotto le duemila parole di corpus il profilo esce dichiarato come indicativo. Chi non ha Python usa la skill per intero senza perdere niente, perché le stesse misure si ricavano a mano su cinquanta frasi e la procedura è scritta nel comando.

`scripts/prova_profilo_voce.py` porta duecentoquarantadue prove automatiche, e girano anche in continua a ogni push e a ogni pull request. Ognuna nasce da un difetto trovato durante l'audit, e serve a impedire che torni.

<p align="right"><a href="#italiano-scrittura-anti-ai">torna in alto</a></p>

## Prerequisiti

- **Per la skill**: Claude Code, oppure claude.ai (app desktop o web) con le skill personali abilitate. Nient'altro.
- **Per lo strumento facoltativo**: Python 3, senza librerie esterne. La continua lo esegue su Python 3.12.

## Installazione

Questa repo è due cose insieme, e si sceglie quale usare.

È un **plugin**, con il suo manifest in `.claude-plugin/plugin.json`: si installa in un colpo solo e porta con sé la skill e i due comandi `/calibra-voce` e `/difendi`, già pronti. Il formato è quello che Claude Code e Claude Cowork condividono.

Ed è una **skill semplice**, una cartella con dentro `SKILL.md`: si copia dove le skill vivono e funziona come ha sempre funzionato, senza plugin e senza marketplace. Chi la usa così non deve cambiare niente.

### Come plugin, in Claude Code

```bash
claude plugin marketplace add mario-montanari/italiano-scrittura-anti-ai
claude plugin install italiano-scrittura-anti-ai@mario-montanari-skills
```

La repo fa da catalogo di sé stessa: `.claude-plugin/marketplace.json` dichiara il marketplace `mario-montanari-skills`, che contiene questo unico plugin.

Per provarlo senza installare niente, da una copia locale della repo:

```bash
claude --plugin-dir ./italiano-scrittura-anti-ai
```

I comandi arrivano con il prefisso del plugin: `/italiano-scrittura-anti-ai:calibra-voce` e `/italiano-scrittura-anti-ai:difendi`.

### Come plugin, in Claude Cowork

Il plugin è nello stesso formato che Cowork usa, ma lì l'installazione non è dell'utente: la fa chi amministra l'organizzazione, dalle impostazioni, caricando il pacchetto o collegando una repo. Se in Cowork ti serve questo plugin, il pacchetto da consegnare a chi amministra è questa repo così com'è.

### Come skill, in Claude Code, per un progetto

Copiare la cartella `italiano-scrittura-anti-ai/` dentro `.claude/skills/` del progetto:

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

### In Claude Code, per tutti i progetti

Copiare la stessa cartella in `~/.claude/skills/` su Linux e macOS, o nel percorso equivalente su Windows.

### Su claude.ai

Le skill personali si caricano dalle Impostazioni, sezione Capabilities, voce Skills, seguendo le istruzioni ufficiali Anthropic.

### Via API

Il meccanismo di caricamento delle skill via API è documentato nella documentazione Anthropic ufficiale.

### Verificare che funzioni

Chiedere a Claude di scrivere un paragrafo italiano su un argomento qualsiasi. Se la skill è attiva, il testo non contiene em-dash, i titoli non hanno le maiuscole all'inglese, le citazioni stanno fra caporali.

<p align="right"><a href="#italiano-scrittura-anti-ai">torna in alto</a></p>

## Come si attiva

Da sola, quando si chiede a Claude di:

- scrivere, redigere o generare un testo italiano destinato a qualcuno
- tradurre in italiano
- revisionare, correggere o migliorare un testo italiano, scritto da chiunque
- «umanizzare» un testo italiano prodotto da un modello
- correggere grammatica e stile
- rispondere a un rilevatore automatico che ha segnalato un testo come generato
- catturare o calibrare la voce di un autore da un corpus di suoi testi

Resta fuori dalle chat informali brevi e dai contesti non testuali come codice, dati e configurazioni. Due comandi facoltativi, `/calibra-voce` e `/difendi`, guidano i due flussi più lunghi passo per passo.

## Un esempio, prima e dopo

**Testo generato e non revisionato:**

> «Nel panorama editoriale in continua evoluzione, è fondamentale sottolineare come l'intelligenza artificiale stia rivoluzionando il modo in cui scriviamo. Diversi studi dimostrano che l'AI offre numerosi vantaggi, tra cui la possibilità di ottimizzare i processi creativi e sbloccare il potenziale degli autori. Non si tratta solo di uno strumento, ma di un vero e proprio punto di svolta. In conclusione, l'AI rappresenta una risorsa imprescindibile per chiunque voglia approfondire il proprio percorso editoriale.»

Quattro frasi, quindici pattern, zero informazioni verificabili.

**Lo stesso contenuto, scritto:**

> «L'intelligenza artificiale è entrata nei processi editoriali italiani nel 2023, due anni dopo il boom anglofono. Gli editori che la usano oggi la impiegano soprattutto per tre cose: editing di prima passata, traduzioni grezze da rifinire, generazione di varianti di copy per A/B test. Non ha sostituito nessuno, ma ha cambiato il mestiere di chi sta davanti al testo. Continuo a pensare a quello che mi disse un editor cinque mesi fa: «Adesso lavoro meno con Word, lavoro più con domande».»

Data verificabile, tre casi d'uso concreti, una posizione presa, la prima persona, una citazione datata fra caporali. Stesso argomento, e un testo che respira.

<p align="right"><a href="#italiano-scrittura-anti-ai">torna in alto</a></p>

## Le regole che non si negoziano

Quindici, applicate sempre, anche senza aprire una guida. Le prime cinque, per dare la misura:

1. **Mai em-dash** (—) in un testo italiano: al suo posto virgole, parentesi tonde, due punti.
2. **Mai maiuscole all'inglese** nei titoli: *Come ottimizzare la SEO*, mai *Come Ottimizzare la SEO*.
3. **Mai virgolette inglesi** per dialoghi e citazioni: si usano le caporali.
4. **Mai aprire** con *Nel mondo di oggi*, *Nell'era digitale*, *Ti sei mai chiesto…?*
5. **Mai chiudere** con *In conclusione*, *Spero che questo articolo ti sia utile*.

L'elenco completo sta in [SKILL.md](SKILL.md), e comprende gli errori ortografici da Trova e Sostituisci, il *piuttosto che* disgiuntivo, e l'obbligo di variare la lunghezza delle frasi dentro ogni paragrafo.

## Struttura della skill

```text
italiano-scrittura-anti-ai/
├── .claude-plugin/
│   ├── plugin.json                    # Manifest del plugin: nome, versione, autore, licenza
│   └── marketplace.json               # Catalogo: la repo fa da marketplace di sé stessa
├── assets/
│   └── banner.png                     # L'immagine del README, versionata qui e non esterna
├── commands/                          # I due comandi, nativi quando si installa il plugin
│   ├── calibra-voce.md                # Comando /calibra-voce
│   └── difendi.md                     # Comando /difendi
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
├── references/                        # Le tredici guide, caricate quando servono
│   ├── grammatica-italiana.md
│   ├── lessico-da-evitare.md
│   ├── pattern-strutturali.md
│   ├── metodologie-operative.md
│   ├── voce-personale.md
│   ├── maestri-della-deviazione.md
│   ├── personalita-e-anima.md
│   ├── checklist-finale.md
│   ├── registri-e-contesti.md
│   ├── segnali-misurabili.md
│   ├── leak-conversazionale.md
│   ├── canali-lettore-saggistica.md
│   └── scudo-falsi-positivi.md
├── scripts/                           # Strumenti facoltativi, sola libreria standard Python
│   ├── profilo_voce.py                # Calcola il profilo quantitativo di una voce
│   └── prova_profilo_voce.py          # 242 prove automatiche, una per ogni difetto corretto
└── extras/                            # Risorse complementari opzionali
    ├── README.md                      # I tre livelli di copertura
    ├── CLAUDE.md.example              # Template per Claude Code
    ├── user-preferences.example.md    # Template per claude.ai
    └── hooks/
        └── consenti-solo-profilo-voce.py  # Hook PreToolUse facoltativo
```

<p align="right"><a href="#italiano-scrittura-anti-ai">torna in alto</a></p>

## Risorse complementari

La skill interviene sui testi che contano. Per il resto della giornata, dove non si attiva (chat informali, commenti tecnici, risposte veloci), la cartella `extras/` porta due template che tengono in piedi le stesse regole.

- **`extras/CLAUDE.md.example`**: memoria persistente per Claude Code, da mettere in `~/.claude/CLAUDE.md` o nella radice di un progetto.
- **`extras/user-preferences.example.md`**: testo da incollare nelle user preferences di claude.ai.
- **`commands/calibra-voce.md`** e **`commands/difendi.md`**: i due comandi, da copiare in `.claude/commands/`. Funzionano anche da soli, senza installare la skill intera.
- **`extras/hooks/consenti-solo-profilo-voce.py`**: hook facoltativo per chi calibra spesso e vuole togliere la conferma manuale al lancio dello strumento, senza allargare la superficie eseguibile.

I due template contengono le venti regole essenziali estratte dalla skill, scritte come istruzioni dirette sempre attive. È la filosofia dei tre livelli: la skill come bisturi, il file di memoria e le preferenze come igiene quotidiana. I dettagli stanno in [extras/README.md](extras/README.md).

## Prossimi passi

Senza date promesse, e in ordine di utilità dichiarata:

- **Plugin Claude Code** con i due comandi nativi, al posto dei file da copiare a mano in `.claude/commands/`.
- **Avviso sulla lingua del corpus** nello strumento, che oggi produce una scheda dalla forma regolare anche su testi che non sono in italiano.
- Il resto nasce dalle segnalazioni: i pattern che la skill non copre ancora arrivano da chi scrive in italiano tutti i giorni.

<p align="right"><a href="#italiano-scrittura-anti-ai">torna in alto</a></p>

## Contributi

I contributi sono benvenuti.

- **Segnalazioni:** aprire un issue con la descrizione chiara del problema o del suggerimento.
- **Pull request:** per le modifiche alle guide, allegare la motivazione e, quando possibile, una fonte o un esempio concreto.
- **Nuovi pattern:** se trovate un pattern AI italiano che la skill non copre, proponetelo con parole spia, esempio negativo, spiegazione del problema e correzione.

Le discussioni stilistiche sono ammesse e incoraggiate, purché ancorate a fonti (Crusca, Treccani, Serianni, manuali editoriali) o a corpora verificabili. Il formato di un pattern e le tre vie del contributo stanno in [CONTRIBUTING.md](CONTRIBUTING.md).

## Licenza

MIT License. Il testo completo sta nel file [LICENSE](LICENSE).

Significa che si può usare, modificare e integrare in qualsiasi progetto, anche commerciale, mantenendo l'attribuzione. La licenza è scelta per massimizzare la riutilizzabilità da parte della comunità italiana.

L'upgrade 1.1.0 incorpora concetti adattati dal repository `creative-writing-skills` di haowjy, distribuito con licenza Apache 2.0. Le due licenze sono compatibili: si può integrare materiale Apache 2.0 in un progetto MIT mantenendo l'attribuzione, che è riportata sia in fondo ai tre reference interessati sia nella sezione crediti. La licenza della skill resta MIT.

<p align="right"><a href="#italiano-scrittura-anti-ai">torna in alto</a></p>

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
- **Skill Humanizer open source**, basata sul WikiProject AI Cleanup

**Fonte dell'upgrade 1.1.0 (segnali misurabili, leak conversazionale, canali del lettore):**

- **`creative-writing-skills` di haowjy**, licenza Apache 2.0. I tre reference adattano in italiano concetti tratti da quel repository (antipatterns, leak del registro conversazionale, canali di ricompensa del lettore). L'attribuzione è riportata anche in fondo a ciascuno dei tre file.

**Fonti scientifiche aggiunte con l'upgrade 1.1.0:**

- Kobak, González-Márquez, Horvát, Lause (2024), *Delving into LLM-assisted writing in biomedical publications through excess vocabulary*, arXiv:2406.07016: vocabolario in eccesso e parole di stile come marcatori d'uso degli LLM
- Shaib, Elazar, Li, Wallace (2024), *Detection and Measurement of Syntactic Templates in Generated Text*, EMNLP 2024, arXiv:2407.00211: template sintattici ripetuti
- Covington, McFall (2010), *Cutting the Gordian Knot: The Moving-Average Type-Token Ratio (MATTR)*, Journal of Quantitative Linguistics: metrica della varietà lessicale robusta rispetto alla lunghezza
- van Laer, de Ruyter, Visconti, Wetzels (2014), *The Extended Transportation-Imagery Model*, Journal of Consumer Research 40(5), doi:10.1086/673383: il trasporto narrativo come costrutto misurabile
- Thissen, Menninghaus, Schlotz (2018), *Measuring optimal reading experiences: The reading flow short scale*, Frontiers in Psychology, doi:10.3389/fpsyg.2018.02542: il flusso di lettura
- Hemingway, *Death in the Afternoon* (1932), capitolo 16: la teoria dell'iceberg

A tutti questi autori, istituzioni e progetti va il riconoscimento per aver fornito la base su cui questa skill è costruita.

<p align="right"><a href="#italiano-scrittura-anti-ai">torna in alto</a></p>

## Autore

**Mario Montanari**

Sito personale: [mariomontanari.it](https://mariomontanari.it)

Il progetto nasce da trent'anni di scrittura professionale e dall'osservazione sistematica dell'italiano prodotto dalle macchine. È pensato come contributo alla comunità italiana che lavora con Claude e con gli altri modelli linguistici.

<p align="right"><a href="#italiano-scrittura-anti-ai">torna in alto</a></p>

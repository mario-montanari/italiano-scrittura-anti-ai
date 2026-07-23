# Changelog

Tutte le modifiche rilevanti alla skill sono annotate qui. Il formato segue la convenzione Keep a Changelog; la numerazione segue il versionamento semantico.

## [1.3.0] - 2026-07-23

Due aggiunte. Il calibratore della voce personale è il primo pezzo eseguibile: la skill smette di essere solo un manuale e comincia a misurare ciò che finora indicava a parole. Lo scudo contro i falsi positivi sposta invece il lavoro dal testo all'accusa, e risponde alla domanda di chi si vede segnalare come generato un testo che ha scritto.

### Aggiunto

- `references/voce-personale.md`: metodo completo per catturare e usare la voce di un autore. Espande la sezione 4 di `metodologie-operative.md` con la raccolta del corpus e i suoi errori tipici, la separazione fra livello misurato e livello osservato, il modello di scheda voce con un esempio compilato su dati reali, le istruzioni operative per scrivere sul profilo, e il confine oltre il quale la voce non prevale: le regole non negoziabili sono norma della lingua e non gusto, quindi nessuno ha una voce fatta di errori ortografici o di segni che l'italiano non usa.
- `extras/commands/calibra-voce.md`: comando `/calibra-voce` da copiare in `.claude/commands/`. Guida la verifica del corpus (un registro alla volta, soglia di parole, voce reale o desiderata), calcola il livello misurato con lo script quando è disponibile, ricava il livello osservato leggendo i testi con citazione obbligatoria dei passi, e compone la scheda. I comandi personalizzati di Claude Code sono unificati con le skill, quindi una repo che distribuisce una skill singola consegna il comando come file da copiare; il plugin con i comandi nativi resta un passo successivo.
- `scripts/profilo_voce.py`: strumento facoltativo che calcola il profilo quantitativo di una voce da una cartella di testi. Solo libreria standard di Python, nessuna installazione, nessun accesso alla rete, nessuna scrittura fuori dalla cartella di uscita. Produce una scheda leggibile e i dati grezzi in JSON. Misura respiro della frase e del paragrafo, leggibilità Gulpease per blocchi, varietà lessicale con MATTR, punteggiatura, persona, ricorrenze, aperture e chiusure di frase. Ogni misura dichiara cosa non dice.
- `references/scudo-falsi-positivi.md`: come si risponde quando un rilevatore automatico segnala come generato un testo scritto da una persona. Contiene il confine d'uso, che cosa misura davvero un rilevatore, le evidenze pubblicate sui suoi errori verificate una a una sul primario (Liang 2023 con il 61,3 per cento di falsi positivi sui saggi di non madrelingua, Weber-Wulff 2023, il ritiro dell'AI Text Classifier di OpenAI, le cifre dichiarate da Turnitin, la disattivazione decisa da Vanderbilt), il vuoto di misure sull'italiano documentato dai benchmark CEAID e MULTITuDE, i sette passaggi della difesa e i due modelli di documento. Il settimo passaggio rifiuta la riscrittura del testo dopo l'accusa, per un motivo pratico prima che etico: distrugge la prova di processo e somiglia a una manomissione. La sezione 3 riporta anche l'obiezione che rende datate quelle evidenze, cioè il working paper NBER di Jabarian e Imas del settembre 2025, e ne accoglie la parte vera: sul loro corpus inglese i tre prodotti commerciali provati sbagliano fra lo 0,1 e lo 0,7 per cento, quindi nessuno può più sostenere che ogni rilevatore sbagli sempre. Resta che un prodotto solo su tre rispetta il tetto che quegli autori propongono, e che nel loro corpus non c'è un elaborato scolastico, uno scrivente non madrelingua o un testo italiano.
- `.github/workflows/codeql.yml`: analisi statica CodeQL sull'unica parte eseguibile della skill, cioè `scripts/profilo_voce.py`. Permessi `read-all` in cima al workflow e scrittura confinata al solo job che ne ha bisogno, action pinnate a SHA completo invece che a tag mutabile, esecuzione a ogni push su `main`, a ogni pull request e una volta a settimana. È il primo workflow della repo, e nasce con la versione che per la prima volta pubblica del codice.
- `.github/dependabot.yml`: aggiornamento settimanale dell'unico ecosistema presente, cioè le action usate dal workflow, che essendo pinnate a SHA non si aggiornano da sole. La skill non ha dipendenze di runtime, perché lo strumento usa la sola libreria standard di Python.
- `extras/commands/difendi.md`: comando `/difendi` da copiare in `.claude/commands/`. Raccoglie i fatti dell'accusa, distingue i tre casi possibili, verifica i materiali dell'autore prima di usarli e compone il documento. Fra gli strumenti permessi non c'è `Bash`: nessuno strumento va eseguito sul testo contestato per stabilirne la natura, perché un punteggio prodotto lì varrebbe quanto quello che si sta contestando.

### Modificato

- `SKILL.md`: rimandi ai due nuovi reference nella calibrazione del contesto, nell'elenco di consultazione e fra le schede dei reference disponibili; nuova sezione «Strumenti inclusi» che dichiara lo script come facoltativo e presenta i due comandi; nuovo blocco «Limite d'uso» dopo la regola 15, che fissa il confine della difesa e dichiara che nessuno strumento certifica la paternità umana di un testo, nemmeno questa skill.
- `README.md`: la difesa dalle accuse dei rilevatori fra le cose che la skill fornisce, struttura aggiornata con i due nuovi reference, la cartella `scripts/` e i due comandi, risorse complementari estese ai comandi. Corretto il conteggio dell'elenco di apertura, che annunciava tre voci mentre erano quattro. Tolta dall'apertura la frase «Non è solo una questione estetica: è un problema pratico», che usava in vetrina lo schema di negazione vietato da `references/leak-conversazionale.md`: la frase dopo dice già quali sono i costi, e il lettore la conclusione la tira da solo.
- `references/segnali-misurabili.md`: la sezione 8 affermava senza fonte che sull'italiano i falsi positivi sono alti. Resta ora solo ciò che si può sostenere: dove l'errore è stato misurato, cioè sull'inglese, è risultato grande, mentre sull'italiano nessuno lo ha misurato e i due benchmark multilingue che coprono sedici lingue lasciano fuori la nostra.
- `references/checklist-finale.md`: stessa correzione nella voce di controllo sui detector, con il rimando al nuovo reference.
- `references/metodologie-operative.md`: la sezione 5 attribuiva le sei mosse di umanizzazione a «Calvino, Eco, Levi, Carrada, Testa, Severgnini». Severgnini non compariva in nessun altro punto della skill, e Carrada e Testa non compaiono in quella sezione, dove stanno invece Camilleri con il dialetto e gli altri tre con un esempio a testa. L'attribuzione nomina ora i quattro autori che quelle mosse le mostrano davvero, e la stessa correzione è stata portata nelle due descrizioni che la ripetevano, in `SKILL.md` e nel `README.md`. Nella terza mossa, «chiude con sentenze brevi?» diventa «chiude con massime brevi?»: il senso era quello giusto, ma accanto a una domanda sulle frasi la parola si prestava a essere letta come il calco da *sentences*, cioè l'errore che questo file insegna a evitare.
- `extras/README.md`: installazione del secondo comando, e le due cose che per scelta non fa.
- `SECURITY.md`: la politica dichiarava che questa skill «è fatta di testo e non esegue codice». Con l'arrivo di `scripts/profilo_voce.py` la frase è diventata falsa, e una politica di sicurezza che descrive male la propria superficie vale meno di nessuna politica. Ora dichiara qual è la parte eseguibile e che cosa fa davvero: sola libreria standard, nessun accesso alla rete, nessuna installazione, due soli file scritti nella cartella di uscita indicata da chi lancia lo strumento.
- `references/voce-personale.md`, `extras/commands/calibra-voce.md` ed `extras/README.md`: tre frasi costruite sullo schema «non è X, è Y» riscritte in forma affermativa. In tutti e tre i casi l'equivoco corretto dalla negazione era reale, quindi la regola di `references/leak-conversazionale.md` le avrebbe assolte. A una skill che quello schema lo vieta conviene però non usarlo mai, nemmeno dove sarebbe lecito.

### Nota di metodo

Il collaudo dello strumento ha smentito una delle attese dichiarate prima di eseguirlo: su un corpus tematico, un testo generato da un modello ha ottenuto varietà lessicale più alta di un corpus umano, perché la prosa artificiale evita la ripetizione con la variazione elegante. La misura porta ora una cautela permanente nella scheda. Il risultato conferma quanto `segnali-misurabili.md` sezione 2 già avvertiva: varietà alta non significa infilare sinonimi rari.

## [1.2.0] - 2026-07-22

Upgrade di contenuto. Due nuove guardie di qualità che nascono da semi già presenti nella skill: la galleria dei maestri della deviazione e la difesa contro l'over-humanizing.

### Aggiunto

- `references/maestri-della-deviazione.md`: galleria di sette autori italiani (Calvino, Eco, Levi, Ginzburg, Testa, Camilleri, Carrada), ognuno con la mossa-firma, un passo che la mostra e la regola per portarla via. Ribalta l'asse della sezione 5 di `metodologie-operative.md`, dove le mosse sono indicizzate per tecnica: qui si parte dall'autore. Citazioni reali solo dove verificabili, con opera e anno; per gli altri, esempi costruiti nello stile e dichiarati come tali, mai false attribuzioni. Le schede di Calvino ed Eco riprendono passaggi già presenti nella sezione 5 di `metodologie-operative.md`.

### Modificato

- `references/personalita-e-anima.md`: nuova sezione 4 «Il profumo dell'umanizzatore», con i sei sintomi del finto-umano di plastica e il test «si può togliere senza perdere senso?». Indice e numerazione delle sezioni successive aggiornati.
- `SKILL.md`: rimandi alle due nuove guardie nella sezione di consultazione e nell'elenco dei reference.
- `references/checklist-finale.md`: due controlli nella famiglia Anima, uno contro il finto-umano di plastica e uno che rimanda alla deviazione d'autore.

## [1.1.1] - 2026-07-20

Rilascio di igiene e coerenza. Nessun cambiamento ai contenuti metodologici, solo pulizia, community health e conformità.

### Aggiunto

- `CONTRIBUTING.md`: le tre vie del contributo, il formato di un pattern (parola spia, esempio negativo, spiegazione, correzione), convenzioni di commit e versione.
- `CODE_OF_CONDUCT.md`: Contributor Covenant 3.0 in versione italiana, con l'originale inglese come testo di riferimento.
- `SECURITY.md`: segnalazione privata tramite il private vulnerability reporting di GitHub.
- `.github/ISSUE_TEMPLATE/`: template di segnalazione e di proposta di un pattern, più `config.yml`.
- `.github/PULL_REQUEST_TEMPLATE.md`: checklist con fonti citate e testo che passa l'audit della skill stessa.
- `CITATION.cff`: metadati per citare la skill.

### Modificato

- `SKILL.md`: rimosso il campo `license` dal frontmatter. Resta la coppia canonica `name` più `description`; la licenza vive nel file `LICENSE`.
- Coerenza di genere: «la skill» al femminile nei quattro punti prima al maschile (`README.md`, `references/personalita-e-anima.md` e `references/metodologie-operative.md`, quest'ultimo in due punti).
- `references/metodologie-operative.md`: nota di cautela nella sezione 6, le cifre per modello sono stime indicative e ordini di grandezza, non misurazioni pubblicate.

## [1.1.0] - 2026-06-03

Upgrade che integra materiale di ricerca selezionato e sposta il baricentro dalle liste di parole ai segnali misurabili.

### Aggiunto

- `references/segnali-misurabili.md`: i segnali anti-AI con base peer-reviewed (varietà lessicale via MATTR, densità di pronomi personali, eccesso di emozioni positive, interiorità superficiale, basso sottotesto, template sintattici ripetuti), con esempi italiani e fonti scientifiche verificate (Kobak 2024, Shaib 2024, Covington e McFall 2010).
- `references/leak-conversazionale.md`: il leak del registro conversazionale nei documenti, cioè il testo che parla come se rispondesse in chat. Pattern di negazione che corregge un equivoco inesistente (*non è X, è Y*), suspense inutile (*qui sta il punto*), riassunti frattali, domande messe in bocca al lettore, con correzione alla radice.
- `references/canali-lettore-saggistica.md`: i quattro canali attraverso cui un lettore gode di un testo (fiducia nel lettore, piacere estetico, trasporto, fluidità), adattati alla saggistica e usati come griglia diagnostica, con fonti scientifiche verificate (van Laer 2014, Thissen 2018, Hemingway 1932).
- `CHANGELOG.md`: questo file.

### Modificato

- `SKILL.md`: aggiunti i rimandi ai tre nuovi reference nella sezione di consultazione e nell'elenco finale.
- `references/checklist-finale.md`: aggiunte tre nuove famiglie di controlli (segnali misurabili, leak del registro conversazionale, canali del lettore) e nuove stringhe di ricerca rapida.
- `references/lessico-da-evitare.md`: declassate le liste di parole da rilevatore affidabile a preferenza di gusto editoriale, con rimando a `segnali-misurabili.md`. Le liste restano integre: cambia solo il loro statuto.
- `README.md`: aggiornati badge di versione, struttura della skill, sezione «Cosa fa questa skill» (quarto punto), crediti e fonti, nota sulla compatibilità delle licenze.

### Attribuzione

I tre nuovi reference adattano in italiano concetti tratti dal repository `creative-writing-skills` di haowjy, distribuito con licenza Apache 2.0, compatibile con la licenza MIT di questa skill. L'attribuzione è riportata in fondo a ciascuno dei tre file e nei crediti del README. La licenza della skill resta MIT.

## [1.0.0] - 2026-04-18

Prima versione pubblica. Grammatica normativa italiana, catalogo del lessico AI da evitare, pattern strutturali, metodologie operative, personalità e anima, checklist finale, registri e contesti, più la cartella `extras/` con i template per Claude Code e per le user preferences di claude.ai.

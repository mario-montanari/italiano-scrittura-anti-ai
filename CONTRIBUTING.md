# Come contribuire

Grazie per l'interesse verso questa skill. I contributi sono benvenuti: nuovi pattern, correzioni, fonti, esempi di riscrittura.

## Le tre vie del contributo

- **Segnalazioni.** Apri una issue con il template di segnalazione. Prima cerca fra le issue esistenti, per non duplicare.
- **Proposta di un pattern.** Se hai trovato un pattern AI italiano che la skill non copre, usa il template «Proposta di un pattern». Serve: la parola o struttura spia, un esempio negativo reale, la spiegazione del perché è un tic dell'AI, la riscrittura corretta. Una fonte o un corpus verificabile sono graditi.
- **Pull request.** Per modifiche ai reference, allega la motivazione e, dove puoi, una fonte o un esempio concreto. Tieni ogni PR piccola e a fuoco.

## Il formato di un pattern

Ogni pattern che entra nella skill rispetta la stessa forma, quella che trovi nei reference:

1. **Parola o struttura spia**: cosa tradisce l'AI.
2. **Esempio negativo**: una frase reale che suona generata.
3. **Perché è un pattern AI**: calco dall'inglese, gonfiatura, meta-annuncio, ritmo piatto, e simili.
4. **Correzione**: la stessa frase riscritta in italiano che respira.
5. **Fonte** (facoltativa): Crusca, Treccani, Serianni, un manuale editoriale, un corpus, o una misura ripetibile.

Le discussioni di stile sono ammesse e incoraggiate, purché ancorate a fonti o a corpora verificabili. La skill declassa le liste di parole a preferenza di gusto: una proposta regge meglio se porta una misura, non solo un'impressione.

## Messaggi di commit

Il progetto usa i [Conventional Commits](https://www.conventionalcommits.org):

- `feat:` una funzione nuova
- `fix:` una correzione
- `docs:` solo documentazione
- `chore:` manutenzione

Le modifiche che rompono la compatibilità riportano `BREAKING CHANGE:` nel corpo del commit. La numerazione segue il versionamento semantico, il changelog il formato Keep a Changelog.

## Prima di aprire una pull request

- Il testo che aggiungi passa l'audit della skill stessa: niente em-dash, caporali «», niente lessico da chatbot, ritmo variato.
- Ogni affermazione su come scrivono gli LLM o gli umani cita una fonte.
- Se tocchi una regola, aggiungi la voce nel `CHANGELOG.md` sotto l'intestazione della versione, con la data al momento del rilascio (formato Keep a Changelog: `## [x.y.z] - AAAA-MM-GG`).

## Codice di condotta

Partecipando al progetto accetti il [Codice di condotta](CODE_OF_CONDUCT.md).

# Changelog

Tutte le modifiche rilevanti alla skill sono annotate qui. Il formato segue la convenzione Keep a Changelog; la numerazione segue il versionamento semantico.

## [1.1.0]

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

## [1.0.0]

Prima versione pubblica. Grammatica normativa italiana, catalogo del lessico AI da evitare, pattern strutturali, metodologie operative, personalità e anima, checklist finale, registri e contesti, più la cartella `extras/` con i template per Claude Code e per le user preferences di claude.ai.

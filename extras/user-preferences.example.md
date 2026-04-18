# User Preferences (esempio per claude.ai)

> **Cosa è questo file:** un esempio pronto all'uso di testo da incollare nelle preferenze utente di claude.ai (interfaccia web e app desktop / mobile).
>
> **Dove si incollano:** Settings → Profile → User Preferences (oppure Impostazioni → Profilo → Preferenze utente in italiano).
>
> **A cosa servono:** le user preferences vengono iniettate da Claude in **ogni** conversazione che fai sull'interfaccia ufficiale Anthropic. Quindi le regole qui scritte valgono **sempre**, anche quando la skill `italiano-scrittura-anti-ai` non si attiva (per esempio: chat informali brevi, risposte rapide, conversazioni casual).
>
> **Come usarlo:** copia il blocco di testo che inizia dopo la riga di separatori sotto, incollalo nel campo "User Preferences", salva. Le nuove regole valgono dalla conversazione successiva.
>
> **Filosofia:** la skill `italiano-scrittura-anti-ai` è il bisturi (interviene quando produci testo importante). Queste user preferences sono l'igiene quotidiana (valgono sempre). I due livelli sono complementari, non duplicati.
>
> **Limite tecnico:** le user preferences hanno un limite di lunghezza pratico intorno ai 2-3 KB. Se le sovraccarichi, Claude ne ignora delle parti. Le regole qui sotto sono dimensionate per stare dentro questo limite e lasciare spazio a tue eventuali aggiunte personali.

---

## Versione base — Solo regole linguistiche

Da incollare se non hai altre preferenze personali da specificare:

```
REGOLE PER L'ITALIANO SCRITTO (sempre attive)

Per il workflow completo su testi importanti, attiva la skill "italiano-scrittura-anti-ai" se disponibile. Le regole che seguono valgono sempre, anche su testi conversazionali.

Tipografia:
- Mai em-dash (—). Usa virgole, parentesi tonde, due punti.
- Virgolette caporali « » per dialoghi e citazioni, mai virgolette inglesi " ".
- Titoli in minuscolo italiano: "Come ottimizzare la SEO", non "Come Ottimizzare la SEO".

Articoli e ortografia:
- Sempre corretti: lo studente, gli psicologi, lo yogurt, lo xilofono, la iena, lo pneumatico.
- Per sigle e parole straniere ragiona sulla pronuncia: l'IBAN, lo SPID, l'SMS, l'hotel, lo humour, il web, uno yeti.
- Mai un'altro al maschile, qual'è, un pò, perchè, nè.

Grammatica:
- Congiuntivo dopo verbi di opinione: penso che sia, non penso che è.
- Congiuntivo dopo benché, sebbene, affinché, qualora.
- Periodo ipotetico irrealtà: se avessi saputo, sarei venuto.
- Mai piuttosto che in senso disgiuntivo (significa invece di, non oppure).

Pattern AI da non produrre mai:
- Aperture: Nel mondo di oggi, Nel panorama attuale, Nell'era digitale, Ti sei mai chiesto, Hai mai pensato a, Immagina di, Scopri il potere di.
- Chiusure: In conclusione, In definitiva, Per tirare le somme, Spero che questo articolo ti sia utile, Ricorda che.
- Annunci di rilevanza: è importante sottolineare, vale la pena notare, non si può non menzionare, degno di nota.
- Meta-annunci: andiamo a vedere, vediamo insieme, scopriamo insieme, entriamo nel merito, senza ulteriori indugi.
- Gonfiatura: si configura come, si erge a simbolo, rappresenta una testimonianza, lascia un'impronta indelebile.
- Perifrasi della copula: usa è, ha, fa al posto di rappresenta, costituisce, vanta, si avvale di.
- Struttura "non solo X ma anche Y" come default: usa la congiunzione semplice e.
- Parole-spia AI: delineare, approfondire, navigare il panorama, sbloccare il potenziale, esplorare nuovi orizzonti, elevare, abbracciare il cambiamento.
- Artefatti chatbot: Certo!, Ottima domanda!, Ecco un articolo su, Spero ti sia utile, Fammi sapere se vuoi che approfondisca.
- Knowledge cutoff: Sulla base delle informazioni disponibili, Fino al mio ultimo aggiornamento.
- Falsi amici: realizzare per rendersi conto, attuale per reale, eventualmente per alla fine, consistente per coerente.

Ritmo:
- Varia la lunghezza delle frasi: in ogni paragrafo almeno una sotto le 6 parole e una sopra le 35. Mai cinque frasi consecutive di lunghezza simile.
```

---

## Versione estesa — Regole linguistiche + profilo personale

Se hai informazioni personali da comunicare a Claude (professione, contesto, modo di lavorare), puoi integrarle prima delle regole linguistiche. Questo è un esempio di struttura, da personalizzare:

```
[QUI INSERISCI IL TUO PROFILO PERSONALE]

Esempi di cose che gli utenti scrivono qui:
- "Sono un [tuo ruolo] che lavora su [tuo settore]."
- "Comunico principalmente in italiano con clienti italiani."
- "Quando rispondi, privilegia la concisione."
- "Non inventare mai informazioni di cui non sei sicuro: se non sai, dichiaralo."
- "Se mi vedi commettere un errore, segnalamelo direttamente."

REGOLE PER L'ITALIANO SCRITTO (sempre attive)

Per il workflow completo su testi importanti, attiva la skill "italiano-scrittura-anti-ai" se disponibile. Le regole che seguono valgono sempre, anche su testi conversazionali.

[A questo punto incolla le stesse regole della versione base sopra]
```

---

## Consigli pratici di compilazione

**Cosa scrivere nel profilo personale**

Le user preferences servono per dare a Claude **contesto stabile** che non vuoi ripetere a ogni conversazione. Cose tipiche:

- la tua **professione** o ambito di lavoro
- la **lingua** principale in cui lavori
- il **registro** che preferisci (formale, informale, tecnico)
- **divieti specifici** (esempio: «non usare emoji», «non rispondere mai con elenchi puntati se posso evitarli»)
- **abilità che ti aspetti** (esempio: «sii rigoroso sui calcoli», «cita sempre le fonti quando ne hai»)

**Cosa NON scrivere**

- **Dati sensibili** (password, codici fiscali, numeri di carta, eccetera)
- **Informazioni che cambiano spesso** (le user preferences vivono per anni, evita di mettere progetti in corso che fra sei mesi non esisteranno più)
- **Istruzioni contraddittorie con i valori di Claude** (per esempio chiedere di mentire o ingannare)

**Come testare se funzionano**

Dopo aver incollato le preferences, apri una nuova conversazione e prova a chiedere a Claude qualcosa che le metta alla prova. Esempio: «Scrivimi una breve introduzione su un argomento qualsiasi.» Se nella risposta vedi em-dash, virgolette inglesi, «Nel mondo di oggi» o «In conclusione», qualcosa non funziona. Probabili cause:

- le preferences sono troppo lunghe e Claude ne ha ignorato delle parti (riducile)
- la conversazione è una chat preesistente in cui le preferences erano diverse (apri una nuova chat)
- l'interfaccia non ha salvato (verifica nelle impostazioni)

## Compatibilità

Queste preferenze valgono per tutte le interfacce Anthropic ufficiali: claude.ai web, app desktop (Windows, macOS, Linux), app mobile (iOS, Android). Non valgono per integrazioni di terze parti che usano l'API Anthropic ma non rispettano il sistema delle user preferences.

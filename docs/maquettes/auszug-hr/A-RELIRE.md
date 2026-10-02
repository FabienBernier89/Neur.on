# Maquettes auszug-hr · textes à relire

Ce fichier liste tous les textes qui ne viennent pas mot pour mot d'une source publiée :
les traductions DE et IT, et les quelques textes rédigés pour la maquette en EN et en FR
(meta description, libellés d'accessibilité, texte alternatif).

## Sources par langue

| Langue | Accueil | Pages légales (`impressum/`, `privacy-policy/`) |
|---|---|---|
| EN | auszug-hr.ch/en, mot pour mot | neur-on.ai/impressum/ et neur-on.ai/privacy-policy/, mot pour mot |
| FR | auszug-hr.ch/fr, mot pour mot | Texte français déjà publié sur le nouveau site Neur.on (`src/pages/mentions-legales/` et `src/pages/protection-des-donnees/`), repris tel quel |
| DE | **Traduction par Claude** (le site source n'a pas de version allemande) | **Traduction par Claude** de la version anglaise |
| IT | **Traduction par Claude** (le site source n'a pas de version italienne) | **Traduction par Claude** de la version anglaise |

Slugs : les mêmes dans les quatre langues (`/{langue}/impressum/`, `/{langue}/privacy-policy/`), comme les
routes de l'application source (`/en/order_translation`, `/fr/order_translation`).

Conventions de traduction : DE en allemand standard suisse (ss, jamais d'eszett ; guillemets « » ; vouvoiement
« Sie ») ; IT en italien de Suisse (guillemets « » ; adresse au pluriel « voi »). Terminologie fournie par la
coordination : Handelsregister / registro di commercio, Handelsregisterauszug / estratto del registro di commercio,
UID / IDI, Apostille / apostille, Haager Übereinkommen vom 5. Oktober 1961 / Convenzione dell’Aia del 5 ottobre 1961,
beglaubigte Übersetzung / traduzione certificata, notarielle Beglaubigung / autenticazione notarile.

## Termes à confirmer

| Langue | Terme retenu | Source | Doute |
|---|---|---|---|
| DE | Firma (onglet, étape 1, texte d'aide) | Company Name / Raison sociale | Terme du droit suisse des raisons de commerce (Code des obligations) ; « Firmenname » serait plus clair pour le grand public. |
| IT | Ditta (onglet, étape 1, texte d'aide) | Company Name / Raison sociale | Terme du registre de commerce ; « ragione sociale » serait une alternative, à vérifier selon l'usage tessinois. |
| IT | impresa | company / entreprise | Choix de l'usage administratif (registro di commercio) plutôt que « società » ou « azienda ». |
| DE | Corrext-Standardbeglaubigung, Beglaubigungsstufe | Standard Corrext Certification, certification level | Le certificat Corrext n'est pas une légalisation officielle : « Bescheinigung » ou « Zertifizierung » pourrait être préféré. |
| DE | Rechtslinguisten | Lawyer-Linguists / juristes-linguistes | « Juristen-Linguisten » ou « juristische Linguisten » existent aussi. |
| IT | giuristi linguisti | Lawyer-Linguists | Variante possible : « giuristi-linguisti ». |
| DE / IT | Schweizer Staatskanzlei / Cancelleria dello Stato svizzera competente | competent Swiss State Chancellery | En Suisse, l'apostille est délivrée par la chancellerie cantonale compétente (ou la Chancellerie fédérale) : à vérifier. |
| DE / IT | Neur.on AI Solutions SA (pages légales) | Neur.on AI Solutions Ltd (source anglaise) | Raison sociale inscrite gardée telle quelle plutôt que traduite en « AG ». |
| IT | Friburgo (dans la phrase), Fribourg (dans l'adresse) | Fribourg | Usage italien pour le nom de ville, forme postale pour l'adresse. |
| IT | Impressum e condizioni d’uso | Impressum & Terms of Use | « Impressum » est courant en Suisse italienne ; « Note legali » est une alternative. |
| DE / IT | Über uns / Chi siamo | About / À propos | Le bloc présente le service plutôt que l'entreprise. |
| IT | adresse au pluriel « voi » | you / vous | Le registre « Lei » est une alternative plus formelle. |

## DE · allemand standard suisse

**Traduction automatique par Claude, à faire relire par un traducteur expert avant publication.**

### Page `de/index.html`

| Emplacement | Texte |
|---|---|
| `<title>` | Handelsregisterauszug \| Corrext |
| `<meta name="description">` | Bestellen Sie online eine beglaubigte Übersetzung von Schweizer Handelsregisterauszügen: Standardbeglaubigung, notarielle Beglaubigung oder Apostille nach dem Haager Übereinkommen, präzise juristische Terminologie, +30 Sprachen. Ab CHF 99.- |
| En-tête · bouton contact | Kontaktieren Sie uns |
| En-tête et appels · bouton commande | Übersetzung bestellen |
| En-tête · `alt` du logo | Corrext-Logo |
| En-tête · `aria-label` sélecteur de langue | Sprache |
| En-tête · `aria-label` menu de langue compact | Sprache: Deutsch |
| Héro · surtitre | Beglaubigung oder Apostille |
| Héro · h1 (partie 1) | Bestellen Sie eine beglaubigte Übersetzung |
| Héro · h1 (partie 2, en bleu ciel) | von Schweizer Handelsregisterauszügen |
| Héro · `aria-label` du formulaire | Unternehmenssuche |
| Héro · « Search by: » | Suche nach: |
| Héro · onglet nom | Firma |
| Héro · onglet UID | UID |
| Héro · texte d'aide, mode nom | Schweizer Unternehmen nach Firma suchen… |
| Héro · texte d'aide, mode UID | CHE-123.456.789 |
| Héro · bouton de recherche | Suchen |
| Héro · pastille de prix | Ab CHF 99.- |
| Héro · `aria-label` de l'illustration | Illustration: ein deutschsprachiger Handelsregisterauszug und seine beglaubigte Übersetzung ins Französische, mit Siegel und Apostille |
| Héro · garantie 1 | Übersetzungen für alle amtlichen Zwecke |
| Héro · garantie 2 | Präzise juristische Terminologie |
| Héro · garantie 3 | Notarielle Beglaubigung & Apostille nach dem Haager Übereinkommen |
| Héro · garantie 4 | +30 Sprachen |
| About · surtitre | Über uns |
| About · titre | Eine hochwertige, rechtskonforme Übersetzung |
| About · sous-titre | Benötigen Sie eine beglaubigte Übersetzung eines Auszugs aus dem Schweizer Handelsregister? |
| About · paragraphe 1 | Als erster Schweizer Anbieter juristischer Übersetzungen mit einem vollständig digitalisierten Bestellprozess gewährleisten wir beglaubigte Übersetzungen von Schweizer Handelsregisterauszügen, die schnell, zuverlässig und amtlich anerkannt sind. |
| About · paragraphe 2 | Wir arbeiten ausschliesslich mit professionellen juristischen Übersetzerinnen und Übersetzern zusammen, die auf Dokumente des «Corporate Housekeeping» spezialisiert sind, und liefern Übersetzungen, die den rechtlichen Anforderungen in der Schweiz und im Ausland vollumfänglich entsprechen. |
| About · paragraphe 3 | Ob Sie eine Standardbeglaubigung, eine notarielle Beglaubigung oder eine Beglaubigung mit Apostille gemäss dem Haager Übereinkommen vom 5. Oktober 1961 benötigen: Unser Service deckt sämtliche Formalitäten im Zusammenhang mit der Übersetzung von Schweizer Handelsregisterauszügen ab. |
| About · bloc 1 · titre | KI-gestützte Übersetzung |
| About · bloc 1 · paragraphe 1 | Das Corrext-Team aus Rechtslinguisten und Data Scientists hat die erste Reihe von Sprachmodellen entwickelt, die speziell mit Schweizer Handelsregisterauszügen trainiert wurden. |
| About · bloc 1 · paragraphe 2 | Diese Modelle stellen sicher, dass die schweizerische Rechtsterminologie in der Zielsprache präzise wiedergegeben und von Behörden sowie Rechtsfachleuten in ausländischen Rechtsordnungen richtig verstanden wird. |
| About · bloc 1 · paragraphe 3 | Durch die Verbindung von menschlicher Expertise und fortschrittlicher Technologie bieten wir einen schnellen, hochwertigen und zuverlässigen Service. |
| About · bloc 2 · titre | Deckt jeden Beglaubigungsbedarf ab |
| About · bloc 2 · texte et trois niveaux | Corrext bietet drei Beglaubigungsstufen, die allen rechtlichen und administrativen Anforderungen gerecht werden: <br>· Corrext-Standardbeglaubigung: Die Übersetzung wird mit einer ordnungsgemäss unterzeichneten und gestempelten Bescheinigung ausgestellt, welche die Qualifikationen der Übersetzerin oder des Übersetzers bestätigt und bescheinigt, dass die Übersetzung mit der gebotenen Sorgfalt und nach bestem Wissen und Können erstellt wurde.<br>· Notarielle Beglaubigung: Für Dokumente, die zusätzliches rechtliches Gewicht haben müssen, kann die Corrext-Bescheinigung von einer Schweizer Notarin oder einem Schweizer Notar beglaubigt werden. Dies gewährleistet die formelle Anerkennung durch Gerichte und Verwaltungsbehörden.<br>· Notarielle Beglaubigung und Apostille: Sind Dokumente für die Verwendung im Ausland bestimmt, können wir eine Apostille der zuständigen Schweizer Staatskanzlei gemäss dem Haager Übereinkommen vom 5. Oktober 1961 beschaffen. Diese Formalität ermöglicht die Anerkennung durch ausländische Gerichte und Behörden in den Vertragsstaaten des Übereinkommens. |
| About · bloc 3 · titre | Vollständig digitalisierter Prozess |
| About · bloc 3 · paragraphe 1 | Unser Service ist als vollständig digitalisierter, nahtloser Prozess konzipiert, von der Bestellung bis zur Lieferung einer beglaubigten Übersetzung, die sofort verwendet werden kann. |
| About · bloc 3 · paragraphe 2 | Wir übernehmen den gesamten Ablauf für Sie: Beschaffung des Handelsregisterauszugs, professionelle juristische Übersetzung und Beglaubigung sowie, falls erforderlich, notarielle Beglaubigung und Apostille. Nach Fertigstellung werden Ihnen die Dokumente direkt per E-Mail und bei Bedarf in gedruckter Form per Post oder Kurier zugestellt. |
| About · bloc 3 · paragraphe 3 | Mit der End-to-End-Lösung von Corrext haben Sie während des gesamten Prozesses eine einzige Ansprechstelle. So entfällt der Aufwand, mit mehreren Anbietern und Behörden zu verkehren, Ihre administrativen Formalitäten werden vereinfacht und Sie sparen wertvolle Zeit. |
| How it works · surtitre | So funktioniert es |
| How it works · titre | Wie lassen Sie Ihren Handelsregisterauszug übersetzen? |
| How it works · introduction | Eine beglaubigte Übersetzung eines Schweizer Handelsregisterauszugs zu bestellen, war noch nie so einfach. Über unsere intuitive Online-Plattform wählen Sie einfach die Zielsprache, die Beglaubigungsstufe (Standard, notariell oder notariell mit Apostille) und die Lieferart. Der gesamte Prozess ist schnell, transparent und sicher gestaltet und gewährleistet, dass Ihre Dokumente in der Schweiz und im Ausland amtlich gültig sind. |
| How it works · étape 1 · titre | Unternehmen suchen |
| How it works · étape 1 · texte | Geben Sie die Firma oder die UID des im Schweizer Handelsregister eingetragenen Unternehmens ein, für das Sie eine beglaubigte Übersetzung benötigen. Wählen Sie anschliessend die Zielsprache (Deutsch, Französisch, Italienisch, Englisch, Spanisch usw.). |
| How it works · étape 2 · titre | Beglaubigungsstufe wählen |
| How it works · étape 2 · texte | Wählen Sie den für Ihre Übersetzung erforderlichen Grad an Förmlichkeit:  <br>· Corrext-Standardbeglaubigung<br>· Notarielle Beglaubigung<br>· Notarielle Beglaubigung und Apostille |
| How it works · étape 3 · titre | Lieferart wählen |
| How it works · étape 3 · texte | Legen Sie fest, wie Sie Ihre beglaubigte Übersetzung erhalten möchten: elektronisch per E-Mail oder sowohl elektronisch als auch in gedruckter Form per Post oder Kurier. |
| How it works · étape 4 · titre | Lieferfrist festlegen |
| How it works · étape 4 · texte | Wählen Sie die Lieferoption: Standardlieferung oder Expresslieferung (in der Schweiz und für internationale Bestimmungsorte verfügbar). |
| Certifications · surtitre | Beglaubigungen |
| Certifications · titre | Die Vorteile der verschiedenen Beglaubigungsstufen |
| Certifications · paragraphe 1 | Jeder Kunde und jedes Verfahren ist einzigartig. Deshalb bietet Ihnen Corrext die Flexibilität, die Beglaubigungsstufe zu wählen, die am besten zu Ihrer Situation passt. |
| Certifications · paragraphe 2 | Ob Sie lediglich eine zuverlässige Übersetzung eines Schweizer Handelsregisterauszugs benötigen oder diese bei schweizerischen oder ausländischen Behörden einreichen müssen: Wir bieten Ihnen die passende Lösung. Dank diesem massgeschneiderten Ansatz optimieren Sie Ihre Kosten und stellen gleichzeitig sicher, dass Ihre Übersetzung den rechtlichen oder administrativen Anforderungen Ihres Falls entspricht. |
| Certifications · paragraphe 3 | Klicken Sie auf die Felder rechts, um mehr über die einzelnen Beglaubigungsoptionen zu erfahren. |
| Certifications · case 1 · titre | Corrext-Standardbeglaubigung |
| Certifications · case 1 · texte | Der Übersetzung liegt eine ordnungsgemäss unterzeichnete und gestempelte Bescheinigung bei, welche die Qualifikationen der Übersetzerin oder des Übersetzers bestätigt und bescheinigt, dass die Übersetzung nach bestem Wissen, Können und Gewissen vollständig und korrekt ist. |
| Certifications · case 2 · titre | Notarielle Beglaubigung |
| Certifications · case 2 · texte | Die Unterschrift auf der Übersetzungsbescheinigung von Corrext wird von einer Schweizer Notarin oder einem Schweizer Notar ordnungsgemäss beglaubigt. Diese zusätzliche Formalität kann von Gerichten oder Verwaltungsbehörden verlangt werden, um die Übersetzung für den amtlichen Gebrauch zu validieren. |
| Certifications · case 3 · titre | Notarielle Beglaubigung und Apostille |
| Certifications · case 3 · texte | Für die Verwendung im Ausland kann die notarielle Beglaubigung mit einer «Apostille» der zuständigen Schweizer Staatskanzlei gemäss dem Haager Übereinkommen vom 5. Oktober 1961 versehen werden. Diese zusätzliche Formalität kann von ausländischen Gerichten oder Verwaltungsbehörden verlangt werden. Die Apostille wird ausschliesslich in den Vertragsstaaten des Haager Übereinkommens anerkannt. |
| Confidentiality · surtitre | Vertraulichkeit |
| Confidentiality · titre | So schützen wir Ihre Daten |
| Confidentiality · carte 1 (titre en gras puis texte) | Sicherheit liegt in unserer DNA. Da Vertraulichkeit in jedem rechtlichen Kontext entscheidend ist, haben wir die Zertifizierung nach ISO 27001 erlangt, dem internationalen Massstab für Informationssicherheit. |
| Confidentiality · carte 2 (titre en gras puis texte) | Kontinuierliche Verbesserung. Wir verbessern unsere Prozesse laufend, um sichere, präzise und kosteneffiziente Ergebnisse zu liefern. |
| Confidentiality · carte 3 (titre en gras puis texte) | Volle Rechtskonformität. Wir halten uns strikt an alle massgeblichen Datenschutzbestimmungen, einschliesslich des Schweizer Datenschutzgesetzes (DSG) und der DSGVO der EU. |
| Confidentiality · carte 4 (titre en gras puis texte) | Infrastruktur in der Schweiz. Wir setzen ausschliesslich auf eine souveräne Schweizer Infrastruktur, im Einklang mit dem langjährigen Engagement der Schweiz für Diskretion und Vertraulichkeit. |
| Bande finale · titre | Bestellen Sie eine beglaubigte Übersetzung von Schweizer Handelsregisterauszügen |
| Pied de page · lien 1 | Nutzungsbedingungen |
| Pied de page · lien 2 | Datenschutz |
| Pied de page · `aria-label` des liens légaux | Rechtliches |

### Page `de/impressum/index.html`

| Emplacement | Texte |
|---|---|
| `<title>` | Impressum & Nutzungsbedingungen \| Corrext |
| h1 | Impressum & Nutzungsbedingungen |
| Intertitre | Kontaktadresse und Verantwortlicher für die Datenbearbeitung |
| Paragraphe 1 | Neur.on AI Solutions SA / Place de la Gare 15 / 1700 Fribourg |
| Paragraphe 2 | E-Mail: dataprotection[at]neur-on.ai |
| Paragraphe 3 | Tel.: +41 44 291 94 19 |
| Paragraphe 4 | Diese Website ist Eigentum der Neur.on AI Solutions SA, Fribourg, und wird von ihr betrieben. |
| Paragraphe 5 | Mit der Nutzung dieser Website bestätigen Sie, dass Sie diese Nutzungsbedingungen gelesen und verstanden haben, und verpflichten sich, sie jederzeit einzuhalten. |
| Intertitre | Geistiges Eigentum |
| Paragraphe 6 | Sämtliche Inhalte dieser Website jeglicher Art (Texte, Grafiken, Logos, PDF-Dateien usw.) sind grundsätzlich durch schweizerisches oder ausländisches Urheberrecht geschützt und stehen im Eigentum der Neur.on AI Solutions SA oder wurden ihr im Rahmen einer nicht übertragbaren Lizenz überlassen. Diese Inhalte werden ausschliesslich zu Informationszwecken, zu Werbezwecken oder im Zusammenhang mit den Dienstleistungen zur Verfügung gestellt, welche die Neur.on AI Solutions SA für ihre Kundinnen und Kunden erbringt, und es ist strengstens untersagt, sie ohne vorgängige schriftliche Zustimmung der Neur.on AI Solutions SA zu anderen Zwecken zu vervielfältigen, zu bearbeiten, zu verbreiten oder zu verwerten. |
| Intertitre | Links zu anderen Websites |
| Paragraphe 7 | Unsere Website enthält Links zu Websites oder Diensten Dritter, die weder in unserem Eigentum stehen noch von uns kontrolliert werden. Wir sind nicht verantwortlich für die Inhalte, Richtlinien oder Praktiken von Websites oder Diensten Dritter, auf die unsere Website verlinkt. Es liegt in Ihrer Verantwortung, die Nutzungsbedingungen und Datenschutzerklärungen dieser Websites Dritter zu lesen, bevor Sie diese nutzen. |
| Intertitre | Änderungen |
| Paragraphe 8 | Diese Nutzungsbedingungen können von Zeit zu Zeit geändert werden, um die Übereinstimmung mit dem geltenden Recht zu gewährleisten und Änderungen in der Art und Weise, wie wir unsere Website betreiben, Rechnung zu tragen. Es liegt in der Verantwortung der Nutzerinnen und Nutzer, regelmässig zu prüfen, ob Änderungen vorgenommen wurden. |
| Intertitre | Anwendbares Recht |
| Paragraphe 9 | Diese Nutzungsbedingungen unterstehen schweizerischem Recht. |
| Intertitre | Kontaktangaben |
| Paragraphe 10 | Bei Fragen oder Anliegen kontaktieren Sie uns bitte über unser Kontaktformular unter der entsprechenden Registerkarte bzw. Webseite. |
| Paragraphe 11 | Version vom Februar 2024 |

### Page `de/privacy-policy/index.html`

| Emplacement | Texte |
|---|---|
| `<title>` | Datenschutz und Datensicherheit \| Corrext |
| h1 | Datenschutz und Datensicherheit |
| Intertitre | 1. Erhobene Daten und Rechte der betroffenen Personen |
| Paragraphe 1 | Wenn Sie unsere Website besuchen, erheben wir verschiedene Daten, von denen einige als Personendaten gelten. In Bezug auf Ihre Personendaten, die sich in unserem Besitz befinden, haben Sie folgende Rechte: |
| Paragraphe 2 | das Recht, von uns Auskunft über die Personendaten zu verlangen, die wir über Sie besitzen; |
| Paragraphe 3 | das Recht, diese Daten von uns berichtigen oder löschen zu lassen; |
| Paragraphe 4 | das Recht, die Bearbeitung Ihrer Personendaten durch uns abzulehnen oder einzuschränken. |
| Paragraphe 5 | Beruht die von uns vorgenommene Bearbeitung auf Ihrer Einwilligung, können Sie diese jederzeit ohne Angabe von Gründen mit einer schriftlichen Anfrage an die oben angegebene Adresse widerrufen. Bitte beachten Sie, dass wir solche Anfragen erst bearbeiten können, wenn wir einen Nachweis Ihrer Identität erhalten haben. |
| Intertitre | 2. Erhebung allgemeiner Daten |
| Paragraphe 6 | Bei jedem Besuch unserer Webseiten erheben wir eine Reihe allgemeiner Daten. Diese allgemeinen Daten und Informationen werden in Protokollen auf dem Server gespeichert. Folgende Daten werden erhoben: |
| Paragraphe 7 | IP-Adresse |
| Paragraphe 8 | Datum und Uhrzeit der Anfrage |
| Paragraphe 9 | Zeitzonendifferenz zur GMT |
| Paragraphe 10 | Inhalt Ihrer Anfrage |
| Paragraphe 11 | HTTP-Statuscode/Zugriffsstatus |
| Paragraphe 12 | Übertragene Datenmenge |
| Paragraphe 13 | Webseite, von der die Anfrage gesendet wurde |
| Paragraphe 14 | Browser (einschliesslich Sprache und Version) |
| Paragraphe 15 | Betriebssystem |
| Paragraphe 16 | Die erhobenen allgemeinen Daten werden keiner bestimmten Person zugeordnet. Wir benötigen diese Daten aus technischen Gründen, um unsere Website stabil und sicher bereitstellen zu können. |
| Intertitre | 3. Kontaktformular |
| Paragraphe 17 | Wenn Sie uns über das Kontaktformular eine Anfrage senden, werden die Daten, die Sie in das Formular eingeben, einschliesslich Ihrer Kontaktangaben, von uns gespeichert, damit wir Ihre Anfrage bearbeiten können. Die Bearbeitung dieser Informationen richtet sich nach unserer Datenschutzerklärung, von der Sie auf Anfrage eine Kopie erhalten können und deren Link in jeder Offerte enthalten ist, die wir für Sie erstellen. Wir geben diese Daten ohne Ihre Einwilligung nicht an Dritte weiter. |
| Paragraphe 18 | Die Informationen, die Sie in das Kontaktformular eingeben, werden nur so lange gespeichert, wie es für den vorgesehenen Zweck erforderlich ist. Hängt die Speicherung ausschliesslich von Ihrer Einwilligung ab, löschen wir die Informationen, sobald Sie Ihre Einwilligung widerrufen, es sei denn, eine längere Aufbewahrungsfrist ist gesetzlich vorgeschrieben. |
| Intertitre | 4. Cookies |
| Paragraphe 19 | Unsere Website verwendet Cookies. Dabei handelt es sich um kleine Textdateien, die auf Ihrem Computer gespeichert werden und abrufbare Informationen über Ihr Surfverhalten enthalten. Cookies dienen dazu, Ihre Verbindung zu unseren Webdiensten herzustellen und Ihr Surferlebnis individuell anzupassen. Cookies erfassen Informationen über Ihre IP-Adresse, Datum und Uhrzeit Ihres Besuchs, die Anzahl der Besuche, die verwendeten Formulare, Ihre Suchparameter, die von Ihnen angezeigten Seiten und Ihre bevorzugten Einstellungen auf unserer Website. |
| Paragraphe 20 | Bei den meisten von uns verwendeten Cookies handelt es sich um «Session-Cookies», die am Ende jedes Besuchs automatisch gelöscht werden. Andere Cookies bleiben auf Ihrem Computer gespeichert, bis Sie sie löschen. Sie können Ihren Browser so einstellen, dass unsere Website keine Cookies installieren kann oder dass Cookies generell deaktiviert werden. Zudem können Sie Ihren Browser jederzeit anweisen, alle bereits installierten Cookies zu löschen. In diesem Fall kann es sein, dass unsere Website aufgrund Ihrer Einstellungen nicht einwandfrei funktioniert. |
| Intertitre | 5. Web-Tracking |
| Paragraphe 21 | Unsere Website verwendet Web-Tracking-Tools, um Probleme zu erkennen, auf die Nutzerinnen und Nutzer stossen können, und um das Nutzererlebnis zu verbessern. |
| Paragraphe 22 | Google Analytics ist ein Webanalysedienst der Google Inc., 1600 Amphitheatre Parkway, Mountain View, CA 94043, U.S.A. (nachfolgend «Google»). Google Analytics verwendet Cookies, die eine Analyse der Nutzung unserer Website ermöglichen. Die durch die Cookies erzeugten Informationen werden in anonymisierter Form an einen Server von Google in den USA übertragen und dort gespeichert. Dank der Anonymisierung ist es unmöglich, diese Daten mit der betroffenen Person in Verbindung zu bringen. Google verwendet diese Informationen, um Ihre Nutzung unserer Website auszuwerten, Berichte über die Aktivitäten der Nutzerinnen und Nutzer zu erstellen und weitere mit der Nutzung unserer Website und des Internets im Allgemeinen verbundene Dienstleistungen zu erbringen. Sofern schweizerisches oder ausländisches Recht dies verlangt, können Google oder Dritte, die diese Daten in seinem Auftrag bearbeiten, diese Informationen an Dritte weitergeben. |
| Paragraphe 23 | Sie können verhindern, dass Google die durch die Cookies erzeugten Informationen über Ihre Nutzung unserer Website erfasst und bearbeitet, indem Sie das «Google Analytics Opt-out Browser Add-on» installieren, das hier verfügbar ist: https://tools.google.com/dlpage/gaoptout?hl=en. |
| Paragraphe 24 | Google ist nach dem Privacy Shield zertifiziert und gewährleistet damit die Einhaltung der europäischen Datenschutzgesetze (https://www.privacyshield.gov/participant?id=a2zt000000001L5AAI&status=Active). Weitere Informationen zur Datenbearbeitung durch Google finden Sie in der Datenschutzerklärung von Google: https://policies.google.com/privacy?hl=en. |
| Paragraphe 25 | Lucky Orange ist ein Analysetool der Lucky Orange LLC, 8665 W 96th St Suite #100, Overland Park, KS 66212, USA (nachfolgend «Lucky Orange»). Lucky Orange erfasst Informationen zum Datenverkehr auf unserer Website, etwa die besuchten Seiten, die Mausbewegungen und Klicks der Besucher, Tastatureingaben sowie HTML-Daten einer von einem Besucher aufgerufenen Seite, sofern diese HTML-Daten Personendaten enthalten. |
| Paragraphe 26 | Sie können verhindern, dass Lucky Orange Ihr Verhalten verfolgt, indem Sie die Funktion «Do not track» Ihres Browsers aktivieren. |
| Paragraphe 27 | Weitere Informationen zur Datenbearbeitung durch Lucky Orange finden Sie in der Datenschutzerklärung (https://www.luckyorange.com/legal/privacy) und den Nutzungsbedingungen (https://www.luckyorange.com/legal/terms) von Lucky Orange. |
| Paragraphe 28 | Version vom Februar 2023 |

## IT · italien de Suisse

**Traduction automatique par Claude, à faire relire par un traducteur expert avant publication.**

### Page `it/index.html`

| Emplacement | Texte |
|---|---|
| `<title>` | Estratto del registro di commercio \| Corrext |
| `<meta name="description">` | Ordinate online una traduzione certificata di estratti del registro di commercio svizzero: certificazione standard, autenticazione notarile o apostille secondo la Convenzione dell’Aia, terminologia giuridica precisa, +30 lingue. A partire da CHF 99.- |
| En-tête · bouton contact | Contattateci |
| En-tête et appels · bouton commande | Ordinate una traduzione |
| En-tête · `alt` du logo | Logo Corrext |
| En-tête · `aria-label` sélecteur de langue | Lingua |
| En-tête · `aria-label` menu de langue compact | Lingua: italiano |
| Héro · surtitre | Certificazione o apostille |
| Héro · h1 (partie 1) | Ordinate una traduzione certificata |
| Héro · h1 (partie 2, en bleu ciel) | di estratti del registro di commercio svizzero |
| Héro · `aria-label` du formulaire | Ricerca di imprese |
| Héro · « Search by: » | Ricerca per: |
| Héro · onglet nom | Ditta |
| Héro · onglet UID | IDI |
| Héro · texte d'aide, mode nom | Cercate un’impresa svizzera in base alla ditta… |
| Héro · texte d'aide, mode UID | CHE-123.456.789 |
| Héro · bouton de recherche | Cerca |
| Héro · pastille de prix | A partire da CHF 99.- |
| Héro · `aria-label` de l'illustration | Illustrazione: un estratto del registro di commercio in tedesco e la sua traduzione certificata in francese, con sigillo e apostille |
| Héro · garantie 1 | Traduzioni per tutti gli usi ufficiali |
| Héro · garantie 2 | Terminologia giuridica precisa |
| Héro · garantie 3 | Autenticazione notarile & apostille secondo la Convenzione dell’Aia |
| Héro · garantie 4 | +30 lingue |
| About · surtitre | Chi siamo |
| About · titre | Una traduzione di alta qualità e giuridicamente conforme |
| About · sous-titre | Avete bisogno di una traduzione certificata di un estratto del registro di commercio svizzero? |
| About · paragraphe 1 | In qualità di primo fornitore svizzero di traduzioni giuridiche con un processo di ordinazione interamente digitalizzato, garantiamo traduzioni certificate di estratti del registro di commercio svizzero rapide, affidabili e ufficialmente riconosciute. |
| About · paragraphe 2 | Collaboriamo esclusivamente con traduttrici e traduttori giuridici professionisti specializzati nei documenti di «corporate housekeeping», per fornire traduzioni pienamente conformi ai requisiti legali in Svizzera e all’estero. |
| About · paragraphe 3 | Che abbiate bisogno di una certificazione standard, di un’autenticazione notarile o di una certificazione con apostille rilasciata conformemente alla Convenzione dell’Aia del 5 ottobre 1961, il nostro servizio copre tutte le formalità relative alla traduzione di estratti del registro di commercio svizzero. |
| About · bloc 1 · titre | Traduzione assistita dall’IA |
| About · bloc 1 · paragraphe 1 | Il team Corrext, composto da giuristi linguisti e data scientist, ha sviluppato la prima serie di modelli linguistici addestrati specificamente su estratti del registro di commercio svizzero. |
| About · bloc 1 · paragraphe 2 | Questi modelli garantiscono che la terminologia giuridica svizzera sia resa con precisione nella lingua di arrivo e correttamente compresa dalle autorità e dai professionisti del diritto nelle giurisdizioni estere. |
| About · bloc 1 · paragraphe 3 | Combinando competenza umana e tecnologia avanzata, offriamo un servizio rapido, di alta qualità e affidabile. |
| About · bloc 2 · titre | Copre tutte le esigenze di certificazione |
| About · bloc 2 · texte et trois niveaux | Corrext offre tre livelli di certificazione per rispondere a ogni esigenza legale e amministrativa: <br>· Certificazione Corrext standard: la traduzione è corredata di un certificato, debitamente firmato e timbrato, che attesta le qualifiche della traduttrice o del traduttore e certifica che la traduzione è stata eseguita con la dovuta diligenza e al meglio delle sue capacità.<br>· Autenticazione notarile: per i documenti che devono avere un valore giuridico supplementare, il certificato Corrext può essere autenticato da un notaio svizzero. Ciò garantisce il riconoscimento formale da parte dei tribunali e delle autorità amministrative.<br>· Autenticazione notarile e apostille: se i documenti sono destinati all’estero, possiamo fornire un’apostille rilasciata dalla Cancelleria dello Stato svizzera competente ai sensi della Convenzione dell’Aia del 5 ottobre 1961. Questa formalità consente il riconoscimento da parte dei tribunali e delle autorità estere nei Paesi che sono parte della Convenzione. |
| About · bloc 3 · titre | Processo interamente digitalizzato |
| About · bloc 3 · paragraphe 1 | Il nostro servizio è concepito come un processo fluido e interamente digitalizzato, dall’ordinazione alla consegna di una traduzione certificata pronta per l’uso immediato. |
| About · bloc 3 · paragraphe 2 | Ci occupiamo per voi dell’intero processo: ottenimento dell’estratto del registro di commercio, traduzione giuridica professionale e certificazione, nonché, se necessario, autenticazione notarile e apostille. Una volta finalizzati, i documenti vi vengono inviati direttamente per e-mail e, se necessario, in forma cartacea per posta o corriere. |
| About · bloc 3 · paragraphe 3 | Con la soluzione completa di Corrext avete un unico interlocutore per l’intero processo. Evitate così di dover gestire più fornitori e autorità, semplificate le vostre formalità amministrative e risparmiate tempo prezioso. |
| How it works · surtitre | Come funziona |
| How it works · titre | Come tradurre il vostro estratto del registro di commercio? |
| How it works · introduction | Ordinare una traduzione certificata di un estratto del registro di commercio svizzero non è mai stato così semplice. Grazie alla nostra intuitiva piattaforma online, vi basta selezionare la lingua di traduzione, il livello di certificazione (standard, autenticazione notarile o autenticazione notarile con apostille) e la modalità di consegna. L’intero processo è concepito per essere rapido, trasparente e sicuro, garantendo che i vostri documenti siano ufficialmente validi in Svizzera e all’estero. |
| How it works · étape 1 · titre | Cercate l’impresa |
| How it works · étape 1 · texte | Inserite la ditta o l’IDI dell’impresa iscritta nel registro di commercio svizzero per la quale vi occorre una traduzione certificata. Selezionate poi la lingua di arrivo (tedesco, francese, italiano, inglese, spagnolo, ecc.). |
| How it works · étape 2 · titre | Selezionate il livello di certificazione |
| How it works · étape 2 · texte | Scegliete il grado di formalità richiesto per la vostra traduzione:  <br>· Certificazione Corrext standard<br>· Autenticazione notarile<br>· Autenticazione notarile e apostille |
| How it works · étape 3 · titre | Scegliete la modalità di consegna |
| How it works · étape 3 · texte | Decidete come desiderate ricevere la vostra traduzione certificata: in formato elettronico per e-mail, oppure sia in formato elettronico sia in forma cartacea per posta o corriere. |
| How it works · étape 4 · titre | Definite i tempi di consegna |
| How it works · étape 4 · texte | Selezionate l’opzione di consegna: consegna standard o consegna espressa (disponibile in Svizzera e per destinazioni internazionali). |
| Certifications · surtitre | Certificazioni |
| Certifications · titre | I vantaggi dei diversi livelli di certificazione |
| Certifications · paragraphe 1 | Ogni cliente e ogni procedura sono unici. Per questo Corrext vi offre la flessibilità di scegliere il livello di certificazione più adatto alla vostra situazione. |
| Certifications · paragraphe 2 | Che abbiate semplicemente bisogno di una traduzione affidabile di un estratto del registro di commercio svizzero o che dobbiate presentarla ad autorità svizzere o estere, vi proponiamo la soluzione adeguata. Questo approccio su misura vi consente di ottimizzare i costi, garantendo al contempo che la vostra traduzione soddisfi i requisiti legali o amministrativi del vostro caso. |
| Certifications · paragraphe 3 | Cliccate sui riquadri a destra per saperne di più su ciascuna opzione di certificazione. |
| Certifications · case 1 · titre | Certificazione Corrext standard |
| Certifications · case 1 · texte | La traduzione è corredata di un certificato debitamente firmato e timbrato che attesta le qualifiche della traduttrice o del traduttore e certifica che, secondo scienza e coscienza, la traduzione è completa e fedele. |
| Certifications · case 2 · titre | Autenticazione notarile |
| Certifications · case 2 · texte | La firma apposta sul certificato di traduzione Corrext è debitamente autenticata da un notaio svizzero. Questa formalità supplementare può essere richiesta dai tribunali o dalle autorità amministrative per convalidare la traduzione a fini ufficiali. |
| Certifications · case 3 · titre | Autenticazione notarile e apostille |
| Certifications · case 3 · texte | Per l’uso all’estero, l’autenticazione notarile può essere corredata di un’«apostille» rilasciata dalla Cancelleria dello Stato svizzera competente conformemente alla Convenzione dell’Aia del 5 ottobre 1961. Questa formalità supplementare può essere richiesta da tribunali o autorità amministrative esteri. L’apostille è riconosciuta esclusivamente nei Paesi che sono parte della Convenzione dell’Aia. |
| Confidentiality · surtitre | Riservatezza |
| Confidentiality · titre | Come proteggiamo i vostri dati |
| Confidentiality · carte 1 (titre en gras puis texte) | La sicurezza è nel nostro DNA. Poiché la riservatezza è fondamentale in ogni contesto giuridico, abbiamo ottenuto la certificazione ISO 27001, il riferimento internazionale in materia di sicurezza delle informazioni. |
| Confidentiality · carte 2 (titre en gras puis texte) | Miglioramento continuo. Perfezioniamo costantemente i nostri processi per offrire risultati sicuri, precisi ed economicamente vantaggiosi. |
| Confidentiality · carte 3 (titre en gras puis texte) | Piena conformità giuridica. Rispettiamo rigorosamente tutte le disposizioni pertinenti in materia di protezione dei dati, compresa la legge federale sulla protezione dei dati (LPD) e il RGPD dell’Unione europea. |
| Confidentiality · carte 4 (titre en gras puis texte) | Infrastruttura in Svizzera. Ci affidiamo esclusivamente a un’infrastruttura svizzera sovrana, in linea con l’impegno storico della Svizzera a favore della discrezione e della riservatezza. |
| Bande finale · titre | Ordinate una traduzione certificata di estratti del registro di commercio svizzero |
| Pied de page · lien 1 | Condizioni d’uso |
| Pied de page · lien 2 | Protezione dei dati |
| Pied de page · `aria-label` des liens légaux | Note legali |

### Page `it/impressum/index.html`

| Emplacement | Texte |
|---|---|
| `<title>` | Impressum e condizioni d’uso \| Corrext |
| h1 | Impressum e condizioni d’uso |
| Intertitre | Indirizzo di contatto e titolare del trattamento |
| Paragraphe 1 | Neur.on AI Solutions SA / Place de la Gare 15 / 1700 Fribourg |
| Paragraphe 2 | E-mail: dataprotection[at]neur-on.ai |
| Paragraphe 3 | Tel.: +41 44 291 94 19 |
| Paragraphe 4 | Questo sito web è di proprietà di Neur.on AI Solutions SA, Friburgo, che lo gestisce. |
| Paragraphe 5 | Utilizzando questo sito web, dichiarate di aver letto e compreso le presenti condizioni d’uso e vi impegnate a rispettarle in ogni momento. |
| Intertitre | Proprietà intellettuale |
| Paragraphe 6 | L’intero contenuto di questo sito web, di qualsiasi natura (testi, grafici, loghi, file PDF, ecc.), è di norma protetto dal diritto d’autore svizzero o estero ed è di proprietà di Neur.on AI Solutions SA o le è stato ceduto in virtù di una licenza non trasferibile. Tale contenuto è messo a disposizione esclusivamente a titolo informativo, a fini pubblicitari o in relazione ai servizi forniti da Neur.on AI Solutions SA ai propri clienti, ed è severamente vietato riprodurlo, elaborarlo, diffonderlo o sfruttarlo per qualsiasi altro scopo senza il previo consenso scritto di Neur.on AI Solutions SA. |
| Intertitre | Link ad altri siti web |
| Paragraphe 7 | Il nostro sito web contiene link a siti web o servizi di terzi che non possediamo né controlliamo. Non siamo responsabili del contenuto, delle politiche o delle pratiche dei siti web o dei servizi di terzi ai quali il nostro sito rimanda. È vostra responsabilità leggere le condizioni d’uso e le informative sulla protezione dei dati di tali siti web di terzi prima di utilizzarli. |
| Intertitre | Modifiche |
| Paragraphe 8 | Le presenti condizioni d’uso possono essere modificate di tanto in tanto per garantirne la conformità alla legge e per riflettere eventuali cambiamenti nel modo in cui gestiamo il nostro sito web. Spetta agli utenti verificare a intervalli regolari l’eventuale presenza di modifiche. |
| Intertitre | Diritto applicabile |
| Paragraphe 9 | Le presenti condizioni d’uso sono disciplinate dal diritto svizzero. |
| Intertitre | Recapiti |
| Paragraphe 10 | Per qualsiasi domanda o dubbio, contattateci tramite il nostro modulo di contatto nella scheda o pagina web corrispondente. |
| Paragraphe 11 | Versione di febbraio 2024 |

### Page `it/privacy-policy/index.html`

| Emplacement | Texte |
|---|---|
| `<title>` | Protezione e sicurezza dei dati \| Corrext |
| h1 | Protezione e sicurezza dei dati |
| Intertitre | 1. Dati raccolti e diritti delle persone interessate |
| Paragraphe 1 | Quando navigate sul nostro sito web, raccogliamo diversi dati, alcuni dei quali sono considerati dati personali. Per quanto riguarda i vostri dati personali in nostro possesso, disponete dei seguenti diritti: |
| Paragraphe 2 | il diritto di chiederci informazioni sui dati personali che deteniamo su di voi; |
| Paragraphe 3 | il diritto di farci rettificare o cancellare tali dati; |
| Paragraphe 4 | il diritto di rifiutare o limitare il trattamento dei vostri dati personali da parte nostra. |
| Paragraphe 5 | Se il trattamento da noi effettuato si basa sul vostro consenso, potete revocarlo in qualsiasi momento, senza indicarne il motivo, inviando una richiesta scritta all’indirizzo indicato sopra. Vi preghiamo di notare che non possiamo dare seguito a tali richieste prima di aver ottenuto una prova della vostra identità. |
| Intertitre | 2. Raccolta di dati generali |
| Paragraphe 6 | Ogni volta che consultate le nostre pagine web, raccogliamo una serie di dati generali. Tali dati e informazioni generali sono registrati nei file di log del server. Vengono raccolti i dati seguenti: |
| Paragraphe 7 | Indirizzo IP |
| Paragraphe 8 | Data e ora della richiesta |
| Paragraphe 9 | Differenza di fuso orario rispetto al fuso GMT |
| Paragraphe 10 | Contenuto della richiesta |
| Paragraphe 11 | Codice di stato HTTP/stato di accesso |
| Paragraphe 12 | Quantità di dati trasmessi |
| Paragraphe 13 | Pagina web da cui è stata inviata la richiesta |
| Paragraphe 14 | Browser (inclusi lingua e versione) |
| Paragraphe 15 | Sistema operativo |
| Paragraphe 16 | I dati generali raccolti non sono attribuiti a una persona identificata. Abbiamo bisogno di raccogliere tali dati per ragioni tecniche, al fine di rendere disponibile il nostro sito web in modo stabile e sicuro. |
| Intertitre | 3. Modulo di contatto |
| Paragraphe 17 | Quando utilizzate il modulo di contatto per inviarci una richiesta, i dati che inserite nel modulo, compresi i vostri recapiti, vengono da noi registrati al fine di trattare la vostra richiesta. Il trattamento di tali informazioni è disciplinato dalla nostra informativa sulla protezione dei dati, di cui potete ricevere una copia su richiesta e il cui link figura in ogni offerta che allestiamo per voi. Non trasmettiamo tali dati a terzi senza il vostro consenso. |
| Paragraphe 18 | Le informazioni inserite nel modulo di contatto sono conservate solo finché servono allo scopo previsto. Nei casi in cui la conservazione dipende esclusivamente dal vostro consenso, cancelliamo le informazioni non appena revocate tale consenso, a meno che la legge non imponga un periodo di conservazione più lungo. |
| Intertitre | 4. Cookie |
| Paragraphe 19 | Il nostro sito web utilizza cookie, ossia piccoli file di testo che vengono salvati sul vostro computer e contengono informazioni consultabili sul vostro comportamento di navigazione. I cookie servono a stabilire la vostra connessione ai nostri servizi web e a personalizzare la vostra esperienza di navigazione. I cookie raccolgono informazioni sul vostro indirizzo IP, sulla data e l’ora della vostra visita, sul numero di visite, sui moduli utilizzati, sui vostri parametri di ricerca, sulle pagine visualizzate e sulle vostre impostazioni preferite sul nostro sito web. |
| Paragraphe 20 | La maggior parte dei cookie che utilizziamo sono «cookie di sessione», che vengono cancellati automaticamente alla fine di ogni visita. Altri cookie restano memorizzati sul vostro computer finché non li cancellate. Potete configurare il vostro browser in modo da impedire al nostro sito web di installare cookie o da disattivare i cookie in generale. Potete inoltre, in qualsiasi momento, impostare il vostro browser in modo che cancelli tutti i cookie già installati. In tal caso, le vostre impostazioni potrebbero impedire il corretto funzionamento del nostro sito web. |
| Intertitre | 5. Web tracking |
| Paragraphe 21 | Il nostro sito web utilizza strumenti di web tracking per individuare i problemi che gli utenti possono incontrare e migliorare l’esperienza d’uso. |
| Paragraphe 22 | Google Analytics è un servizio di analisi web di Google Inc., 1600 Amphitheatre Parkway, Mountain View, CA 94043, U.S.A. (di seguito «Google»). Google Analytics utilizza cookie che consentono di analizzare l’utilizzo del nostro sito web. Le informazioni generate dai cookie sono trasmesse in forma anonimizzata a un server di Google negli Stati Uniti, dove vengono memorizzate. Grazie al processo di anonimizzazione, è impossibile collegare tali dati alla persona interessata. Google utilizza tali informazioni per analizzare il vostro utilizzo del nostro sito web, elaborare rapporti sulle attività degli utenti e fornire altri servizi connessi all’utilizzo del nostro sito web e di Internet in generale. Se richiesto dal diritto svizzero o estero, Google o terzi che trattano tali dati per suo conto possono comunicare tali informazioni a terzi. |
| Paragraphe 23 | Potete impedire a Google di registrare e trattare le informazioni generate dai cookie sul vostro utilizzo del nostro sito web installando il «Google Analytics Opt-out Browser Add-on», disponibile qui: https://tools.google.com/dlpage/gaoptout?hl=en. |
| Paragraphe 24 | Google è certificata Privacy Shield e garantisce pertanto il rispetto delle leggi europee sulla protezione dei dati (https://www.privacyshield.gov/participant?id=a2zt000000001L5AAI&status=Active). Per maggiori informazioni sul trattamento dei dati da parte di Google, consultate l’informativa sulla privacy di Google: https://policies.google.com/privacy?hl=en. |
| Paragraphe 25 | Lucky Orange è uno strumento di analisi offerto da Lucky Orange LLC, 8665 W 96th St Suite #100, Overland Park, KS 66212, USA (di seguito «Lucky Orange»). Lucky Orange raccoglie informazioni relative al traffico sul nostro sito web, quali le pagine visitate, i movimenti del mouse e i clic del visitatore, i dati di digitazione e i dati HTML di una pagina visitata da un visitatore, qualora tali dati HTML contengano informazioni personali. |
| Paragraphe 26 | Potete impedire a Lucky Orange di tracciare il vostro comportamento attivando la funzione «Do not track» del vostro browser. |
| Paragraphe 27 | Per maggiori informazioni sul trattamento dei dati da parte di Lucky Orange, consultate la dichiarazione sulla privacy (https://www.luckyorange.com/legal/privacy) e le condizioni di servizio (https://www.luckyorange.com/legal/terms) di Lucky Orange. |
| Paragraphe 28 | Versione di febbraio 2023 |

## FR · textes rédigés pour la maquette

À faire relire par un traducteur expert. Ils suivent la typographie du site source (pas d'espace avant le
deux-points ni avant le point d'interrogation).

| Emplacement | Texte |
|---|---|
| `<meta name="description">` (fr/index.html) | Commandez en ligne une traduction certifiée d’extraits du registre du commerce suisse: certification standard, notariée ou apostillée selon la Convention de La Haye, terminologie juridique rigoureuse, + 30 langues. Dès CHF 99.- |
| `aria-label` du formulaire de recherche | Recherche d’entreprise |
| `aria-label` du sélecteur de langue | Langue |
| `aria-label` du menu de langue compact | Langue: français |
| `aria-label` des liens légaux du pied de page | Informations légales |
| `aria-label` de l'illustration du héro | Illustration: un extrait du registre du commerce allemand et sa traduction française certifiée, avec un sceau et une apostille |
| `alt` du logo Corrext | Logo Corrext (le site source garde « Corrext logo » en anglais sur sa page FR) |

Pages légales FR : texte du site Neur.on repris tel quel, avec trois adaptations de maquette. La mention de
version passe en fin de page, comme dans les autres langues. Le lien « formulaire de contact », qui visait une
page du site Neur.on, est retiré (le texte reste). Les liens « Voir aussi » pointent vers la page sœur de la maquette.

## EN · textes rédigés pour la maquette (référence)

| Emplacement | Texte |
|---|---|
| `<meta name="description">` (en/index.html) | Order a certified translation of Swiss commercial register extracts online: standard, notarized or apostilled certification under the Hague Convention, accurate legal terminology, +30 languages. From CHF 99.- |
| `aria-label` du formulaire de recherche | Company search |
| `aria-label` du sélecteur de langue | Language |
| `aria-label` du menu de langue compact | Language: English |
| `aria-label` des liens légaux du pied de page | Legal |
| `aria-label` de l'illustration du héro | Illustration: a German commercial register extract and its certified French translation, with a seal and an apostille |
| Texte d'aide du champ, mode UID (choix du brief) | CHE-123.456.789 |

## Écarts volontaires avec le texte source (toutes langues)

- Bloc « Fully Digitized Process » : le tiret demi-cadratin de la source est remplacé par une virgule
  (règle du groupe : aucun tiret demi-cadratin ni cadratin).
- Pied de page : « © Neur.on AI Solutions SA », à la place de « © 2025 Neur.on. All rights reserved. ».
- Les mises en gras internes aux paragraphes de la source ne sont pas reprises (texte identique).

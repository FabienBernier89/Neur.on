# Table des adresses anglaises (EN)

Source de vérité : `docs-traduction/routes-en.json` (chemin FR → adresse EN), à fusionner dans `src/routes.json` avec les entrées IT. Ce fichier-ci n'en est que la version lisible.

Logique des slugs :

1. Chaque adresse EN suit la hiérarchie FR (`en/translation/` pour `fr/traduction/`, `en/help/` pour `fr/aide/`), à la même profondeur. Les noms de produits ne se traduisent pas (`en/corrext/`, `en/lexmachina/`, `chnell`).
2. Le slug porte la requête principale d'un lecteur international qui travaille avec la Suisse : avocat d'un cabinet international, juriste d'une multinationale établie en Suisse, banquier, contrepartie étrangère. D'où « commercial-register-extracts », « contracts », « law-firms », « annual-reports ».
3. Vocabulaire de la Confédération en anglais, pas celui du droit anglais ou américain : « commercial register » (et non « companies house »), « fiduciaries » (et non « trust »), « legal-departments ». Voir `docs-traduction/guide-en.md`, section 3.
4. Écriture : minuscules, mots séparés par des tirets, aucun accent, un à trois mots quand c'est possible. Orthographe britannique en « -ise » (`admin-organisation`), comme le veut le General Style Guide de la Chancellerie fédérale (§1).
5. Continuité avec l'ancien site anglais de neur-on.ai, servi à la racine : `en/about/`, `en/contact/`, `en/impressum/`, `en/privacy-policy/` reprennent les mots des anciennes adresses `/about/`, `/contact/`, `/impressum/`, `/privacy-policy/`.
6. Le glossaire garde ses slugs FR, déjà allemands (mots-vedettes) ; les actualités prennent un slug court tiré de l'événement (nom, lieu, année), comme en DE.

Les requêtes visées sont des hypothèses de rédaction, **non mesurées** : à confronter aux volumes réels (Google Ads Keyword Planner, Search Console, marché « anglais, Suisse » et « anglais, monde ») avant de figer les titres. Une adresse EN ne change plus une fois publiée.

Total : 156 pages FR, 156 adresses EN, aucune en double, aucune identique à une adresse FR ou DE, aucune identique à une ancienne adresse de `src/data/redirections.json` (contrôle par script le 2 octobre 2026).

## Slugs discutables

| Adresse EN | Pourquoi elle se discute | Alternative |
|---|---|---|
| `/en/security/` | Court et parallèle au DE (`/de/sicherheit/`), mais la page vend la souveraineté des données, pas la sécurité informatique en général. | `/en/data-sovereignty/` |
| `/en/corrext/review-editor/` | La page décrit l'outil de TAO intégré (bouton « Open in CAT »). « review editor » parle au juriste, « CAT tool » au traducteur. | `/en/corrext/cat-tool/` |
| `/en/solutions/fiduciaries/` | La « fiduciaire » suisse (Treuhand) n'a pas d'équivalent anglais exact. Le Legal Style Guide (§3.5, Trust / trustee) interdit « trust » et recommande « fiduciary ». Un lecteur étranger cherchera plutôt « accounting firm » ou « audit firm ». | `/en/solutions/fiduciary-and-audit-firms/` |
| `/en/solutions/banks/` | Parallèle au DE ; le FR dit « banques-finance ». La page domaine correspondante s'appelle `/en/translation/banking-and-finance/`. | `/en/solutions/banking-and-finance/` |
| `/en/help/admin-organisation/` | Orthographe britannique imposée par le guide fédéral, alors que l'interface Corrext peut afficher « Organization » (à relever). | `/en/help/admin-organization/` |
| `/en/comparison/` | Le hub vise « DeepL alternative » ; « compare » est plus court mais moins courant comme rubrique. | `/en/compare/` |
| `/en/resources/studies/` | Le FR dit « études et benchmarks ». | `/en/resources/benchmarks/` |
| `/en/resources/guides/law-firm-translation-workflow/` | Évite « organise / organize » dans l'adresse ; la requête reste « how to organise translation in a law firm ». | `/en/resources/guides/organising-translation-in-a-law-firm/` |
| `/en/impressum/` | Mot allemand. Le General Style Guide (§20) traduit « Impressum » par « Publication details ». Gardé pour la continuité avec l'ancienne page anglaise `/impressum/`, dont le texte d'origine s'intitule « Impressum & Terms of Use ». | `/en/legal-notice/` |
| `/en/resources/blog/canton-of-fribourg-support/` | « État de Fribourg » rendu par « Canton of Fribourg » (General Style Guide §4 : majuscule à « Canton » pour le gouvernement cantonal). Le site fr.ch n'a pas de version anglaise. | `/en/resources/blog/state-of-fribourg-support/` |
| `/en/resources/blog/ejustice-40-years-fireside-chat/` | « Kamingespräch » traduit par « fireside chat » dans l'adresse ; la requête garde le nom allemand de l'événement. | `/en/resources/blog/ejustice-40-years-kamingespraech/` |
| `/en/translation/tax-law/` | « tax » seul serait plus court ; « tax law » distingue la page juridique d'une offre fiscale. | `/en/translation/tax/` |

## Accueil et produit (12)

| Page | Adresse FR | Adresse EN | Requête visée |
|---|---|---|---|
| Neur.on : traduction juridique et financière par IA en Suisse | `/fr/` | `/en/` | legal translation Switzerland |
| Corrext : plateforme de traduction juridique suisse | `/fr/corrext/` | `/en/corrext/` | legal translation platform Switzerland |
| Traduction de texte et de documents juridiques · Corrext | `/fr/corrext/traduction-texte-et-document/` | `/en/corrext/document-translation/` | translate legal documents keep formatting |
| Gestion de projet : relecture juridique et devis | `/fr/corrext/gestion-de-projet/` | `/en/corrext/translation-projects/` | legal translation quote with human review |
| Éditeur de relecture Corrext : outil de TAO juridique suisse | `/fr/corrext/editeur-de-relecture/` | `/en/corrext/review-editor/` | legal translation review tool (CAT) |
| Fast lookup CHnell : concordancier du droit suisse | `/fr/corrext/chnell/` | `/en/corrext/chnell/` | Swiss legal terminology concordance |
| Extraits du registre du commerce traduits et certifiés | `/fr/corrext/extraits-registre-commerce/` | `/en/corrext/commercial-register-extracts/` | Swiss commercial register extract translation |
| API et on-premises · Corrext par Neur.on : intégrations | `/fr/corrext/api-on-premises/` | `/en/corrext/api-on-premises/` | legal translation API on-premises |
| LexMachina : le moteur de Corrext entraîné sur le droit suisse | `/fr/lexmachina/` | `/en/lexmachina/` | machine translation for Swiss law |
| Langues et formats de Corrext par Neur.on : les 30 langues | `/fr/langues-et-formats/` | `/en/languages-and-formats/` | translate PDF keep layout |
| Quatre niveaux de qualité de traduction · Corrext par Neur.on | `/fr/niveaux-de-qualite/` | `/en/quality-levels/` | post-editing legal translation |
| Sécurité et souveraineté des données suisses | `/fr/securite-souverainete/` | `/en/security/` | Swiss data sovereignty translation |

## Comparatifs (4)

| Page | Adresse FR | Adresse EN | Requête visée |
|---|---|---|---|
| Comparatifs · Corrext par Neur.on face aux autres solutions | `/fr/comparatif/` | `/en/comparison/` | DeepL alternative for lawyers |
| Agence de traduction ou plateforme : le choix avec Corrext | `/fr/comparatif/agence-ou-plateforme/` | `/en/comparison/translation-agency-or-platform/` | translation agency vs translation software |
| ChatGPT et traduction juridique : ce que Corrext apporte | `/fr/comparatif/chatgpt-traduction-juridique/` | `/en/comparison/chatgpt-legal-translation/` | ChatGPT legal translation |
| DeepL Pro et traduction juridique : ce que Corrext change | `/fr/comparatif/deepl-traduction-juridique/` | `/en/comparison/deepl-legal-translation/` | DeepL legal translation |

## Solutions par métier (7)

| Page | Adresse FR | Adresse EN | Requête visée |
|---|---|---|---|
| Solutions par métier · Neur.on, traduction juridique suisse | `/fr/solutions/` | `/en/solutions/` | translation for lawyers and banks |
| Traduction juridique pour cabinets d'avocats suisses | `/fr/solutions/cabinets-avocats/` | `/en/solutions/law-firms/` | translation for law firms Switzerland |
| Traduction juridique et financière pour banques | `/fr/solutions/banques-finance/` | `/en/solutions/banks/` | financial translation for banks Switzerland |
| Traduction pour directions juridiques et Legal Ops | `/fr/solutions/directions-juridiques/` | `/en/solutions/legal-departments/` | translation for in-house legal teams |
| Traduction pour autorités et administrations suisses | `/fr/solutions/autorites-administration/` | `/en/solutions/public-authorities/` | translation for public authorities Switzerland |
| Traduction pour fiduciaires, audit et conseil | `/fr/solutions/fiduciaires-conseil/` | `/en/solutions/fiduciaries/` | translation for fiduciary and audit firms |
| Traduction juridique pour LegalTechs et éditeurs | `/fr/solutions/editeurs-legaltech/` | `/en/solutions/legaltech-publishers/` | legal translation API for LegalTech |

## Domaines du droit (13)

| Page | Adresse FR | Adresse EN | Requête visée |
|---|---|---|---|
| Traduction juridique par domaine et par langue | `/fr/traduction/` | `/en/translation/` | Swiss legal translation by area of law |
| Traduction juridique de contrats suisses, DE FR IT | `/fr/traduction/contrats/` | `/en/translation/contracts/` | contract translation Swiss law |
| Traduction en droit des sociétés suisse, DE FR IT | `/fr/traduction/droit-des-societes/` | `/en/translation/corporate-law/` | articles of association translation |
| Traduction pour fusions et acquisitions en Suisse | `/fr/traduction/fusions-acquisitions/` | `/en/translation/mergers-and-acquisitions/` | M&A translation Switzerland |
| Traduction juridique pour contentieux et arbitrage | `/fr/traduction/contentieux-arbitrage/` | `/en/translation/litigation-and-arbitration/` | arbitration translation Switzerland |
| Traduction juridique et financière pour les banques | `/fr/traduction/banque-finance/` | `/en/translation/banking-and-finance/` | financial translation Switzerland |
| Traduction réglementaire, compliance et FINMA | `/fr/traduction/compliance-finma/` | `/en/translation/compliance-finma/` | FINMA circular translation |
| Traduction des rapports annuels et comptes suisses | `/fr/traduction/rapports-annuels-financiers/` | `/en/translation/annual-reports/` | annual report translation Switzerland |
| Traduction juridique et fiscale en droit suisse | `/fr/traduction/fiscalite/` | `/en/translation/tax-law/` | Swiss tax translation |
| Traduction juridique pour l'assurance en Suisse | `/fr/traduction/assurance/` | `/en/translation/insurance/` | insurance translation Switzerland |
| Traduction de brevets, marques et droit d'auteur | `/fr/traduction/propriete-intellectuelle/` | `/en/translation/intellectual-property/` | patent translation Switzerland |
| Traduction juridique en droit du travail suisse | `/fr/traduction/droit-du-travail/` | `/en/translation/employment-law/` | employment contract translation Switzerland |
| Traduction en droit pénal et procédure pénale suisse | `/fr/traduction/droit-penal/` | `/en/translation/criminal-law/` | criminal law translation Switzerland |

## Paires de langues (6)

| Page | Adresse FR | Adresse EN | Requête visée |
|---|---|---|---|
| Traduction juridique de l'allemand au français | `/fr/traduction/allemand-francais/` | `/en/translation/german-french/` | German to French legal translation |
| Traduction juridique du français vers l'allemand | `/fr/traduction/francais-allemand/` | `/en/translation/french-german/` | French to German legal translation |
| Traduction juridique de l'allemand vers l'anglais | `/fr/traduction/allemand-anglais/` | `/en/translation/german-english/` | German to English legal translation |
| Traduction juridique de l'anglais vers l'allemand | `/fr/traduction/anglais-allemand/` | `/en/translation/english-german/` | English to German contract translation |
| Traduction juridique du français vers l'anglais | `/fr/traduction/francais-anglais/` | `/en/translation/french-english/` | French to English legal translation |
| Traduction juridique de l'italien au français | `/fr/traduction/italien-francais/` | `/en/translation/italian-french/` | Italian to French legal translation |

## Glossaire (53)

| Page | Adresse FR | Adresse EN | Requête visée |
|---|---|---|---|
| Glossaire juridique suisse en quatre langues | `/fr/ressources/glossaire/` | `/en/resources/glossary/` | Swiss legal glossary German English |
| Abtretung : la cession de créance en droit suisse | `/fr/ressources/glossaire/abtretung/` | `/en/resources/glossary/abtretung/` | Abtretung in English |
| Aktiengesellschaft : la société anonyme suisse | `/fr/ressources/glossaire/aktiengesellschaft/` | `/en/resources/glossary/aktiengesellschaft/` | Aktiengesellschaft in English |
| Aktienkapital : le capital-actions | `/fr/ressources/glossaire/aktienkapital/` | `/en/resources/glossary/aktienkapital/` | Aktienkapital in English |
| Arbeitsvertrag : le contrat de travail suisse | `/fr/ressources/glossaire/arbeitsvertrag/` | `/en/resources/glossary/arbeitsvertrag/` | Arbeitsvertrag in English |
| Arrest : le séquestre en droit suisse des poursuites | `/fr/ressources/glossaire/arrest/` | `/en/resources/glossary/arrest/` | Arrest in English |
| Bankgeheimnis : le secret bancaire en droit suisse | `/fr/ressources/glossaire/bankgeheimnis/` | `/en/resources/glossary/bankgeheimnis/` | Bankgeheimnis in English |
| Beschwerde : le recours devant le Tribunal fédéral | `/fr/ressources/glossaire/beschwerde/` | `/en/resources/glossary/beschwerde/` | Beschwerde in English |
| Betreibung : la poursuite pour dettes en Suisse | `/fr/ressources/glossaire/betreibung/` | `/en/resources/glossary/betreibung/` | Betreibung in English |
| Bürgschaft : le cautionnement en droit suisse | `/fr/ressources/glossaire/buergschaft/` | `/en/resources/glossary/buergschaft/` | Bürgschaft in English |
| Bundesgericht : le Tribunal fédéral suisse | `/fr/ressources/glossaire/bundesgericht/` | `/en/resources/glossary/bundesgericht/` | Bundesgericht in English |
| fristlose Kündigung : la résiliation immédiate | `/fr/ressources/glossaire/fristlose-kuendigung/` | `/en/resources/glossary/fristlose-kuendigung/` | fristlose Kündigung in English |
| Geldwäscherei : le blanchiment d'argent en Suisse | `/fr/ressources/glossaire/geldwaescherei/` | `/en/resources/glossary/geldwaescherei/` | Geldwäscherei in English |
| Generalversammlung : l'assemblée générale en Suisse | `/fr/ressources/glossaire/generalversammlung/` | `/en/resources/glossary/generalversammlung/` | Generalversammlung in English |
| Gewährleistung : la garantie des défauts | `/fr/ressources/glossaire/gewaehrleistung/` | `/en/resources/glossary/gewaehrleistung/` | Gewährleistung in English |
| GmbH : la société à responsabilité limitée | `/fr/ressources/glossaire/gmbh/` | `/en/resources/glossary/gmbh/` | Gesellschaft mit beschränkter Haftung in English |
| Grundbuch : le registre foncier suisse | `/fr/ressources/glossaire/grundbuch/` | `/en/resources/glossary/grundbuch/` | Grundbuch in English |
| Handelsregister : le registre du commerce suisse | `/fr/ressources/glossaire/handelsregister/` | `/en/resources/glossary/handelsregister/` | Handelsregister in English |
| Konkurrenzverbot : la clause de non-concurrence | `/fr/ressources/glossaire/konkurrenzverbot/` | `/en/resources/glossary/konkurrenzverbot/` | Konkurrenzverbot in English |
| Konkurs : la faillite et la masse en droit suisse | `/fr/ressources/glossaire/konkurs/` | `/en/resources/glossary/konkurs/` | Konkurs in English |
| Konventionalstrafe : la clause pénale | `/fr/ressources/glossaire/konventionalstrafe/` | `/en/resources/glossary/konventionalstrafe/` | Konventionalstrafe in English |
| Kündigung : la résiliation du contrat de travail | `/fr/ressources/glossaire/kuendigung/` | `/en/resources/glossary/kuendigung/` | Kündigung in English |
| Mängelrüge : l'avis des défauts en droit suisse | `/fr/ressources/glossaire/maengelruege/` | `/en/resources/glossary/maengelruege/` | Mängelrüge in English |
| Mehrwertsteuer : la TVA suisse en quatre langues | `/fr/ressources/glossaire/mehrwertsteuer/` | `/en/resources/glossary/mehrwertsteuer/` | Mehrwertsteuer in English |
| Mietvertrag : le bail à loyer en droit suisse | `/fr/ressources/glossaire/mietvertrag/` | `/en/resources/glossary/mietvertrag/` | Mietvertrag in English |
| Nachlassstundung : le sursis concordataire | `/fr/ressources/glossaire/nachlassstundung/` | `/en/resources/glossary/nachlassstundung/` | Nachlassstundung in English |
| Personendaten : les données personnelles en Suisse | `/fr/ressources/glossaire/personendaten/` | `/en/resources/glossary/personendaten/` | Personendaten in English |
| Pflichtteil : la réserve héréditaire suisse | `/fr/ressources/glossaire/pflichtteil/` | `/en/resources/glossary/pflichtteil/` | Pflichtteil in English |
| Prospekt : le prospectus des marchés financiers | `/fr/ressources/glossaire/prospekt/` | `/en/resources/glossary/prospekt/` | Prospekt in English |
| Quellensteuer : l'impôt à la source suisse | `/fr/ressources/glossaire/quellensteuer/` | `/en/resources/glossary/quellensteuer/` | Quellensteuer in English |
| Rechtsöffnung : la mainlevée de l'opposition | `/fr/ressources/glossaire/rechtsoeffnung/` | `/en/resources/glossary/rechtsoeffnung/` | Rechtsöffnung in English |
| Rechtsvorschlag : l'opposition en poursuite suisse | `/fr/ressources/glossaire/rechtsvorschlag/` | `/en/resources/glossary/rechtsvorschlag/` | Rechtsvorschlag in English |
| Revisionsstelle : l'organe de révision en Suisse | `/fr/ressources/glossaire/revisionsstelle/` | `/en/resources/glossary/revisionsstelle/` | Revisionsstelle in English |
| Schadenersatz : les dommages-intérêts en Suisse | `/fr/ressources/glossaire/schadenersatz/` | `/en/resources/glossary/schadenersatz/` | Schadenersatz in English |
| Schiedsgericht : le tribunal arbitral en Suisse | `/fr/ressources/glossaire/schiedsgericht/` | `/en/resources/glossary/schiedsgericht/` | Schiedsgericht in English |
| Schuldnerverzug : la demeure du débiteur | `/fr/ressources/glossaire/schuldnerverzug/` | `/en/resources/glossary/schuldnerverzug/` | Schuldnerverzug in English |
| Sorgfaltspflichten : les obligations de diligence | `/fr/ressources/glossaire/sorgfaltspflichten/` | `/en/resources/glossary/sorgfaltspflichten/` | Sorgfaltspflichten in English |
| Statuten : les statuts d'une société suisse | `/fr/ressources/glossaire/statuten/` | `/en/resources/glossary/statuten/` | Statuten in English |
| Steuerhinterziehung : la soustraction d'impôt | `/fr/ressources/glossaire/steuerhinterziehung/` | `/en/resources/glossary/steuerhinterziehung/` | Steuerhinterziehung in English |
| Strafbefehl : l'ordonnance pénale en droit suisse | `/fr/ressources/glossaire/strafbefehl/` | `/en/resources/glossary/strafbefehl/` | Strafbefehl in English |
| Überstunden : les heures supplémentaires en Suisse | `/fr/ressources/glossaire/ueberstunden/` | `/en/resources/glossary/ueberstunden/` | Überstunden in English |
| Untersuchungshaft : la détention provisoire suisse | `/fr/ressources/glossaire/untersuchungshaft/` | `/en/resources/glossary/untersuchungshaft/` | Untersuchungshaft in English |
| Verfügung : la décision administrative suisse | `/fr/ressources/glossaire/verfuegung/` | `/en/resources/glossary/verfuegung/` | Verfügung in English |
| Verjährung : la prescription des créances en Suisse | `/fr/ressources/glossaire/verjaehrung/` | `/en/resources/glossary/verjaehrung/` | Verjährung in English |
| Verrechnungssteuer : l'impôt anticipé en Suisse | `/fr/ressources/glossaire/verrechnungssteuer/` | `/en/resources/glossary/verrechnungssteuer/` | Verrechnungssteuer in English |
| Versicherungsvertrag : le contrat d'assurance suisse | `/fr/ressources/glossaire/versicherungsvertrag/` | `/en/resources/glossary/versicherungsvertrag/` | Versicherungsvertrag in English |
| Verwaltungsrat : le conseil d'administration suisse | `/fr/ressources/glossaire/verwaltungsrat/` | `/en/resources/glossary/verwaltungsrat/` | Verwaltungsrat in English |
| Verzugszins : intérêt moratoire en droit suisse | `/fr/ressources/glossaire/verzugszins/` | `/en/resources/glossary/verzugszins/` | Verzugszins in English |
| Vollmacht : pouvoirs et procuration | `/fr/ressources/glossaire/vollmacht/` | `/en/resources/glossary/vollmacht/` | Vollmacht in English |
| vorsorgliche Massnahmen : mesures provisionnelles | `/fr/ressources/glossaire/vorsorgliche-massnahmen/` | `/en/resources/glossary/vorsorgliche-massnahmen/` | vorsorgliche Massnahmen in English |
| Willensvollstrecker : l'exécuteur testamentaire | `/fr/ressources/glossaire/willensvollstrecker/` | `/en/resources/glossary/willensvollstrecker/` | Willensvollstrecker in English |
| Ayant droit économique : la notion de la LBA | `/fr/ressources/glossaire/wirtschaftlich-berechtigte-person/` | `/en/resources/glossary/wirtschaftlich-berechtigte-person/` | wirtschaftlich berechtigte Person in English |
| Zahlungsbefehl : le commandement de payer suisse | `/fr/ressources/glossaire/zahlungsbefehl/` | `/en/resources/glossary/zahlungsbefehl/` | Zahlungsbefehl in English |

## Centre d'aide (14)

| Page | Adresse FR | Adresse EN | Requête visée |
|---|---|---|---|
| Centre d'aide Corrext | `/fr/aide/` | `/en/help/` | Corrext help |
| Premiers pas dans Corrext : se connecter et traduire | `/fr/aide/premiers-pas/` | `/en/help/getting-started/` | Corrext login getting started |
| Découvrir Corrext · Centre d'aide | `/fr/aide/decouvrir-corrext/` | `/en/help/corrext-overview/` | Corrext features |
| Traduction texte et document dans Corrext | `/fr/aide/traduction-texte-et-document/` | `/en/help/document-translation/` | Corrext translate a file |
| Gestion de projet : relecture et devis Corrext | `/fr/aide/gestion-de-projet/` | `/en/help/translation-projects/` | Corrext order review quote |
| Éditeur de relecture · Centre d'aide | `/fr/aide/editeur-de-relecture/` | `/en/help/review-editor/` | Corrext revise a translation |
| Fast lookup CHnell : chercher un terme en contexte | `/fr/aide/chnell/` | `/en/help/chnell/` | Fast lookup CHnell search a term |
| Traduction certifiée d'extraits du registre suisse | `/fr/aide/extraits-registre/` | `/en/help/commercial-register-extracts/` | order certified translation of commercial register extract |
| Formats de fichiers et langues acceptés par Corrext | `/fr/aide/formats-et-langues/` | `/en/help/formats-and-languages/` | Corrext file formats languages |
| Sécurité, confidentialité et compte · Centre d'aide | `/fr/aide/securite-et-confidentialite/` | `/en/help/security-and-privacy/` | Corrext data privacy account |
| Dépannage Corrext : bouton grisé, langue, fichier | `/fr/aide/depannage/` | `/en/help/troubleshooting/` | Corrext troubleshooting |
| Organisation, membres et rôles · Centre d'aide | `/fr/aide/admin-organisation/` | `/en/help/admin-organisation/` | Corrext manage users and roles |
| Moteurs et confidentialité · Centre d'aide | `/fr/aide/admin-moteurs/` | `/en/help/admin-engines/` | Corrext allowed translation engines |
| Mémoires et terminologie · Centre d'aide | `/fr/aide/admin-memoires/` | `/en/help/admin-translation-memories/` | Corrext translation memory terminology import |

## Ressources, guides et études (6)

| Page | Adresse FR | Adresse EN | Requête visée |
|---|---|---|---|
| Ressources sur la traduction juridique suisse | `/fr/ressources/` | `/en/resources/` | Swiss legal translation guide |
| Guides pratiques de la traduction juridique suisse | `/fr/ressources/guides/` | `/en/resources/guides/` | legal translation guide |
| Organiser la traduction juridique dans un cabinet | `/fr/ressources/guides/organiser-traduction-cabinet/` | `/en/resources/guides/law-firm-translation-workflow/` | how to organise translation in a law firm |
| Préparer un rapport annuel multilingue en Suisse | `/fr/ressources/guides/rapport-annuel-multilingue/` | `/en/resources/guides/multilingual-annual-report/` | multilingual annual report Switzerland |
| Études et benchmarks sur la traduction juridique | `/fr/ressources/etudes/` | `/en/resources/studies/` | legal machine translation benchmark |
| Évaluer un moteur de traduction sur le droit suisse | `/fr/ressources/etudes/evaluer-moteur-traduction-juridique/` | `/en/resources/studies/evaluating-translation-engines/` | how to evaluate machine translation |

## Blog : articles (4)

| Page | Adresse FR | Adresse EN | Requête visée |
|---|---|---|---|
| Blog Neur.on : droit suisse, traduction et actualités | `/fr/ressources/blog/` | `/en/resources/blog/` | Swiss legal translation blog |
| Traduire un contrat en droit suisse quadrilingue | `/fr/ressources/blog/traduire-contrat-droit-suisse/` | `/en/resources/blog/translating-contracts-swiss-law/` | translate a contract under Swiss law |
| Comprendre un devis de traduction juridique suisse | `/fr/ressources/blog/comprendre-devis-traduction-juridique/` | `/en/resources/blog/legal-translation-quotes/` | legal translation quote cost |
| Secret professionnel et outils de traduction IA | `/fr/ressources/blog/secret-professionnel-outils-traduction/` | `/en/resources/blog/professional-secrecy-ai-translation/` | professional secrecy AI translation |

## Blog : actualités (32)

| Page | Adresse FR | Adresse EN | Requête visée |
|---|---|---|---|
| Actualités de Neur.on depuis 2020 | `/fr/ressources/blog/actualites/` | `/en/resources/blog/news/` | Neur.on news |
| Paula Reichenberg à l’EPFL Investor Day 2024 | `/fr/ressources/blog/paula-reichenberg-pitch-epfl-investor-day-2024/` | `/en/resources/blog/epfl-investor-day-2024/` | EPFL Investor Day 2024 |
| Swisscom et Neur.on annoncent une collaboration | `/fr/ressources/blog/neuron-swisscom-collaboration-kickstart-2024/` | `/en/resources/blog/swisscom-collaboration-2024/` | Swisscom Neur.on collaboration |
| Neur.on au Startups Showcase du TLTF Summit 2024 | `/fr/ressources/blog/neuron-tltf-summit-2024-miami-startups-showcase/` | `/en/resources/blog/tltf-summit-2024-miami/` | TLTF Summit 2024 Startups Showcase |
| LegalTechTalk 2024 à Londres : enseignements clés | `/fr/ressources/blog/legaltechtalk-2024-londres-enseignements/` | `/en/resources/blog/legaltechtalk-2024-key-takeaways/` | LegalTechTalk 2024 London |
| L’IA dans le secteur juridique : table ronde SLTA | `/fr/ressources/blog/table-ronde-ia-juridique-slta-zurich-2024/` | `/en/resources/blog/slta-panel-zurich-2024/` | SLTA panel AI legal Zurich |
| Kilian Marty rejoint le conseil consultatif | `/fr/ressources/blog/kilian-marty-rejoint-conseil-consultatif-neuron/` | `/en/resources/blog/kilian-marty-advisory-board/` | Kilian Marty cybersecurity |
| Les start-up doivent-elles craindre l’AI Act ? | `/fr/ressources/blog/ai-act-grand-challenge-universite-saint-gall/` | `/en/resources/blog/ai-act-grand-challenge-st-gallen/` | AI Act start-ups St Gallen |
| PwC et The LegalTech Fund : pitch à Londres | `/fr/ressources/blog/paula-reichenberg-pwc-legaltech-fund-londres/` | `/en/resources/blog/pwc-legaltech-fund-london/` | PwC The LegalTech Fund London |
| AI Days 2025 Genève : entraîner un LLM à traduire | `/fr/ressources/blog/neuron-ai-days-2025-geneve-llm-traduction/` | `/en/resources/blog/ai-days-2025-geneva/` | AI Days 2025 Geneva |
| eJustice.ch, 40 ans : premier Kamingespräch | `/fr/ressources/blog/ejustice-40-ans-kamingesprach-neuron/` | `/en/resources/blog/ejustice-40-years-fireside-chat/` | eJustice.ch Kamingespräch Swiss Justice Base Model |
| IA et études d’avocats : panel AI in Business | `/fr/ressources/blog/panel-ai-in-business-zurich-2024/` | `/en/resources/blog/ai-in-business-zurich-2024/` | AI in Business Zurich law firms |
| GEN AI Summit 2024 Lausanne : IA et traduction | `/fr/ressources/blog/neuron-gen-ai-summit-2024-lausanne/` | `/en/resources/blog/gen-ai-summit-2024-lausanne/` | GEN AI Summit 2024 Lausanne |
| Swiss FinTech Awards 2024 : Neur.on parmi les 4 finalistes | `/fr/ressources/blog/neuron-quatre-finalistes-swiss-fintech-awards-2024/` | `/en/resources/blog/swiss-fintech-awards-2024-finalists/` | Swiss FinTech Awards 2024 finalists |
| Trust Valley Day : risques cyber et PME | `/fr/ressources/blog/trust-valley-day-2023-risques-cyber-pme/` | `/en/resources/blog/trust-valley-day-2023-cyber-risks/` | Trust Valley Day cyber risks SMEs |
| LegalTech et avocats : alliés ou concurrents ? | `/fr/ressources/blog/legaltech-avocats-allies-ou-concurrents/` | `/en/resources/blog/legaltech-and-lawyers/` | LegalTech and lawyers |
| Paula Reichenberg au Female Founder Project 2025 | `/fr/ressources/blog/paula-reichenberg-female-founder-project-ubs-2025/` | `/en/resources/blog/female-founder-project-ubs-2025/` | UBS Female Founder Project 2025 |
| GILW25 : Paula Reichenberg et l’IA rentable | `/fr/ressources/blog/paula-reichenberg-panel-gilw25-geneve-ia/` | `/en/resources/blog/gilw25-geneva-ai-panel/` | Geneva International Legal Week 2025 |
| Paula Reichenberg au Conseil stratégique HES-SO | `/fr/ressources/blog/paula-reichenberg-conseil-strategique-hes-so/` | `/en/resources/blog/hes-so-strategic-council/` | HES-SO strategic council |
| Kickstart Innovation 2024 : 42 scale-ups retenues | `/fr/ressources/blog/neuron-cohorte-kickstart-innovation-2024/` | `/en/resources/blog/kickstart-innovation-2024/` | Kickstart Innovation 2024 finance insurance |
| LegalTechTalk 2024 : réinventer les cabinets | `/fr/ressources/blog/legaltechtalk-2024-londres-modele-operationnel-cabinets/` | `/en/resources/blog/legaltechtalk-2024-law-firm-operating-model/` | law firm operating model LegalTech |
| AMLD EPFL 2024 : AI-Powered Projects à Lausanne | `/fr/ressources/blog/neuron-amld-epfl-2024-lausanne/` | `/en/resources/blog/amld-epfl-2024-lausanne/` | AMLD EPFL 2024 |
| Le parcours d’Orane Laeri sur orientation.ch | `/fr/ressources/blog/orane-laeri-parcours-orientation-ch/` | `/en/resources/blog/orane-laeri-career-path/` | Orane Laeri linguistics career |
| Soutien de l’État de Fribourg à la traduction IA | `/fr/ressources/blog/etat-fribourg-soutien-neuron-traduction-juridique-ia/` | `/en/resources/blog/canton-of-fribourg-support/` | Canton of Fribourg AI translation support |
| Schwyz : extraits du registre traduits par IA | `/fr/ressources/blog/registre-commerce-schwyz-traduction-ia-extraits-anglais/` | `/en/resources/blog/schwyz-commercial-register-english/` | Schwyz commercial register English extracts |
| Weblaw Forum 2024 : Paula Reichenberg au jury | `/fr/ressources/blog/paula-reichenberg-jury-weblaw-forum-2024/` | `/en/resources/blog/weblaw-forum-2024-jury/` | Weblaw Forum 2024 Elevator Pitch |
| Swiss FinTech Awards 2024 : finaliste Early Stage | `/fr/ressources/blog/neuron-finaliste-early-stage-swiss-fintech-awards-2024/` | `/en/resources/blog/swiss-fintech-awards-2024-early-stage/` | Swiss FinTech Awards 2024 Early Stage |
| Top 10 des Swiss FinTech Awards 2024 | `/fr/ressources/blog/neuron-top-10-startups-fintech-suisses-2024/` | `/en/resources/blog/swiss-fintech-awards-2024-top-10/` | Swiss FinTech Awards 2024 Top 10 |
| Souveraineté des données en Suisse : Trust Valley | `/fr/ressources/blog/cybersecurite-souverainete-donnees-pme-trust-valley/` | `/en/resources/blog/trust-valley-2023-data-sovereignty/` | data sovereignty SMEs Switzerland |
| Conférence MIDS 2023 à Genève : IA générative | `/fr/ressources/blog/paula-reichenberg-conference-mids-geneve-2023/` | `/en/resources/blog/mids-conference-geneva-2023/` | MIDS conference Geneva generative AI |
| Paula Reichenberg, Digital Shaper 2023 | `/fr/ressources/blog/paula-reichenberg-digital-shaper-2023-bilanz/` | `/en/resources/blog/digital-shaper-2023-bilanz/` | BILANZ Digital Shapers 2023 |
| Conférence BDÜ 2022 : avocats et traducteurs | `/fr/ressources/blog/paula-reichenberg-table-ronde-bdu-2022/` | `/en/resources/blog/bdue-conference-2022/` | BDÜ conference 2022 lawyers translators |

## Société et pages légales (5)

| Page | Adresse FR | Adresse EN | Requête visée |
|---|---|---|---|
| À propos de Neur.on · la société suisse derrière Corrext | `/fr/a-propos/` | `/en/about/` | Neur.on Fribourg LegalTech |
| Presse · Neur.on AI Solutions SA, LegalTech suisse à Fribourg | `/fr/a-propos/presse/` | `/en/about/press/` | Neur.on press |
| Contact et démo · Neur.on, traduction juridique en Suisse | `/fr/contact/` | `/en/contact/` | Corrext demo |
| Mentions légales et conditions d'utilisation | `/fr/mentions-legales/` | `/en/impressum/` | Neur.on impressum |
| Protection des données | `/fr/protection-des-donnees/` | `/en/privacy-policy/` | Neur.on privacy policy |

## Point d'attention : anciennes adresses anglaises

- Aucune ancienne adresse de `src/data/redirections.json` ne commence par `/en/`. Aucune adresse EN ne peut donc écrire un fichier au même endroit qu'une page de renvoi (le cas de `/de/impressum/` ne se reproduit pas).
- Les anciennes pages anglaises de neur-on.ai étaient servies à la racine. À la tâche 13, leur cible deviendra l'équivalent EN :

| Ancienne adresse | Cible EN |
|---|---|
| `/about/` | `/en/about/` |
| `/contact/`, `/schedule-a-demo/` | `/en/contact/` |
| `/news/` | `/en/resources/blog/news/` |
| `/impressum/` | `/en/impressum/` |
| `/terms-of-use/` | `/en/impressum/#conditions-d-utilisation` (identifiant de la source FR, conservé comme sur la page DE) |
| `/privacy-policy/` | `/en/privacy-policy/` |
| anciens billets anglais 2020-2021 (`/lexmachina-…`, `/discover-our-…`, etc.) | `/en/resources/blog/news/#actu-…` (même ancre que la cible FR) |

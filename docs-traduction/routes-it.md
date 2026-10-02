# Table des adresses italiennes (IT)

Version lisible de `docs-traduction/routes-it.json` (à fusionner dans `src/routes.json`, clé `it`). Lecteur visé : avocate ou avocat tessinois, banque ou fiduciaria à Lugano, giurista d'impresa, administration de la Suisse italienne.

Logique des slugs :

1. Chaque adresse IT suit la hiérarchie FR (`it/traduzione/` pour `fr/traduction/`, `it/aiuto/` pour `fr/aide/`, `it/risorse/` pour `fr/ressources/`), sans noms de produits traduits (`it/corrext/`, `it/lexmachina/`, `chnell`, `api-on-premises`).
2. Le slug porte la requête principale d'un lecteur de Suisse italienne : « estratto registro di commercio », « contratti », « studi legali », « rapporti annuali ».
3. Vocabulaire des textes fédéraux en italien et non de l'Italie : « registro di commercio » (art. 927 CO), « studio legale » (art. 5 LLCA), « fiduciaria » (loi tessinoise LFid), « preventivo » (art. 375 CO, FR « devis »), « Svitto », « Friburgo », « Losanna » (art. 1 Cost., art. 4 LTF).
4. Écriture : minuscules, accents retirés (« qualità » devient `qualita`, « proprietà » `proprieta`), apostrophe supprimée, mots séparés par des tirets. Les connecteurs suivent le FR : `lingue-e-formati` (FR `langues-et-formats`), `contenzioso-arbitrato` (FR `contentieux-arbitrage`). La préposition reste quand elle fait partie du terme officiel : `registro-di-commercio`, `diritto-del-lavoro`, `protezione-dei-dati`.
5. Les outils de Corrext et les rubriques du centre d'aide portent le même slug (`traduzione-documenti`, `progetti-di-traduzione`, `revisione`, `estratto-registro-di-commercio`), comme en DE.
6. Le glossaire garde ses slugs FR, qui sont déjà les mots-vedettes allemands ; les actualités prennent un slug court tiré de l'événement (nom, lieu en italien, année).

Les requêtes visées sont des hypothèses de rédaction, plausibles en Suisse italienne mais **non mesurées** : à confronter aux volumes réels (Google Ads Keyword Planner, région Tessin et Grisons italophones ; Search Console) avant de figer les titres. Une adresse IT ne change plus une fois publiée.

Total : 156 pages FR, 156 adresses IT, aucune en double (contrôle automatique : unicité, format `[a-z0-9-]`, parent IT = adresse IT du parent FR).

## Slugs discutables

| Adresse IT | Pourquoi on hésite | Alternative |
|---|---|---|
| `/it/soluzioni/uffici-legali/` | FR « directions juridiques ». « ufficio legale » est l'usage courant en entreprise ; l'administration dit « servizio giuridico ». Non vérifié dans un texte fédéral. | `servizi-giuridici` |
| `/it/soluzioni/enti-pubblici/` | FR « autorités et administrations ». `autorita` perd son accent et se lit mal ; « enti pubblici » couvre Confédération, Cantoni et Comuni. | `autorita`, `amministrazioni` |
| `/it/traduzione/diritto-tributario/` | FR « fiscalité ». La requête probable est « traduzione fiscale » ; `fiscalita` perd son accent. | `diritto-fiscale`, `fiscalita` |
| `/it/traduzione/rapporti-annuali/` | Le CO dit « relazione sulla gestione » (art. 958 CO) ; les sociétés publient un « rapporto annuale » ou un « rapporto di gestione », que les lecteurs cherchent. | `relazione-sulla-gestione` |
| `/it/corrext/revisione/`, `/it/aiuto/revisione/` | « revisione » est le terme du métier pour la relecture d'une traduction, mais en droit suisse il désigne aussi l'audit (« ufficio di revisione », art. 727 CO). Ambiguïté possible auprès des fiduciaires. | `rilettura` |
| `/it/risorse/blog/preventivo-traduzione-giuridica/` | « preventivo » est le mot du CO (art. 375, FR « devis ») ; le commerce suisse dit aussi « offerta ». | `offerta-traduzione-giuridica` |
| `/it/risorse/studi/` | FR « études ». « studi » se confond avec « studi legali ». | `ricerche`, `studi-e-benchmark` |
| `/it/aiuto/` | Court, comme `de/hilfe/`. Les sites suisses disent aussi « assistenza » ou « centro assistenza ». | `assistenza` |
| `/it/note-legali/` | Usage courant pour les mentions légales ; certains sites suisses gardent « impressum ». | `impressum` |
| `/it/risorse/blog/notizie/` | FR « actualités ». « attualita » perd son accent. | `attualita`, `news` |
| `/it/confronto/` | Singulier pour une rubrique de quatre comparatifs. | `confronti` |
| `/it/risorse/blog/ejustice-40-anni-kamingespraech/` | « Kamingespräch » est le nom allemand du format de l'événement, gardé comme en DE. | `ejustice-40-anni` |
| `/it/risorse/blog/cantone-friburgo-sostegno/` | FR « État de Fribourg » : la traduction italienne de la Constitution fribourgeoise écrit « Cantone di Friburgo » (RS 131.219, art. 1). | `stato-di-friburgo-sostegno` |
| `/it/corrext/estratto-registro-di-commercio/` | Long (30 caractères), mais il reprend mot pour mot la requête et le terme officiel. | `estratti-registro` |


## Accueil et produit (12)

| Page | Adresse FR | Adresse IT | Requête visée |
|---|---|---|---|
| Neur.on : traduction juridique et financière par IA en Suisse | `/fr/` | `/it/` | traduzione giuridica Svizzera |
| Corrext : plateforme de traduction juridique suisse | `/fr/corrext/` | `/it/corrext/` | piattaforma di traduzione giuridica Svizzera |
| Traduction de texte et de documents juridiques · Corrext | `/fr/corrext/traduction-texte-et-document/` | `/it/corrext/traduzione-documenti/` | tradurre documenti giuridici |
| Gestion de projet : relecture juridique et devis | `/fr/corrext/gestion-de-projet/` | `/it/corrext/progetti-di-traduzione/` | preventivo traduzione con revisione |
| Éditeur de relecture Corrext : outil de TAO juridique suisse | `/fr/corrext/editeur-de-relecture/` | `/it/corrext/revisione/` | revisione traduzione giuridica |
| Fast lookup CHnell : concordancier du droit suisse | `/fr/corrext/chnell/` | `/it/corrext/chnell/` | concordanziere terminologia giuridica svizzera |
| Extraits du registre du commerce traduits et certifiés | `/fr/corrext/extraits-registre-commerce/` | `/it/corrext/estratto-registro-di-commercio/` | traduzione estratto registro di commercio |
| API et on-premises · Corrext par Neur.on : intégrations | `/fr/corrext/api-on-premises/` | `/it/corrext/api-on-premises/` | API di traduzione on-premises |
| LexMachina : le moteur de Corrext entraîné sur le droit suisse | `/fr/lexmachina/` | `/it/lexmachina/` | traduzione automatica giuridica Svizzera |
| Langues et formats de Corrext par Neur.on : les 30 langues | `/fr/langues-et-formats/` | `/it/lingue-e-formati/` | tradurre PDF mantenendo il layout |
| Quatre niveaux de qualité de traduction · Corrext par Neur.on | `/fr/niveaux-de-qualite/` | `/it/livelli-di-qualita/` | post-editing traduzione giuridica |
| Sécurité et souveraineté des données suisses | `/fr/securite-souverainete/` | `/it/sicurezza/` | sovranità dei dati Svizzera traduzione |

## Comparatifs (4)

| Page | Adresse FR | Adresse IT | Requête visée |
|---|---|---|---|
| Comparatifs · Corrext par Neur.on face aux autres solutions | `/fr/comparatif/` | `/it/confronto/` | alternativa a DeepL Svizzera |
| Agence de traduction ou plateforme : le choix avec Corrext | `/fr/comparatif/agence-ou-plateforme/` | `/it/confronto/agenzia-o-piattaforma/` | agenzia di traduzione o software di traduzione |
| ChatGPT et traduction juridique : ce que Corrext apporte | `/fr/comparatif/chatgpt-traduction-juridique/` | `/it/confronto/chatgpt-traduzione-giuridica/` | ChatGPT traduzione giuridica |
| DeepL Pro et traduction juridique : ce que Corrext change | `/fr/comparatif/deepl-traduction-juridique/` | `/it/confronto/deepl-traduzione-giuridica/` | DeepL traduzione giuridica |

## Solutions par métier (7)

| Page | Adresse FR | Adresse IT | Requête visée |
|---|---|---|---|
| Solutions par métier · Neur.on, traduction juridique suisse | `/fr/solutions/` | `/it/soluzioni/` | traduzione per avvocati e banche |
| Traduction juridique pour cabinets d'avocats suisses | `/fr/solutions/cabinets-avocats/` | `/it/soluzioni/studi-legali/` | traduzione per studi legali |
| Traduction juridique et financière pour banques | `/fr/solutions/banques-finance/` | `/it/soluzioni/banche/` | traduzione per banche Svizzera |
| Traduction pour directions juridiques et Legal Ops | `/fr/solutions/directions-juridiques/` | `/it/soluzioni/uffici-legali/` | traduzione ufficio legale Legal Ops |
| Traduction pour autorités et administrations suisses | `/fr/solutions/autorites-administration/` | `/it/soluzioni/enti-pubblici/` | traduzione per enti pubblici e amministrazioni |
| Traduction pour fiduciaires, audit et conseil | `/fr/solutions/fiduciaires-conseil/` | `/it/soluzioni/fiduciarie/` | traduzione per fiduciarie e società di revisione |
| Traduction juridique pour LegalTechs et éditeurs | `/fr/solutions/editeurs-legaltech/` | `/it/soluzioni/legaltech-editori/` | API traduzione giuridica LegalTech |

## Domaines du droit (13)

| Page | Adresse FR | Adresse IT | Requête visée |
|---|---|---|---|
| Traduction juridique par domaine et par langue | `/fr/traduction/` | `/it/traduzione/` | traduzione giuridica specializzata Svizzera |
| Traduction juridique de contrats suisses, DE FR IT | `/fr/traduction/contrats/` | `/it/traduzione/contratti/` | traduzione contratti |
| Traduction en droit des sociétés suisse, DE FR IT | `/fr/traduction/droit-des-societes/` | `/it/traduzione/diritto-societario/` | traduzione statuto società |
| Traduction pour fusions et acquisitions en Suisse | `/fr/traduction/fusions-acquisitions/` | `/it/traduzione/fusioni-acquisizioni/` | traduzione M&A |
| Traduction juridique pour contentieux et arbitrage | `/fr/traduction/contentieux-arbitrage/` | `/it/traduzione/contenzioso-arbitrato/` | traduzione arbitrato |
| Traduction juridique et financière pour les banques | `/fr/traduction/banque-finance/` | `/it/traduzione/banca-finanza/` | traduzione finanziaria |
| Traduction réglementaire, compliance et FINMA | `/fr/traduction/compliance-finma/` | `/it/traduzione/compliance-finma/` | traduzione circolari FINMA |
| Traduction des rapports annuels et comptes suisses | `/fr/traduction/rapports-annuels-financiers/` | `/it/traduzione/rapporti-annuali/` | traduzione rapporto annuale |
| Traduction juridique et fiscale en droit suisse | `/fr/traduction/fiscalite/` | `/it/traduzione/diritto-tributario/` | traduzione fiscale |
| Traduction juridique pour l'assurance en Suisse | `/fr/traduction/assurance/` | `/it/traduzione/assicurazioni/` | traduzione assicurativa |
| Traduction de brevets, marques et droit d'auteur | `/fr/traduction/propriete-intellectuelle/` | `/it/traduzione/proprieta-intellettuale/` | traduzione brevetti |
| Traduction juridique en droit du travail suisse | `/fr/traduction/droit-du-travail/` | `/it/traduzione/diritto-del-lavoro/` | traduzione contratto di lavoro |
| Traduction en droit pénal et procédure pénale suisse | `/fr/traduction/droit-penal/` | `/it/traduzione/diritto-penale/` | traduzione diritto penale |

## Paires de langues (6)

| Page | Adresse FR | Adresse IT | Requête visée |
|---|---|---|---|
| Traduction juridique de l'allemand au français | `/fr/traduction/allemand-francais/` | `/it/traduzione/tedesco-francese/` | traduzione giuridica tedesco francese |
| Traduction juridique du français vers l'allemand | `/fr/traduction/francais-allemand/` | `/it/traduzione/francese-tedesco/` | traduzione francese tedesco diritto |
| Traduction juridique de l'allemand vers l'anglais | `/fr/traduction/allemand-anglais/` | `/it/traduzione/tedesco-inglese/` | traduzione giuridica tedesco inglese |
| Traduction juridique de l'anglais vers l'allemand | `/fr/traduction/anglais-allemand/` | `/it/traduzione/inglese-tedesco/` | tradurre contratto inglese tedesco |
| Traduction juridique du français vers l'anglais | `/fr/traduction/francais-anglais/` | `/it/traduzione/francese-inglese/` | traduzione giuridica francese inglese |
| Traduction juridique de l'italien au français | `/fr/traduction/italien-francais/` | `/it/traduzione/italiano-francese/` | traduzione giuridica italiano francese |

## Glossaire (53)

| Page | Adresse FR | Adresse IT | Requête visée |
|---|---|---|---|
| Glossaire juridique suisse en quatre langues | `/fr/ressources/glossaire/` | `/it/risorse/glossario/` | dizionario giuridico tedesco italiano |
| Abtretung : la cession de créance en droit suisse | `/fr/ressources/glossaire/abtretung/` | `/it/risorse/glossario/abtretung/` | cessione del credito in tedesco |
| Aktiengesellschaft : la société anonyme suisse | `/fr/ressources/glossaire/aktiengesellschaft/` | `/it/risorse/glossario/aktiengesellschaft/` | società anonima in tedesco |
| Aktienkapital : le capital-actions | `/fr/ressources/glossaire/aktienkapital/` | `/it/risorse/glossario/aktienkapital/` | capitale azionario in tedesco |
| Arbeitsvertrag : le contrat de travail suisse | `/fr/ressources/glossaire/arbeitsvertrag/` | `/it/risorse/glossario/arbeitsvertrag/` | contratto di lavoro in tedesco |
| Arrest : le séquestre en droit suisse des poursuites | `/fr/ressources/glossaire/arrest/` | `/it/risorse/glossario/arrest/` | sequestro in tedesco |
| Bankgeheimnis : le secret bancaire en droit suisse | `/fr/ressources/glossaire/bankgeheimnis/` | `/it/risorse/glossario/bankgeheimnis/` | segreto bancario in tedesco |
| Beschwerde : le recours devant le Tribunal fédéral | `/fr/ressources/glossaire/beschwerde/` | `/it/risorse/glossario/beschwerde/` | ricorso in tedesco |
| Betreibung : la poursuite pour dettes en Suisse | `/fr/ressources/glossaire/betreibung/` | `/it/risorse/glossario/betreibung/` | esecuzione in tedesco |
| Bürgschaft : le cautionnement en droit suisse | `/fr/ressources/glossaire/buergschaft/` | `/it/risorse/glossario/buergschaft/` | fideiussione in tedesco |
| Bundesgericht : le Tribunal fédéral suisse | `/fr/ressources/glossaire/bundesgericht/` | `/it/risorse/glossario/bundesgericht/` | Tribunale federale in tedesco |
| fristlose Kündigung : la résiliation immédiate | `/fr/ressources/glossaire/fristlose-kuendigung/` | `/it/risorse/glossario/fristlose-kuendigung/` | risoluzione immediata in tedesco |
| Geldwäscherei : le blanchiment d'argent en Suisse | `/fr/ressources/glossaire/geldwaescherei/` | `/it/risorse/glossario/geldwaescherei/` | riciclaggio di denaro in tedesco |
| Generalversammlung : l'assemblée générale en Suisse | `/fr/ressources/glossaire/generalversammlung/` | `/it/risorse/glossario/generalversammlung/` | assemblea generale in tedesco |
| Gewährleistung : la garantie des défauts | `/fr/ressources/glossaire/gewaehrleistung/` | `/it/risorse/glossario/gewaehrleistung/` | garanzia in tedesco |
| GmbH : la société à responsabilité limitée | `/fr/ressources/glossaire/gmbh/` | `/it/risorse/glossario/gmbh/` | società a garanzia limitata in tedesco |
| Grundbuch : le registre foncier suisse | `/fr/ressources/glossaire/grundbuch/` | `/it/risorse/glossario/grundbuch/` | registro fondiario in tedesco |
| Handelsregister : le registre du commerce suisse | `/fr/ressources/glossaire/handelsregister/` | `/it/risorse/glossario/handelsregister/` | registro di commercio in tedesco |
| Konkurrenzverbot : la clause de non-concurrence | `/fr/ressources/glossaire/konkurrenzverbot/` | `/it/risorse/glossario/konkurrenzverbot/` | divieto di concorrenza in tedesco |
| Konkurs : la faillite et la masse en droit suisse | `/fr/ressources/glossaire/konkurs/` | `/it/risorse/glossario/konkurs/` | fallimento in tedesco |
| Konventionalstrafe : la clause pénale | `/fr/ressources/glossaire/konventionalstrafe/` | `/it/risorse/glossario/konventionalstrafe/` | pena convenzionale in tedesco |
| Kündigung : la résiliation du contrat de travail | `/fr/ressources/glossaire/kuendigung/` | `/it/risorse/glossario/kuendigung/` | disdetta in tedesco |
| Mängelrüge : l'avis des défauts en droit suisse | `/fr/ressources/glossaire/maengelruege/` | `/it/risorse/glossario/maengelruege/` | avviso al venditore in tedesco |
| Mehrwertsteuer : la TVA suisse en quatre langues | `/fr/ressources/glossaire/mehrwertsteuer/` | `/it/risorse/glossario/mehrwertsteuer/` | imposta sul valore aggiunto in tedesco |
| Mietvertrag : le bail à loyer en droit suisse | `/fr/ressources/glossaire/mietvertrag/` | `/it/risorse/glossario/mietvertrag/` | contratto di locazione in tedesco |
| Nachlassstundung : le sursis concordataire | `/fr/ressources/glossaire/nachlassstundung/` | `/it/risorse/glossario/nachlassstundung/` | moratoria concordataria in tedesco |
| Personendaten : les données personnelles en Suisse | `/fr/ressources/glossaire/personendaten/` | `/it/risorse/glossario/personendaten/` | dati personali in tedesco |
| Pflichtteil : la réserve héréditaire suisse | `/fr/ressources/glossaire/pflichtteil/` | `/it/risorse/glossario/pflichtteil/` | porzione legittima in tedesco |
| Prospekt : le prospectus des marchés financiers | `/fr/ressources/glossaire/prospekt/` | `/it/risorse/glossario/prospekt/` | prospetto in tedesco |
| Quellensteuer : l'impôt à la source suisse | `/fr/ressources/glossaire/quellensteuer/` | `/it/risorse/glossario/quellensteuer/` | imposta alla fonte in tedesco |
| Rechtsöffnung : la mainlevée de l'opposition | `/fr/ressources/glossaire/rechtsoeffnung/` | `/it/risorse/glossario/rechtsoeffnung/` | rigetto dell'opposizione in tedesco |
| Rechtsvorschlag : l'opposition en poursuite suisse | `/fr/ressources/glossaire/rechtsvorschlag/` | `/it/risorse/glossario/rechtsvorschlag/` | opposizione in tedesco |
| Revisionsstelle : l'organe de révision en Suisse | `/fr/ressources/glossaire/revisionsstelle/` | `/it/risorse/glossario/revisionsstelle/` | ufficio di revisione in tedesco |
| Schadenersatz : les dommages-intérêts en Suisse | `/fr/ressources/glossaire/schadenersatz/` | `/it/risorse/glossario/schadenersatz/` | risarcimento del danno in tedesco |
| Schiedsgericht : le tribunal arbitral en Suisse | `/fr/ressources/glossaire/schiedsgericht/` | `/it/risorse/glossario/schiedsgericht/` | tribunale arbitrale in tedesco |
| Schuldnerverzug : la demeure du débiteur | `/fr/ressources/glossaire/schuldnerverzug/` | `/it/risorse/glossario/schuldnerverzug/` | mora del debitore in tedesco |
| Sorgfaltspflichten : les obligations de diligence | `/fr/ressources/glossaire/sorgfaltspflichten/` | `/it/risorse/glossario/sorgfaltspflichten/` | obblighi di diligenza in tedesco |
| Statuten : les statuts d'une société suisse | `/fr/ressources/glossaire/statuten/` | `/it/risorse/glossario/statuten/` | statuto in tedesco |
| Steuerhinterziehung : la soustraction d'impôt | `/fr/ressources/glossaire/steuerhinterziehung/` | `/it/risorse/glossario/steuerhinterziehung/` | sottrazione d'imposta in tedesco |
| Strafbefehl : l'ordonnance pénale en droit suisse | `/fr/ressources/glossaire/strafbefehl/` | `/it/risorse/glossario/strafbefehl/` | decreto d'accusa in tedesco |
| Überstunden : les heures supplémentaires en Suisse | `/fr/ressources/glossaire/ueberstunden/` | `/it/risorse/glossario/ueberstunden/` | lavoro straordinario in tedesco |
| Untersuchungshaft : la détention provisoire suisse | `/fr/ressources/glossaire/untersuchungshaft/` | `/it/risorse/glossario/untersuchungshaft/` | carcerazione preventiva in tedesco |
| Verfügung : la décision administrative suisse | `/fr/ressources/glossaire/verfuegung/` | `/it/risorse/glossario/verfuegung/` | decisione in tedesco |
| Verjährung : la prescription des créances en Suisse | `/fr/ressources/glossaire/verjaehrung/` | `/it/risorse/glossario/verjaehrung/` | prescrizione in tedesco |
| Verrechnungssteuer : l'impôt anticipé en Suisse | `/fr/ressources/glossaire/verrechnungssteuer/` | `/it/risorse/glossario/verrechnungssteuer/` | imposta preventiva in tedesco |
| Versicherungsvertrag : le contrat d'assurance suisse | `/fr/ressources/glossaire/versicherungsvertrag/` | `/it/risorse/glossario/versicherungsvertrag/` | contratto d'assicurazione in tedesco |
| Verwaltungsrat : le conseil d'administration suisse | `/fr/ressources/glossaire/verwaltungsrat/` | `/it/risorse/glossario/verwaltungsrat/` | consiglio d'amministrazione in tedesco |
| Verzugszins : intérêt moratoire en droit suisse | `/fr/ressources/glossaire/verzugszins/` | `/it/risorse/glossario/verzugszins/` | interesse moratorio in tedesco |
| Vollmacht : pouvoirs et procuration | `/fr/ressources/glossaire/vollmacht/` | `/it/risorse/glossario/vollmacht/` | procura in tedesco |
| vorsorgliche Massnahmen : mesures provisionnelles | `/fr/ressources/glossaire/vorsorgliche-massnahmen/` | `/it/risorse/glossario/vorsorgliche-massnahmen/` | provvedimenti cautelari in tedesco |
| Willensvollstrecker : l'exécuteur testamentaire | `/fr/ressources/glossaire/willensvollstrecker/` | `/it/risorse/glossario/willensvollstrecker/` | esecutore testamentario in tedesco |
| Ayant droit économique : la notion de la LBA | `/fr/ressources/glossaire/wirtschaftlich-berechtigte-person/` | `/it/risorse/glossario/wirtschaftlich-berechtigte-person/` | avente economicamente diritto in tedesco |
| Zahlungsbefehl : le commandement de payer suisse | `/fr/ressources/glossaire/zahlungsbefehl/` | `/it/risorse/glossario/zahlungsbefehl/` | precetto esecutivo in tedesco |

## Centre d'aide (14)

| Page | Adresse FR | Adresse IT | Requête visée |
|---|---|---|---|
| Centre d'aide Corrext | `/fr/aide/` | `/it/aiuto/` | Corrext aiuto |
| Premiers pas dans Corrext : se connecter et traduire | `/fr/aide/premiers-pas/` | `/it/aiuto/primi-passi/` | Corrext accesso primi passi |
| Découvrir Corrext · Centre d'aide | `/fr/aide/decouvrir-corrext/` | `/it/aiuto/scoprire-corrext/` | Corrext funzionalità |
| Traduction texte et document dans Corrext | `/fr/aide/traduction-texte-et-document/` | `/it/aiuto/traduzione-documenti/` | Corrext tradurre un file |
| Gestion de projet : relecture et devis Corrext | `/fr/aide/gestion-de-projet/` | `/it/aiuto/progetti-di-traduzione/` | Corrext ordinare revisione e preventivo |
| Éditeur de relecture · Centre d'aide | `/fr/aide/editeur-de-relecture/` | `/it/aiuto/revisione/` | Corrext rivedere una traduzione |
| Fast lookup CHnell : chercher un terme en contexte | `/fr/aide/chnell/` | `/it/aiuto/chnell/` | Fast lookup CHnell cercare un termine |
| Traduction certifiée d'extraits du registre suisse | `/fr/aide/extraits-registre/` | `/it/aiuto/estratto-registro-di-commercio/` | ordinare traduzione certificata estratto registro di commercio |
| Formats de fichiers et langues acceptés par Corrext | `/fr/aide/formats-et-langues/` | `/it/aiuto/formati-e-lingue/` | Corrext formati di file e lingue |
| Sécurité, confidentialité et compte · Centre d'aide | `/fr/aide/securite-et-confidentialite/` | `/it/aiuto/sicurezza-e-riservatezza/` | Corrext protezione dei dati account |
| Dépannage Corrext : bouton grisé, langue, fichier | `/fr/aide/depannage/` | `/it/aiuto/risoluzione-problemi/` | Corrext risolvere un problema |
| Organisation, membres et rôles · Centre d'aide | `/fr/aide/admin-organisation/` | `/it/aiuto/admin-organizzazione/` | Corrext gestire utenti e ruoli |
| Moteurs et confidentialité · Centre d'aide | `/fr/aide/admin-moteurs/` | `/it/aiuto/admin-motori/` | Corrext abilitare motori di traduzione |
| Mémoires et terminologie · Centre d'aide | `/fr/aide/admin-memoires/` | `/it/aiuto/admin-memorie/` | Corrext memoria di traduzione e terminologia |

## Ressources, guides et études (6)

| Page | Adresse FR | Adresse IT | Requête visée |
|---|---|---|---|
| Ressources sur la traduction juridique suisse | `/fr/ressources/` | `/it/risorse/` | guida traduzione giuridica Svizzera |
| Guides pratiques de la traduction juridique suisse | `/fr/ressources/guides/` | `/it/risorse/guide/` | guida pratica traduzione giuridica |
| Organiser la traduction juridique dans un cabinet | `/fr/ressources/guides/organiser-traduction-cabinet/` | `/it/risorse/guide/organizzare-traduzioni-studio-legale/` | organizzare le traduzioni nello studio legale |
| Préparer un rapport annuel multilingue en Suisse | `/fr/ressources/guides/rapport-annuel-multilingue/` | `/it/risorse/guide/rapporto-annuale-multilingue/` | rapporto annuale multilingue |
| Études et benchmarks sur la traduction juridique | `/fr/ressources/etudes/` | `/it/risorse/studi/` | benchmark traduzione automatica diritto |
| Évaluer un moteur de traduction sur le droit suisse | `/fr/ressources/etudes/evaluer-moteur-traduction-juridique/` | `/it/risorse/studi/valutare-motore-traduzione/` | valutare un motore di traduzione automatica |

## Blog : articles (4)

| Page | Adresse FR | Adresse IT | Requête visée |
|---|---|---|---|
| Blog Neur.on : droit suisse, traduction et actualités | `/fr/ressources/blog/` | `/it/risorse/blog/` | blog traduzione giuridica Svizzera |
| Traduire un contrat en droit suisse quadrilingue | `/fr/ressources/blog/traduire-contrat-droit-suisse/` | `/it/risorse/blog/tradurre-contratto-diritto-svizzero/` | tradurre un contratto di diritto svizzero |
| Comprendre un devis de traduction juridique suisse | `/fr/ressources/blog/comprendre-devis-traduction-juridique/` | `/it/risorse/blog/preventivo-traduzione-giuridica/` | preventivo traduzione giuridica costi |
| Secret professionnel et outils de traduction IA | `/fr/ressources/blog/secret-professionnel-outils-traduction/` | `/it/risorse/blog/segreto-professionale-traduzione-ia/` | segreto professionale traduzione IA |

## Blog : actualités (32)

| Page | Adresse FR | Adresse IT | Requête visée |
|---|---|---|---|
| Actualités de Neur.on depuis 2020 | `/fr/ressources/blog/actualites/` | `/it/risorse/blog/notizie/` | Neur.on notizie |
| Paula Reichenberg à l’EPFL Investor Day 2024 | `/fr/ressources/blog/paula-reichenberg-pitch-epfl-investor-day-2024/` | `/it/risorse/blog/epfl-investor-day-2024/` | EPFL Investor Day 2024 |
| Swisscom et Neur.on annoncent une collaboration | `/fr/ressources/blog/neuron-swisscom-collaboration-kickstart-2024/` | `/it/risorse/blog/collaborazione-swisscom-2024/` | Swisscom Neur.on collaborazione |
| Neur.on au Startups Showcase du TLTF Summit 2024 | `/fr/ressources/blog/neuron-tltf-summit-2024-miami-startups-showcase/` | `/it/risorse/blog/tltf-summit-2024-miami/` | TLTF Summit 2024 Startups Showcase |
| LegalTechTalk 2024 à Londres : enseignements clés | `/fr/ressources/blog/legaltechtalk-2024-londres-enseignements/` | `/it/risorse/blog/legaltechtalk-2024-londra/` | LegalTechTalk 2024 Londra |
| L’IA dans le secteur juridique : table ronde SLTA | `/fr/ressources/blog/table-ronde-ia-juridique-slta-zurich-2024/` | `/it/risorse/blog/tavola-rotonda-slta-zurigo-2024/` | SLTA tavola rotonda IA diritto Zurigo |
| Kilian Marty rejoint le conseil consultatif | `/fr/ressources/blog/kilian-marty-rejoint-conseil-consultatif-neuron/` | `/it/risorse/blog/kilian-marty-consiglio-consultivo/` | Kilian Marty cibersicurezza |
| Les start-up doivent-elles craindre l’AI Act ? | `/fr/ressources/blog/ai-act-grand-challenge-universite-saint-gall/` | `/it/risorse/blog/ai-act-grand-challenge-san-gallo/` | AI Act start-up San Gallo |
| PwC et The LegalTech Fund : pitch à Londres | `/fr/ressources/blog/paula-reichenberg-pwc-legaltech-fund-londres/` | `/it/risorse/blog/pwc-legaltech-fund-londra/` | PwC The LegalTech Fund Londra |
| AI Days 2025 Genève : entraîner un LLM à traduire | `/fr/ressources/blog/neuron-ai-days-2025-geneve-llm-traduction/` | `/it/risorse/blog/ai-days-2025-ginevra/` | AI Days 2025 Ginevra |
| eJustice.ch, 40 ans : premier Kamingespräch | `/fr/ressources/blog/ejustice-40-ans-kamingesprach-neuron/` | `/it/risorse/blog/ejustice-40-anni-kamingespraech/` | eJustice.ch Kamingespräch Swiss Justice Base Model |
| IA et études d’avocats : panel AI in Business | `/fr/ressources/blog/panel-ai-in-business-zurich-2024/` | `/it/risorse/blog/ai-in-business-zurigo-2024/` | AI in Business Zurigo studi legali |
| GEN AI Summit 2024 Lausanne : IA et traduction | `/fr/ressources/blog/neuron-gen-ai-summit-2024-lausanne/` | `/it/risorse/blog/gen-ai-summit-2024-losanna/` | GEN AI Summit 2024 Losanna |
| Swiss FinTech Awards 2024 : Neur.on parmi les 4 finalistes | `/fr/ressources/blog/neuron-quatre-finalistes-swiss-fintech-awards-2024/` | `/it/risorse/blog/swiss-fintech-awards-2024-finalisti/` | Swiss FinTech Awards 2024 finalisti |
| Trust Valley Day : risques cyber et PME | `/fr/ressources/blog/trust-valley-day-2023-risques-cyber-pme/` | `/it/risorse/blog/trust-valley-day-2023-rischi-cyber/` | rischi cyber PMI Trust Valley |
| LegalTech et avocats : alliés ou concurrents ? | `/fr/ressources/blog/legaltech-avocats-allies-ou-concurrents/` | `/it/risorse/blog/legaltech-e-avvocati/` | LegalTech avvocati concorrenza |
| Paula Reichenberg au Female Founder Project 2025 | `/fr/ressources/blog/paula-reichenberg-female-founder-project-ubs-2025/` | `/it/risorse/blog/female-founder-project-ubs-2025/` | UBS Female Founder Project 2025 |
| GILW25 : Paula Reichenberg et l’IA rentable | `/fr/ressources/blog/paula-reichenberg-panel-gilw25-geneve-ia/` | `/it/risorse/blog/gilw25-ginevra-panel-ia/` | Geneva International Legal Week 2025 |
| Paula Reichenberg au Conseil stratégique HES-SO | `/fr/ressources/blog/paula-reichenberg-conseil-strategique-hes-so/` | `/it/risorse/blog/consiglio-strategico-hes-so/` | HES-SO consiglio strategico |
| Kickstart Innovation 2024 : 42 scale-ups retenues | `/fr/ressources/blog/neuron-cohorte-kickstart-innovation-2024/` | `/it/risorse/blog/kickstart-innovation-2024/` | Kickstart Innovation 2024 Finance Insurance |
| LegalTechTalk 2024 : réinventer les cabinets | `/fr/ressources/blog/legaltechtalk-2024-londres-modele-operationnel-cabinets/` | `/it/risorse/blog/legaltechtalk-2024-modello-operativo/` | modello operativo studio legale LegalTech |
| AMLD EPFL 2024 : AI-Powered Projects à Lausanne | `/fr/ressources/blog/neuron-amld-epfl-2024-lausanne/` | `/it/risorse/blog/amld-epfl-2024-losanna/` | AMLD EPFL 2024 |
| Le parcours d’Orane Laeri sur orientation.ch | `/fr/ressources/blog/orane-laeri-parcours-orientation-ch/` | `/it/risorse/blog/orane-laeri-percorso/` | Orane Laeri linguistica percorso |
| Soutien de l’État de Fribourg à la traduction IA | `/fr/ressources/blog/etat-fribourg-soutien-neuron-traduction-juridique-ia/` | `/it/risorse/blog/cantone-friburgo-sostegno/` | Cantone di Friburgo traduzione IA |
| Schwyz : extraits du registre traduits par IA | `/fr/ressources/blog/registre-commerce-schwyz-traduction-ia-extraits-anglais/` | `/it/risorse/blog/registro-di-commercio-svitto/` | registro di commercio Svitto estratti in inglese |
| Weblaw Forum 2024 : Paula Reichenberg au jury | `/fr/ressources/blog/paula-reichenberg-jury-weblaw-forum-2024/` | `/it/risorse/blog/weblaw-forum-2024-giuria/` | Weblaw Forum 2024 Elevator Pitch |
| Swiss FinTech Awards 2024 : finaliste Early Stage | `/fr/ressources/blog/neuron-finaliste-early-stage-swiss-fintech-awards-2024/` | `/it/risorse/blog/swiss-fintech-awards-2024-early-stage/` | Swiss FinTech Awards 2024 Early Stage |
| Top 10 des Swiss FinTech Awards 2024 | `/fr/ressources/blog/neuron-top-10-startups-fintech-suisses-2024/` | `/it/risorse/blog/swiss-fintech-awards-2024-top-10/` | Swiss FinTech Awards 2024 Top 10 |
| Souveraineté des données en Suisse : Trust Valley | `/fr/ressources/blog/cybersecurite-souverainete-donnees-pme-trust-valley/` | `/it/risorse/blog/trust-valley-2023-sovranita-dati/` | sovranità dei dati PMI Svizzera |
| Conférence MIDS 2023 à Genève : IA générative | `/fr/ressources/blog/paula-reichenberg-conference-mids-geneve-2023/` | `/it/risorse/blog/conferenza-mids-ginevra-2023/` | conferenza MIDS Ginevra IA generativa |
| Paula Reichenberg, Digital Shaper 2023 | `/fr/ressources/blog/paula-reichenberg-digital-shaper-2023-bilanz/` | `/it/risorse/blog/digital-shaper-2023-bilanz/` | BILANZ Digital Shapers 2023 |
| Conférence BDÜ 2022 : avocats et traducteurs | `/fr/ressources/blog/paula-reichenberg-table-ronde-bdu-2022/` | `/it/risorse/blog/conferenza-bdue-2022/` | conferenza BDÜ 2022 avvocati traduttori |

## Société et pages légales (5)

| Page | Adresse FR | Adresse IT | Requête visée |
|---|---|---|---|
| À propos de Neur.on · la société suisse derrière Corrext | `/fr/a-propos/` | `/it/chi-siamo/` | Neur.on Friburgo LegalTech |
| Presse · Neur.on AI Solutions SA, LegalTech suisse à Fribourg | `/fr/a-propos/presse/` | `/it/chi-siamo/stampa/` | Neur.on stampa |
| Contact et démo · Neur.on, traduction juridique en Suisse | `/fr/contact/` | `/it/contatto/` | Corrext demo |
| Mentions légales et conditions d'utilisation | `/fr/mentions-legales/` | `/it/note-legali/` | Neur.on note legali |
| Protection des données | `/fr/protection-des-donnees/` | `/it/protezione-dei-dati/` | Neur.on informativa sulla protezione dei dati |

## Points d'attention

- `src/data/redirections.json` ne contient aucune ancienne adresse en `/it/` : aucune collision avec les adresses ci-dessus.
- Il n'existe pas de page de paire au départ ou à destination de l'italien autre que `italien-francais`. Un lecteur tessinois cherche plutôt « traduzione giuridica tedesco italiano » ou « italiano tedesco » : piste pour une page future, hors de ce lot.
- Adresses à fusionner dans `src/routes.json` sous la clé `it`, à côté de `de` et `en`.

# Italien : points à trancher par le traducteur expert

État au 2 octobre 2026. Les 156 pages IT sont adaptées puis relues par un second agent : le contrôle automatique ne signale aucun bloquant. Elles restent « brouillon » (`src/langues/it/statut.json`) jusqu'à la relecture experte. Ce fichier rassemble les choix que les agents n'ont pas pu trancher seuls.

## Conventions fixées par défaut (à confirmer)

- **Registre** : « voi » partout (vérifié sur UBS Aziende et Swisscom Business en Suisse italienne). Les libellés de boutons et de liens sont à l'infinitif (« Leggere l'articolo »), comme le prévoit le guide.
- **Devis** : « offerta », usage commercial suisse et parallèle à « Offerte » en DE ; « preventivo » (art. 375 CO) seulement dans le title, la description et le h1 de l'article sur le devis.
- **Milliers** : apostrophe dans le texte courant (15'000), comme les versions FR et DE ; la page Langues précise que les textes fédéraux emploient l'espace.
- **Écriture inclusive** : masculin inclusif, selon les Istruzioni de la Chancellerie fédérale (n. 143 à 147).
- **Niveau 3** : libellé de l'application « Double review & certified translation » ; dans le texte courant « Double review e traduzione certificata » ; document de l'agence « attestazione » ; niveau 4 « Autenticazione e apostille ».
- **Stockage** : « archiviazione » (environ 170 occurrences). L'équivalent exact serait « conservazione » (art. 5 lett. d LPD, RGPD italien art. 4 n. 2) : à changer en une seule passe si l'expert le préfère.

## Termes à confirmer

- « responsabili del trattamento » pour les sous-traitants (art. 9 LPD) ; l'art. 9 cpv. 3 parle de « terzi » pour les sous-sous-traitants.
- « traduzione certificata e legalizzata » pour « traduction assermentée et légalisée » ; « autenticazione notarile ».
- « strumento CAT » pour TAO ; « lingua di partenza / di arrivo ».
- « rilevanti per i corsi di borsa » et « atta a influenzare il corso di valori mobiliari » (art. 2 let. j LInFi) pour « sensible sur le plan des prix ».
- « modelli di traduzione » pour les « modèles de langage » du service auszug-hr.ch (le texte officiel anglais dit « language models »).
- « cabina di regia », « prova guidata », « colloquio preliminare », « traduzioni fai da te », « visto si stampi ».
- « riservatezza Standard », « aggiunta » (avenant), « società di audit » (LFINMA), « impresa di revisione » (CO).
- « Cancelliere capo » (au Tessin, on dit simplement « Cancelliere »), « Esperto fiduciario », « Socia, dipartimento contenzioso » (fonctions des témoignages d'exemple).
- « clausola di manleva », « garanzia autonoma », « pericolo di collusione » : termes d'usage absents des textes fédéraux.
- « cruscotto », « riquadro » (carte, volet et encadré), « componente aggiuntivo », « barra multifunzione ».
- « direttori legali » dans les actualités ; « servizi di informazione » ou « di intelligence ».
- Noms d'institutions : « Conférence latine des bâtonniers » gardé en français ; « Promozione economica di Zurigo » (descriptif) ; « la stella nascente » (nom de la catégorie UBS non vérifié) ; « Swisslex - Banca svizzera di dati giuridici SA » (à confirmer sur Zefix).

## Écarts entre la base terminologique et les textes officiels

- Vollmacht « procura » : les art. 32 à 34 CO disent « facoltà (di rappresentanza) ».
- Bankgeheimnis « segreto bancario » : l'art. 47 LBCR dit « segreto professionale ».
- Überstunden « lavoro straordinario » : l'art. 321c cpv. 1 CO dit « ore suppletive ».
- « conclusioni » (art. 221 CPC) : le texte dit « la domanda ».
- Avis des défauts : l'art. 201 CO dit « avviso al venditore ».
- LEF : la base contient « sulla esecuzione » (titre officiel) et « sull'esecuzione » ; à unifier.
- 13 titres complets de lois manquent dans `termes-it.json` (les liens Fedlex fonctionnent par l'abréviation).

## Adaptations au lecteur tessinois

Exemples transposés au Tessin ou aux Grisons dans les domaines, les paires et les articles (contrat rédigé à Lugano, exécuté à Zurich ; siège au Tessin, succursale à Zurich…). Aucun n'introduit de fait vérifiable ; à valider.

## Source FR corrigée pendant l'adaptation italienne

Points relevés par les agents italiens et corrigés dans toutes les langues : Verzugszinse (art. 104 OR), Anwaltskongress, 30 domaines CHnell, titres 23 à 32 du CO, cours du Tribunal fédéral à Lucerne, procès-verbal de l'assemblée générale (art. 702 CO), et les fiches du glossaire listées dans le commit « Glossaire FR et DE : 13 imprécisions corrigées ».

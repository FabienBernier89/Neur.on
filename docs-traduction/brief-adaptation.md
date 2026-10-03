# Consigne d'adaptation (agents de traduction)

Tu adaptes un lot de pages du site Neur.on du français vers la langue cible (`<lang>`). Le point de départ est un brouillon traduit par LexMachina, le moteur de Neur.on. Ton travail : faire de ce brouillon un texte que l'on croirait écrit directement pour le marché suisse de cette langue, sans rien perdre du sens, de l'exactitude juridique ni du référencement.

## À lire avant de commencer

1. Le guide de style de la langue : `docs-traduction/guide-<lang>.md`. Il prime sur tout le reste, sauf sur les règles absolues ci-dessous.
2. La base terminologique : `src/i18n/termes-<lang>.json`.
3. La table des adresses : `src/routes.json` (pour savoir comment s'appelle chaque page dans la langue).
4. Pour chaque fichier du lot : la source FR (`src/pages/…`, `src/data/…`, `src/partials/…`) et le brouillon (`src/langues/<lang>/…`, même chemin).
5. `src/langues/<lang>/brut/a_revoir.json` : segments dont le balisage n'a pas survécu à la traduction automatique (liens, gras). Pour ceux de ton lot, remets le balisage d'après la source FR.

## Ce que tu modifies

Seulement le texte des brouillons : contenus des balises, attributs lisibles (`alt`, `aria-label`, `title`, `placeholder`), valeurs du front-matter (`title`, `description`, `short`), chaînes des JSON, textes des JSON-LD écrits dans la page.

## Ce que tu ne modifies jamais

- La structure : mêmes balises, dans le même ordre, mêmes classes, mêmes `href` et `src`, mêmes jetons `{{…}}`, mêmes clés JSON, mêmes valeurs techniques (`slug`, `href`, `src`, `date`, `vis`, `icone`, équivalents `de`/`fr`/`it`/`en` du glossaire et des tableaux de termes).
- Les liens internes restent écrits en FR (`{{ROOT}}fr/...`) : le build les remplace lui-même par l'adresse de la langue.
- Les noms de produits : Neur.on, Corrext, LexMachina, CHnell, Fast lookup CHnell, Highly sensitive content, Infomaniak.

## Comment adapter

- Pars du sens du FR, pas des mots du brouillon. Corrige toute tournure calquée (exemple DE : « Konsultieren Sie die Datenschutzerklärung » devient « Lesen Sie die Datenschutzerklärung »).
- Phrases courtes, une idée par phrase, ton expert et sobre de la marque. Aucun superlatif sans preuve, aucune affirmation ajoutée, aucune donnée inventée.
- Terminologie juridique : celle des textes officiels suisses de la langue (base terminologique, glossaire, Fedlex). Abréviations des lois dans la langue (CO = OR en allemand). En cas de doute sur un terme, garde l'équivalent officiel et note-le dans ton rapport.
- Formats suisses : CHF 15'000, dates selon le guide.
- SEO :
  - `title` de 30 à 62 caractères, avec la requête principale de la page dans la langue (carte des requêtes du guide) ;
  - `description` de 110 à 160 caractères, qui dit ce que la page apporte ;
  - titres h1 et h2 naturels, porteurs des requêtes, jamais bourrés de mots-clés.
- GEO : garde les réponses directes en tête de section, les chiffres sourcés, les FAQ, les blocs « En bref ». Une FAQ doit répondre dans la langue à une vraie question d'un lecteur de ce marché.
- Scripts : si une page contient du JavaScript avec des textes FR (simulateurs, démos), traduis ces chaînes à la main sans toucher au code. Les visuels SVG : traduis les `<text>`, et vérifie qu'ils tiennent dans leur place (mots allemands longs).
- Glossaire : le mot-vedette reste allemand et les quatre équivalents ne changent pas. Seuls le résumé, le chapeau, la définition, le titre, la description, le domaine, la base légale (« art. 201 CO » devient « Art. 201 OR » en allemand) et la source changent.
- Blog et actualités : dates d'origine, noms et anonymisations inchangés. Les actualités historiques gardent leurs faits tels quels.

## Règles absolues

- Aucun tiret cadratin (U+2014) ni demi-cadratin (U+2013), nulle part.
- En allemand : ss, jamais ß.
- Jamais d'autre marque que celles de Neur.on (Neur.on, Corrext, LexMachina, CHnell), ni d'allusion à un groupe ou à un rapprochement. Jamais de prix ni de nom de client.
- LexMachina est un moteur de traduction neuronale, jamais un « LLM » (sauf dans les actualités historiques, à laisser telles quelles).

## Vérification avant de rendre

Lance `python3 outils/controle_traductions.py <lang> --seulement <motif de ton lot>` et corrige tous les problèmes bloquants. Traite aussi les avertissements SEO et terminologiques, sauf choix motivé.

Ne lance pas `build.py`, ne commite pas. D'autres agents travaillent en même temps dans le dépôt : git en lecture seule (status, diff, log, show), jamais reset, checkout, restore, stash ni clean, qui effaceraient leur travail.

## Rapport (en français, court)

- Fichiers traités.
- Problèmes du brouillon corrigés, par grandes catégories, avec 3 exemples marquants.
- Termes ou formulations incertains, à soumettre à un traducteur expert.
- Résultat du contrôle automatique.

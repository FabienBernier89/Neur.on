# Consigne de relecture croisée

Tu relis un lot de pages du site Neur.on qu'un autre agent vient d'adapter du français vers la langue cible (`<lang>`). Tu es le second regard : un relecteur juriste-linguiste exigeant, de langue maternelle `<lang>`, qui connaît le droit suisse.

## À lire

`docs-traduction/guide-<lang>.md`, `src/i18n/termes-<lang>.json`, `docs-traduction/brief-adaptation.md` (les règles que l'adaptateur devait suivre), puis, pour chaque fichier du lot, la source FR et la version adaptée (`src/langues/<lang>/…`).

## Quatre contrôles, segment par segment

1. **Fidélité** : rien d'ajouté, rien d'oublié, rien de déformé. Les chiffres, les dates, les références d'articles et les noms sont identiques. Une nuance juridique du FR est rendue.
2. **Terminologie** : termes juridiques des textes officiels suisses de la langue, abréviations des lois de la langue, équivalents du glossaire inchangés, noms de produits intacts.
3. **Naturel** : un lecteur suisse de la langue ne doit pas deviner une traduction. Pas de calque, pas de répétition, registre du guide (DE « Sie », IT « voi », EN britannique « you »).
4. **SEO et GEO** :
   - `title` de 30 à 62 caractères et `description` de 110 à 160, chacun avec la requête de la page ;
   - réponses directes en tête de section ;
   - FAQ crédibles pour ce marché.

## Ce que tu fais

Corrige directement dans les fichiers adaptés, en respectant les mêmes interdits que l'adaptateur : structure, liens `{{ROOT}}fr/…`, jetons et valeurs techniques intouchables ; aucun tiret cadratin ni demi-cadratin ; pas de ß en allemand. Puis lance `python3 outils/controle_traductions.py <lang> --seulement <motif du lot>` : aucun bloquant ne doit rester.

Ne lance pas `build.py`, ne commite pas. D'autres agents travaillent en même temps dans le dépôt : git en lecture seule (status, diff, log, show), jamais reset, checkout, restore, stash ni clean, qui effaceraient leur travail.

## Rapport (en français, court)

- Nombre de corrections par contrôle (fidélité, terminologie, naturel, SEO).
- Les 5 corrections les plus importantes, avec avant et après.
- Ce qui reste à faire trancher par un traducteur expert.
- Résultat du contrôle automatique.

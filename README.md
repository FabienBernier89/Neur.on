# Neur.on · site neur-on.ai

Site statique de Neur.on (Corrext, LexMachina, CHnell) en quatre langues (FR, DE, IT, EN), généré depuis des sources et des données.

**Mise en ligne** : voir [INTEGRATION.md](INTEGRATION.md).

**Aperçu en ligne** : https://fabienbernier89.github.io/Neur.on/ (aperçu de travail, `noindex` et
`robots.txt` fermé : il ne doit jamais concurrencer neur-on.ai dans l'index des moteurs).

## Construire

```bash
python3 build.py              # aperçu : chaque page porte noindex
python3 build.py --production # version destinée à neur-on.ai
python3 -m http.server 8799 --bind 127.0.0.1 --directory docs
```

## Organisation

| Dossier | Rôle |
|---|---|
| `src/pages/` | pages rédigées, une par dossier, avec un front-matter en commentaire |
| `src/partials/` | méga-menu, pied de page, `llms.txt`, `robots.production.txt` |
| `src/data/` | données des pages à l'échelle (métiers, domaines, langues, glossaire, aide) |
| `src/generators.py` | rendu des pages à l'échelle depuis `src/data` |
| `src/langues/`, `src/i18n/`, `src/routes.json` | traductions, textes d'interface, adresses par langue |
| `assets/` | socle CSS, démo Corrext, méga-menu |
| `docs/` | site généré, servi par GitHub Pages |

## Règles de contenu

Jamais de tiret cadratin ni demi-cadratin ; aucune autre marque que celles de Neur.on, aucune allusion à un groupe ; LexMachina est le moteur de traduction neuronale de Neur.on (jamais « LLM », sauf dans les actualités historiques) ; aucun prix ni nom de client ; témoignages d'exemple signalés comme tels jusqu'à leur remplacement ; modèles concurrents nommés sans numéro de version ; toute affirmation produit vient de l'application observée, toute référence juridique de Fedlex.

## Traductions

Les versions DE, IT et EN sont dans `src/langues/<langue>/`, les adresses dans `src/routes.json`, les guides et consignes dans `docs-traduction/`. Contrôle : `python3 outils/controle_traductions.py <langue>`. Une langue n'est publiée en production que lorsque toutes ses pages sont marquées « relue » dans son `statut.json`.

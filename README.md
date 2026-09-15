# Neur.on · site neur-on.ai

Site statique de Neur.on (Corrext, Neur.on LLM, CHnell), généré depuis des sources et des données.

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
| `assets/` | socle CSS, démo Corrext, méga-menu |
| `docs/` | site généré, servi par GitHub Pages |

## Règles de contenu

Français ; jamais de tiret cadratin ; aucune mention de Legal 230, Lexa ou LexMachina (le moteur
s'appelle Neur.on LLM) ; aucun prix, nom de client ni témoignage ; les modèles concurrents sont
nommés sans numéro de version ; toute affirmation produit vient de l'application observée.

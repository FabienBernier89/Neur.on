# Écrire une page du site Neur.on

Une page = un dossier sous `src/pages/` contenant `index.html`. Le générateur ajoute le doctype,
le head, le méga-menu, le fil d'Ariane, le pied de page et les scripts. **N'écrivez jamais**
`<!DOCTYPE>`, `<html>`, `<head>`, `<body>`, la barre de navigation, le fil d'Ariane ni le footer.

## Front-matter obligatoire

```html
<!--page
title: Titre de l'onglet, 55 à 62 caractères, avec « Neur.on » ou « Corrext »
description: 140 à 155 caractères, bénéfice concret, le mot « Suisse » quand c'est vrai
short: Libellé court pour le fil d'Ariane
nav: corrext | solutions | ressources | neuron-llm | (vide)
-->
```

Ajoutez `assets: ["corrext-demo.js"]` seulement si la page réutilise la démo Fast translation
(un seul cadre `#cx` par page).

## Ordre des blocs

1. `<section class="thero">` hero bleu nuit compact (H1 avec le nom en lede `<em>`, lead,
   `.thero-cta` avec le bouton `btn btn-blue` vers `contact.html` et un `btn btn-ghost` d'ancre,
   `.thero-promise` avec trois preuves).
2. Le corps : alternez les registres, jamais deux grilles de cartes identiques à la suite.
3. `<section class="faq">` avec 5 à 8 `<details class="faq-item">` et le `FAQPage` JSON-LD
   correspondant, mot pour mot.
4. `<section class="final-cta">` bleu nuit (deuxième et dernière ancre navy de la page).

Un bloc `<script type="application/ld+json">` en tête de corps est remonté dans le head par le
générateur. N'y mettez jamais de `BreadcrumbList` : il est généré.

## Classes disponibles (socle `assets/neuron.css`)

| Besoin | Classes |
|---|---|
| Section standard | `section` + `.container`, en-tête `.sec-head` (h2 + p) |
| Registre de faits | `.facts` > `.facts-grid` > `.facts-lead` (h2, p, `.links`) + `.facts-list` > `.fact` (b + p, `small` pour la précision) |
| Trois situations | `.who` > `.sec-head` + `.who-grid` > `.who-item` (h3 avec `<span class="pn">Audience.</span>`, p) |
| Encadré à question | `.gov` > `.gov-box` (div avec h2 + p + `.feat-link`) + `.gov-steps` > div (svg + span avec `<b>`) |
| Bande de liens | `.siblings` > h2 + `.siblings-row` > a (b + span + svg flèche) |
| Bloc fonctionnalité | `.feature` (+ `.rev` pour inverser) > `.feat-txt` (h3, p, `.feat-list` > li > `.chk`, `.feat-link`) + `.feat-visual` > `.win` |
| Cartes produit | `.prod-grid` > `.prod-card` |
| Piliers | `.pillars` > `.pillars-grid` > `.pillar` |
| Preuve, registre | `.trust` > `.trust-grid` (`.trust-lead` + `.ledger` > `.ledger-row`) |
| Tableau comparatif | `.compare` > `.compare-wrap` > `table.cmp` (`.cmp-y`, `.cmp-p`, `.cmp-n`) |
| Chiffres | `.stats` > `.stats-grid` > `.stat` (`.num` + label) |
| Niveaux | `.levels` > `.lev-grid` > `.lev.l1…l4` (`.ln`, `.gauge`, h3, p) |
| Cadre de démonstration Corrext | `.cx` et ses classes (voir une page outil existante) |
| Boutons | `.btn.btn-blue`, `.btn.btn-ghost`, `.btn-outline`, lien de suite `.feat-link` |

Le CSS propre à la page va dans un `<style>` en tête de corps (remonté dans le head). Préfixez
vos classes pour éviter les collisions.

## Règles absolues

- **Français** partout, sauf les libellés de l'application Corrext, qui restent en anglais.
- **Jamais** le tiret cadratin « — » (U+2014). Utilisez « · », « : », la virgule ou « - ».
- **Jamais** les mots Legal 230, Lexa, LexMachina, « groupe », « rapprochement ». Le moteur maison
  s'appelle **Neur.on LLM**. Les moteurs tiers se nomment sans numéro de version : DeepL Pro,
  Azure OpenAI GPT, Claude.
- **Jamais** de prix, de montant en francs, de nom de client, de témoignage, de logo client, ni de
  promesse non observée dans l'application.
- Chiffres autorisés : plus de 15 millions de segments, ISO 27001 (février 2024), 30 langues sur la
  plateforme, quatre langues natives, 25 fichiers de 50 Mo, 26 domaines CHnell, économies « jusqu'à »
  60 / 50 / 80 %, distinctions (Swiss Fintech Awards 2024, BILANZ 2024, Digital Shapers 2023,
  Innosuisse).
- **Souveraineté, formulation exacte** : stockage sur des serveurs suisses dans tous les cas ;
  traitement exclusivement en Suisse en mode Highly sensitive content ou avec Neur.on LLM ; les
  moteurs tiers sont hébergés à l'étranger et déclenchent l'avis Attorney-Client privilege.
- Une seule H1. Hiérarchie h2 puis h3, sans saut. Pas de kicker au-dessus d'un titre : le libellé
  d'audience se met dans le titre, en lede accent suivi d'un point.
- Deux sections bleu nuit par page au maximum : le hero et le CTA final.
- `prefers-reduced-motion` respecté ; animations par `transform` et `opacity` seulement.

## Liens internes

Écrivez les liens vers les autres pages avec le jeton `{{ROOT}}` : `href="{{ROOT}}fr/corrext/"`.
Le générateur le remplace par le bon chemin relatif et neutralise les liens dont la page n'existe
pas encore.

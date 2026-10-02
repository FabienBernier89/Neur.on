# Maquettes auszug-hr · textes à relire

**À faire relire par un traducteur expert avant toute mise en ligne.**

Tous les textes visibles des pages viennent du site source, repris mot pour mot :
auszug-hr.ch/en et auszug-hr.ch/fr pour les pages d'accueil, neur-on.ai/impressum/ et
neur-on.ai/privacy-policy/ pour les pages légales. Ce fichier liste les seuls textes rédigés pour la
maquette, qui n'existent pas sur le site source : meta description, libellés d'accessibilité,
texte alternatif. Pour le français, ils suivent la typographie du site source (pas d'espace avant
le deux-points ni avant le point d'interrogation).

## Versions de langue

| Langue | Statut |
|---|---|
| EN | Créée : `en/index.html`, `en/impressum/index.html`, `en/privacy-policy/index.html` |
| FR | Créée : `fr/index.html`. Pas de pages légales en français : le site source pointe, depuis la version FR, vers les pages anglaises de neur-on.ai (seule version existante). Le pied de page FR renvoie donc vers `en/impressum/` et `en/privacy-policy/`. |
| DE | **Non créée.** Le site source n'a pas de version allemande : le menu de langue ne propose que English et Français, et auszug-hr.ch/de renvoie vers /en/de (erreur 404). Aucun texte allemand à reprendre. |
| IT | **Non créée.** Même constat : auszug-hr.ch/it renvoie vers /en/it (erreur 404). Aucun texte italien à reprendre. |

Dans le sélecteur de langue, Deutsch et Italiano sont affichés sans lien en attendant ces versions.

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
| `<title>` de en/impressum/ | Impressum & Terms of Use \| Corrext |
| `<title>` de en/privacy-policy/ | Privacy and Data Security \| Corrext |

## FR · textes traduits par Claude

| Emplacement | Texte |
|---|---|
| `<meta name="description">` (fr/index.html) | Commandez en ligne une traduction certifiée d’extraits du registre du commerce suisse: certification standard, notariée ou apostillée selon la Convention de La Haye, terminologie juridique rigoureuse, + 30 langues. Dès CHF 99.- |
| `aria-label` du formulaire de recherche | Recherche d’entreprise |
| `aria-label` du sélecteur de langue | Langue |
| `aria-label` du menu de langue compact | Langue: français |
| `aria-label` des liens légaux du pied de page | Informations légales |
| `aria-label` de l'illustration du héro | Illustration: un extrait du registre du commerce allemand et sa traduction française certifiée, avec un sceau et une apostille |
| `alt` du logo Corrext (en-tête et pied de page) | Logo Corrext (le site source garde « Corrext logo » en anglais sur sa page FR) |

## Notes pour le relecteur (écarts volontaires avec le texte source)

- FR et EN, bloc « Processus entièrement digitalisé » / « Fully Digitized Process » : le tiret
  demi-cadratin de la source, après « entièrement digitalisé » et « seamless process », est
  remplacé par une virgule, règle du groupe (aucun tiret demi-cadratin ni cadratin).
- FR et EN, pied de page : « © Neur.on AI Solutions SA » (choix validé pour la maquette EN), à la
  place de « © 2025 Neur.on. Tous droits réservés. » / « © 2025 Neur.on. All rights reserved. ».
- FR et EN : les mises en gras internes aux paragraphes de la source ne sont pas reprises (le texte
  est identique). Les italiques du français sont conservées (« corporate housekeeping »,
  « data scientists »).

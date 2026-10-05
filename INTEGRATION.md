# Mise en ligne de neur-on.ai : guide pour l'intégrateur

Ce dépôt contient le nouveau site de Neur.on, en quatre langues (français, allemand, italien, anglais). C'est un site **statique** : du HTML, une feuille de style et quelques scripts, générés par un programme Python. Il n'y a ni serveur applicatif, ni base de données, ni CMS.

## 1. Générer la version de production

Prérequis : Python 3.9 ou plus récent. Le programme n'utilise que la bibliothèque standard (aucun `pip install`) ; il lit l'historique git pour dater les pages, donc il faut un clone complet du dépôt.

```bash
git clone https://github.com/FabienBernier89/Neur.on.git
cd Neur.on
python3 -m unittest discover tests      # contrôles automatiques : tout doit passer
python3 build.py --production           # génère le site dans le dossier docs/
```

Le contenu du dossier `docs/` est le site à publier **à la racine** de `https://neur-on.ai/`.

**Attention** : le dossier `docs/` présent dans le dépôt est l'**aperçu** de travail (servi sur https://fabienbernier89.github.io/Neur.on/). Chaque page y porte `noindex` et le `robots.txt` y ferme l'indexation. Ne le publiez jamais tel quel : regénérez toujours avec `--production`.

Ce que `--production` change par rapport à l'aperçu :
- plus de `noindex`, `robots.txt` ouvert aux moteurs et aux assistants IA ;
- Google Analytics 4 (`G-H128S2PTKN`), chargé **seulement après consentement** (bandeau `assets/consent.js`, dans la langue de la page) ;
- fichier `.htaccess` (voir § 3) ;
- les quatre langues sont publiées, chacune à ses propres adresses (`/fr/`, `/de/`, `/it/`, `/en/`).

## 2. Deux verrous avant la mise en ligne

Le build de production **refuse de s'exécuter** tant que l'une de ces conditions n'est pas remplie. C'est voulu.

1. **Témoignages d'exemple.** Les pages « Solutions » contiennent des témoignages signalés comme exemples, en attendant de vrais témoignages. Le build de production s'arrête avec le message « Production refusée : témoignage d'exemple à remplacer ». Neur.on fournira les textes définitifs.
2. **Langues relues.** Une langue n'est publiée que si toutes ses pages sont marquées `"relue"` dans `src/langues/<langue>/statut.json` (le français est toujours publié). Les quatre langues sont validées : français, allemand, italien et anglais sont publiés. Si une langue devait être retirée temporairement, il suffirait de repasser une de ses valeurs à `"brouillon"` ; ses liens dans le sélecteur de langue apparaîtraient alors comme « bientôt ».

## 3. Hébergement (Infomaniak, Apache)

- Publiez **tout** le contenu de `docs/`, y compris le fichier caché `.htaccess`.
- Le `.htaccess` généré gère :
  - la redirection vers `https://neur-on.ai` (sans `www`, en HTTPS) ;
  - la racine `/` : redirection 302 vers `/fr/`, `/de/`, `/it/` ou `/en/` selon la langue du navigateur, parmi les langues publiées ;
  - les **redirections 301** des anciennes adresses du site WordPress actuel (liste dans `src/data/redirections.json`, chacune vers la page de sa langue quand elle est publiée) ;
  - les anciens sitemaps de Yoast et le flux `/feed/` ;
  - la page d'erreur `404.html` (dans la langue de l'adresse demandée) ;
  - le cache et la compression.
- Si l'hébergement final est Nginx, les règles sont à transposer à l'identique.
- Certificat HTTPS actif sur `neur-on.ai` et `www.neur-on.ai`.
- **DNS** : ne supprimez jamais l'enregistrement TXT de vérification Google Search Console ni le CNAME de vérification Bing.

## 4. Formulaire de contact

La page Contact (`/fr/contact/` et ses versions) contient un formulaire de demande de démo. Il n'est pas encore relié à un service d'envoi : sans réglage, il ouvre un courriel prérempli vers `team@corrext.com`.

Pour le relier (HubSpot, Formspree ou un service de Neur.on qui accepte un POST `multipart/form-data` et répond en JSON), renseignez l'adresse dans `build.py` :

```python
FORM_ENDPOINT = "https://…"
```

puis regénérez. Le formulaire des quatre langues l'utilisera.

## 5. Outil de gestion des cookies

Le site contient un bandeau de consentement minimal (`assets/consent.js`, traduit dans les quatre langues) : Google Analytics 4 n'est chargé qu'après acceptation, et un lien « Préférences cookies » est ajouté au pied de page.

Neur.on prévoit d'installer un outil de gestion des consentements (CMP) après la mise en ligne. Pour le faire :
1. dans `build.py`, mettre `GA4_ID = ""` : le bandeau minimal, son lien de pied de page et le chargement de GA4 disparaissent ;
2. intégrer le script de l'outil et charger GA4 par son intermédiaire (dans `build.py`, fonction `build_page`, à l'endroit où `consent.js` est ajouté) ;
3. faire adapter les sections 4 et 5 de la politique de confidentialité (`src/pages/protection-des-donnees/` et ses versions dans `src/langues/`), qui citent le bandeau et le lien « Préférences cookies ».

## 6. Après la mise en ligne

1. Vérifier quelques anciennes adresses (redirection 301), par exemple `/about/`, `/de/about/`, `/fr/about/`, `/news/`, et une adresse inexistante (page 404).
2. Vérifier `https://neur-on.ai/robots.txt`, `https://neur-on.ai/sitemap.xml` et `https://neur-on.ai/llms.txt`.
3. Soumettre `https://neur-on.ai/sitemap.xml` dans Google Search Console et dans Bing Webmaster Tools. Le sitemap contient les versions linguistiques de chaque page (balises `hreflang`).
4. Vérifier dans Google Analytics que les visites arrivent après acceptation du bandeau, et rien avant.

## 7. Modifier le site ensuite

Toute modification se fait dans les sources, jamais dans `docs/` (il est effacé à chaque génération) :

| Dossier | Contenu |
|---|---|
| `src/pages/` | pages françaises rédigées, une par dossier |
| `src/data/` | données des pages générées (domaines du droit, glossaire, centre d'aide, blog, actualités…) |
| `src/langues/<langue>/` | versions allemande (`de`), italienne (`it`) et anglaise (`en`) des pages et données, avec leur `statut.json` |
| `src/i18n/` | textes d'interface traduits, bases terminologiques |
| `src/routes.json` | adresse de chaque page dans chaque langue (ne pas changer une adresse publiée) |
| `src/partials/` | menu, pied de page, 404, `llms.txt`, `robots.production.txt` |
| `assets/` | feuille de style, scripts, images |
| `build.py`, `src/generators.py` | génération du site |
| `outils/` | contrôles des traductions et des liens |
| `tests/` | tests automatiques |

Après toute modification : `python3 -m unittest discover tests`, puis `python3 build.py --production`.

Pour toute question sur le contenu, voir avec Fabien Bernier.

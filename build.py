#!/usr/bin/env python3
"""Générateur du site Neur.on.

Sources : src/pages (pages rédigées), src/templates + src/data (pages à l'échelle),
src/partials (méga-menu et pied de page), assets/ (CSS et JS partagés).
Sortie : docs/ (servi par GitHub Pages et par le serveur local).

Usage : python3 build.py [--production]
En mode aperçu (défaut), chaque page porte noindex et robots.txt interdit tout :
l'aperçu GitHub Pages ne doit jamais concurrencer neur-on.ai dans l'index.
"""
import subprocess
import json, os, re, shutil, sys, datetime

BASE = os.environ.get("NEURON_BASE") or os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(BASE, "src")
OUT = os.path.join(BASE, "docs")
SITE = "https://neur-on.ai"
LANG = "fr"
PRODUCTION = "--production" in sys.argv
TODAY = datetime.date.today().isoformat()
# Mesure d'audience, active seulement avec --production.
# GA4 repris du site WordPress actuel ; le script Google ne se charge qu'après consentement (consent.js).
GA4_ID = "G-H128S2PTKN"
# Jeton de vérification Google Search Console (balise HTML), à renseigner si la vérification DNS n'est pas retenue.
GSC_TOKEN = ""
def _asset_version():
    import hashlib
    h = hashlib.sha1()
    for f in sorted(os.listdir(os.path.join(BASE, "assets"))):
        if f.endswith((".css", ".js")):
            h.update(open(os.path.join(BASE, "assets", f), "rb").read())
    return h.hexdigest()[:8]


ASSET_V = _asset_version()

# Anciens noms de fichiers plats vers les chemins du site
LEGACY = {
    "neuron-homepage.html": "fr/",
    "corrext.html": "fr/corrext/",
    "corrext-traduction-texte-et-document.html": "fr/corrext/traduction-texte-et-document/",
    "corrext-gestion-de-projet.html": "fr/corrext/gestion-de-projet/",
    "corrext-chnell.html": "fr/corrext/chnell/",
    "corrext-extraits-registre.html": "fr/corrext/extraits-registre-commerce/",
    "securite-souverainete.html": "fr/securite-souverainete/",
    "neuron-llm.html": "fr/lexmachina/",
    "contact.html": "fr/contact/",
    "a-propos.html": "fr/a-propos/",
}

PAGES = {}   # (langue, chemin FR) -> {title, short, lastmod}
sys.path.insert(0, os.path.join(BASE, "src"))
import i18n  # noqa: E402
from i18n import T  # noqa: E402
from langues import Routes, localiser, alternates, LANGUES, HREFLANG, OG_LOCALE  # noqa: E402
ROUTES = Routes({})
DISPO = {l: set() for l in LANGUES}   # chemins FR publiés dans chaque langue
SORTIES = set()                        # adresses publiées, toutes langues
NOMS_LANGUES = {"de": "DE", "fr": "FR", "it": "IT", "en": "EN"}


def src_langue(lang):
    return SRC if lang == "fr" else os.path.join(SRC, "langues", lang)


def statut_relu(lang):
    """Vrai si toutes les pages de la langue sont marquées « relue » (src/langues/<lang>/statut.json)."""
    p = os.path.join(SRC, "langues", lang, "statut.json")
    if not os.path.exists(p):
        return False
    st = json.load(open(p, encoding="utf-8"))
    return bool(st) and all(v == "relue" for v in st.values())


def langues_actives():
    """FR, plus chaque langue qui a des sources. En production, seulement les langues entièrement relues."""
    out = ["fr"]
    for l in ("de", "it", "en"):
        if os.path.isdir(os.path.join(SRC, "langues", l, "pages")) or os.path.isdir(os.path.join(SRC, "langues", l, "data")):
            if not PRODUCTION or statut_relu(l):
                out.append(l)
    return out


def chemin_sortie(fr_path, lang):
    return ROUTES.chemin(fr_path, lang)


# ---------------------------------------------------------------- utilitaires

def read(p):
    with open(p, encoding="utf-8") as f:
        return f.read()


def write(p, s):
    os.makedirs(os.path.dirname(p), exist_ok=True)
    with open(p, "w", encoding="utf-8") as f:
        f.write(s)


def parse_front(src):
    """Front-matter en commentaire HTML au début du fichier source."""
    m = re.match(r"\s*<!--page\s*(.*?)-->\s*(.*)", src, re.S)
    if not m:
        return {}, src
    meta, body = {}, m.group(2)
    for line in m.group(1).strip().split("\n"):
        if ":" not in line:
            continue
        k, v = line.split(":", 1)
        v = v.strip()
        if v.startswith("["):
            try:
                v = json.loads(v)
            except Exception:
                pass
        meta[k.strip()] = v
    return meta, body


def rel(from_path, to_path):
    """Chemin relatif d'une page vers une autre ressource du site."""
    depth = from_path.count("/")
    return "../" * depth + to_path


def esc(s):
    return (s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
             .replace('"', "&quot;"))


# ---------------------------------------------------------------- rendu

def load_json_data(name):
    """Fichier de src/data/ lu tel quel (None s'il n'existe pas)."""
    p = os.path.join(SRC, "data", name + ".json")
    return json.load(open(p, encoding="utf-8")) if os.path.exists(p) else None


def crumbs_for(path, short, lang="fr"):
    """[(libellé, chemin FR ou None), …] du fil d'Ariane, racine exclue de la page courante."""
    if path == "fr/":
        return []
    items = [(T("Accueil"), "fr/")]
    segs = path.strip("/").split("/")[1:]
    acc = "fr"
    for i, seg in enumerate(segs):
        acc += "/" + seg
        p = acc + "/"
        last = i == len(segs) - 1
        label = short if last else PAGES.get((lang, p), {}).get("short", seg.replace("-", " ").capitalize())
        items.append((label, None if last else (p if (lang, p) in PAGES else None)))
    return items


def neutralize_links(html):
    """Un lien vers une page non encore écrite perd son href : ni cliquable, ni suivi."""
    def fix(m):
        href = m.group(1)
        target = href.split("#")[0].split("?")[0]
        logical = re.sub(r"^(\.\./)+", "", target)
        if href.startswith(("http", "mailto:", "tel:", "#", "/")) or not logical:
            return m.group(0)
        if logical in SORTIES or logical.startswith("assets/") or "assets/" in logical:
            return m.group(0)
        return '<a class="soon" aria-disabled="true" data-soon="%s" data-cible="%s"' % (T("bientôt"), logical)
    return re.sub(r'<a href="([^"]+)"', fix, html)


def selecteur(fr_path, lang, sep):
    """Liens DE · FR · IT · EN vers la même page dans chaque langue (accueil de la langue si la page n'y existe pas)."""
    liens = []
    for l in ("de", "fr", "it", "en"):
        cible = chemin_sortie(fr_path, l) if fr_path in DISPO[l] else f"{l}/"
        on = ' class="on"' if l == lang else ""
        cur = ' aria-current="true"' if l == lang else ""
        liens.append(f'<a{on} href="{{{{ROOT}}}}{cible}"{cur}>{NOMS_LANGUES[l]}</a>')
    return sep.join(liens)


def render_nav_footer(part, path, navkey, lang="fr", fr_path=None):
    """path : adresse de sortie (pour la profondeur) ; fr_path : identifiant FR de la page."""
    fr_path = fr_path or path
    part = part.replace("{{LANGUES:sep}}", selecteur(fr_path, lang, '<span class="sep">·</span>\n        '))
    part = part.replace("{{LANGUES:span}}", selecteur(fr_path, lang, "<span>·</span>\n      "))
    part, _ = localiser(part, lang, ROUTES, DISPO[lang], SITE)
    s = part.replace("{{ROOT}}", "../" * path.count("/")).replace("{{NAV}}", navkey or "")
    return neutralize_links(s)


ORG_ID = f"{SITE}/#organisation"
PAIRES_LANG = {"allemand": "de", "francais": "fr", "italien": "it", "anglais": "en"}


def entites(path, meta, short, desc):
    """Données d'entité : qui publie le site, ce que chaque page propose (accueil, à propos, services, moteur)."""
    org = json.loads(json.dumps(load_json_data("organisation")))
    # textes de l'organisation dans la langue de la page (les noms, l'adresse et le courriel ne se traduisent pas)
    org["description"] = T(org["description"])
    org["award"] = [T(a) for a in org.get("award", [])]
    for b in org.get("brand", []):
        b["description"] = T(b["description"])
    ref = {"@type": "Organization", "@id": ORG_ID, "name": org["name"], "url": org["url"]}
    out = []
    if path == "fr/":
        out.append({"@context": "https://schema.org", "@graph": [
            org, {"@type": "WebSite", "@id": f"{SITE}/#site", "url": f"{SITE}/", "name": "Neur.on",
                  "inLanguage": HREFLANG[i18n.langue()], "publisher": {"@id": ORG_ID}}]})
    elif path == "fr/a-propos/":
        out.append({"@context": "https://schema.org", "@graph": [
            org, {"@type": "AboutPage", "url": f"{SITE}/{path}", "name": meta.get("title", short),
                  "inLanguage": HREFLANG[i18n.langue()], "about": {"@id": ORG_ID}, "mainEntity": {"@id": ORG_ID}}]})
    elif path == "fr/lexmachina/":
        out.append({"@context": "https://schema.org", "@type": "SoftwareApplication", "name": "LexMachina",
                    "applicationCategory": "BusinessApplication", "operatingSystem": "Web",
                    "url": f"{SITE}/{path}", "description": desc, "inLanguage": HREFLANG[i18n.langue()], "publisher": ref})
    elif path.startswith("fr/traduction/") and path.count("/") == 3:
        slug = path.split("/")[2]
        langs = slug.split("-")
        srv = {"@context": "https://schema.org", "@type": "Service", "name": short, "description": desc,
               "serviceType": "Traduction juridique et financière", "url": f"{SITE}/{path}",
               "provider": ref, "areaServed": {"@type": "Country", "name": "Suisse"}}
        if len(langs) == 2 and all(l in PAIRES_LANG for l in langs):
            srv["availableLanguage"] = [PAIRES_LANG[l] for l in langs]
        out.append(srv)
    return [json.dumps(x, ensure_ascii=False) for x in out]


LIENS_MANQUANTS = {}   # langue -> chemins FR liés mais absents de la langue


def build_page(path, meta, body, lang="fr"):
    """path : identifiant FR terminé par / (ex. 'fr/corrext/') ; la page est écrite à son adresse dans la langue."""
    out = chemin_sortie(path, lang)
    depth = out.count("/")
    root = "../" * depth
    title = meta.get("title", meta.get("short", "Neur.on"))
    desc = meta.get("description", "")
    canonical = meta.get("canonical") or f"{SITE}/{out}"
    navkey = meta.get("nav", "")
    short = meta.get("short", title)

    # styles et JSON-LD remontés du corps vers le head
    styles = re.findall(r"<style>(.*?)</style>", body, re.S)
    body = re.sub(r"<style>.*?</style>", "", body, flags=re.S)
    lds = re.findall(r'<script type="application/ld\+json">(.*?)</script>', body, re.S)
    body = re.sub(r'<script type="application/ld\+json">.*?</script>', "", body, flags=re.S)

    # liens hérités des anciens fichiers plats
    def legacy(m):
        href, anchor = m.group(1), m.group(2) or ""
        if href in LEGACY:
            return 'href="%s%s%s"' % (root, LEGACY[href], anchor)
        return m.group(0)
    body = re.sub(r'href="([a-z0-9\-]+\.html)(#[^"]*)?"', legacy, body)
    # blog : en-tête et « derniers articles » des articles écrits à la main, tirés de src/data/blog.json
    if "{{BLOG:" in body:
        if SRC not in sys.path:
            sys.path.insert(0, SRC)
        import generators
        mots = len(re.sub(r"<[^>]+>", " ", re.sub(r"<(script|style)[\s\S]*?</\1>", "", body)).split())
        body = re.sub(r"\{\{BLOG:entete:([a-z0-9-]+)\}\}", lambda m: generators.blog_entete(src_langue(lang), m.group(1), mots), body)
        body = re.sub(r"\{\{BLOG:recents:([a-z0-9-]+)\}\}", lambda m: generators.blog_recents(src_langue(lang), m.group(1)), body)
    # liens internes : adresse FR -> adresse de la langue
    body, manq = localiser(body, lang, ROUTES, DISPO[lang], SITE)
    LIENS_MANQUANTS.setdefault(lang, set()).update(manq)
    body = body.replace('href="{{ROOT}}', 'href="' + root).replace("{{ROOT}}", root)
    # pictogrammes partagés : {{ICONE:nom}} renvoie au jeu WS_ICONS de src/generators.py
    if "{{ICONE:" in body:
        if SRC not in sys.path:
            sys.path.insert(0, SRC)
        import generators
        body = re.sub(r"\{\{ICONE:([a-z]+)\}\}", lambda m: generators.WS_ICONS[m.group(1)], body)
    # cartes de hero partagées : {{CARTE:nom}} renvoie à src/data/cartes.json
    if "{{CARTE:" in body:
        if SRC not in sys.path:
            sys.path.insert(0, SRC)
        import generators
        body = re.sub(r"\{\{CARTE:([a-z-]+)\}\}", lambda m: generators.carte(m.group(1)), body)
    body = neutralize_links(body)

    # FAQPage automatique : toute page qui pose des questions le déclare aux moteurs
    if "faq-item" in body and not any('"FAQPage"' in ld for ld in lds):
        pairs = re.findall(r'<details class="faq-item">\s*<summary>(.*?)</summary>\s*<p>(.*?)</p>',
                           body, re.S)
        def flat(x):
            x = re.sub(r"<[^>]+>", "", x)
            return re.sub(r"\s+", " ", x).replace("&nbsp;", " ").strip()
        qs = [{"@type": "Question", "name": flat(q),
               "acceptedAnswer": {"@type": "Answer", "text": flat(a)}} for q, a in pairs]
        if qs:
            lds.append(json.dumps({"@context": "https://schema.org", "@type": "FAQPage",
                                   "mainEntity": qs}, ensure_ascii=False))

    # fil d'Ariane
    items = crumbs_for(path, short, lang)
    crumb_html = ""
    if items:
        lis = []
        for label, target in items:
            if target:
                lis.append('<li><a href="%s%s">%s</a></li>' % (root, chemin_sortie(target, lang), label))
            else:
                lis.append('<li><span aria-current="page">%s</span></li>' % label)
        light = " crumbs-light" if meta.get("hero") in ("law", "read", "help") else ""
        # Centre d'aide et pages de lecture : fil d'Ariane en bandeau clair, sans héro sombre
        light = " crumbs-light crumbs-band" if meta.get("hero") == "aide" else light
        crumb_html = ('\n<nav class="crumbs%s" aria-label="%s"><div class="container"><ol>' % (light, T("Fil d'Ariane"))
                      + "".join(lis) + "</ol></div></nav>\n")
        crumb_ld = {"@context": "https://schema.org", "@type": "BreadcrumbList",
                    "itemListElement": [
                        {"@type": "ListItem", "position": i + 1, "name": label,
                         "item": f"{SITE}/{chemin_sortie(target, lang)}" if target else f"{SITE}/{out}"}
                        for i, (label, target) in enumerate(items)]}
        lds.append(json.dumps(crumb_ld, ensure_ascii=False))
    lds += entites(path, meta, short, desc)
    lds = [localiser(ld, lang, ROUTES, DISPO[lang], SITE)[0] for ld in lds]

    # image de partage : celle de l'article s'il en a une, sinon l'image de marque (1200 x 630)
    og_image = f"{SITE}/assets/img/og-neuron.jpg"
    if meta.get("image"):
        # LinkedIn lit mal le WebP : copie JPG dans assets/img/blog/og/
        jpg = "assets/img/blog/og/" + os.path.splitext(os.path.basename(meta["image"]))[0] + ".jpg"
        og_image = f"{SITE}/{jpg}" if os.path.exists(os.path.join(BASE, jpg)) else f"{SITE}/{meta['image']}"
    og_alt = meta.get("image_alt") or T("Neur.on, traduction par IA pour le droit, la fiscalité et la finance")
    lecture = re.match(r"fr/ressources/(blog|guides|etudes)/[^/]+/$", path) and path != "fr/ressources/blog/actualites/"
    og_type = "article" if lecture else "website"
    head = [
        '<!DOCTYPE html>', f'<html lang="{lang}">', '<head>',
        '<meta charset="UTF-8">',
        '<meta name="viewport" content="width=device-width, initial-scale=1.0">',
        f'<title>{title}</title>',
    ]
    if desc:
        head.append(f'<meta name="description" content="{desc}">')
    if not PRODUCTION:
        head.append('<meta name="robots" content="noindex, nofollow">')
    head += [
        f'<link rel="canonical" href="{canonical}">',
        *[f'<link rel="alternate" hreflang="{h}" href="{u}">' for h, u in alternates(path, DISPO, ROUTES, SITE)],
        f'<meta property="og:title" content="{esc(title)}">',
        f'<meta property="og:description" content="{esc(desc)}">',
        f'<meta property="og:url" content="{canonical}">',
        f'<meta property="og:type" content="{og_type}">',
        f'<meta property="og:image" content="{og_image}">',
        f'<meta property="og:image:alt" content="{esc(og_alt)}">',
        '<meta property="og:site_name" content="Neur.on">',
        f'<meta property="og:locale" content="{OG_LOCALE[lang]}">',
        '<meta name="twitter:card" content="summary_large_image">',
        '<link rel="preconnect" href="https://fonts.googleapis.com">',
        '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>',
        '<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&display=swap" rel="stylesheet">',
        f'<link rel="icon" href="{root}assets/img/favicon.ico" sizes="any">',
        f'<link rel="icon" type="image/png" href="{root}assets/img/neuron-mark.png">',
        f'<link rel="apple-touch-icon" href="{root}assets/img/neuron-mark-180.png">',
        '<meta name="theme-color" content="#001B4C">',
        f'<link rel="stylesheet" href="{root}assets/neuron.css?v={ASSET_V}">',
    ]
    for st in styles:
        head.append("<style>" + st.strip() + "</style>")
    for ld in lds:
        head.append('<script type="application/ld+json">' + ld.strip() + "</script>")
    if PRODUCTION and GSC_TOKEN:
        head.append(f'<meta name="google-site-verification" content="{GSC_TOKEN}">')
    head.append("</head>")

    def partiel(nom):
        p = os.path.join(src_langue(lang), "partials", nom)
        return read(p if os.path.exists(p) else os.path.join(SRC, "partials", nom))
    nav = render_nav_footer(partiel("nav.html"), out, navkey, lang, path)
    foot = render_nav_footer(partiel("footer.html"), out, navkey, lang, path)
    confidentialite = chemin_sortie("fr/protection-des-donnees/", lang) if "fr/protection-des-donnees/" in DISPO[lang] else "fr/protection-des-donnees/"

    scripts = [f'<script src="{root}assets/nav.js?v={ASSET_V}" defer></script>']
    if PRODUCTION and GA4_ID:
        scripts.append(f'<script src="{root}assets/consent.js?v={ASSET_V}" data-ga4="{GA4_ID}" data-privacy="{root}{confidentialite}" defer></script>')
    for a in meta.get("assets", []) or []:
        scripts.append(f'<script src="{root}assets/{a}?v={ASSET_V}"></script>')

    html = "\n".join(head) + "\n<body>\n" + nav + crumb_html + \
           '\n<main id="main">\n' + body.strip() + "\n</main>\n\n" + foot + "\n" + \
           "\n".join(scripts) + "\n</body>\n</html>\n"
    write(os.path.join(OUT, out, "index.html"), html)
    return (lang, path, out)


# ---------------------------------------------------------------- collecte

# Pages générées : fichiers de données dont dépend leur contenu (le gabarit et les partiels n'en font pas partie)
SOURCES_GENEREES = (("fr/ressources/blog/actualites/", ["src/data/actualites.json", "src/data/blog.json"]),
                    ("fr/ressources/glossaire/", ["src/data/glossaire.json"]),
                    ("fr/ressources/blog/", ["src/data/blog.json"]),
                    ("fr/solutions/", ["src/data/solutions.json"]),
                    ("fr/traduction/", ["src/data/domaines.json", "src/data/paires.json"]),
                    ("fr/aide/", ["src/data/aide.json"]))
_DATES = {}


def sources_generees(path, lang="fr"):
    fichiers = next((f for pre, f in SOURCES_GENEREES if path.startswith(pre)), [])
    return fichiers if lang == "fr" else [f.replace("src/data/", f"src/langues/{lang}/data/") for f in fichiers]


def date_contenu(fichiers):
    """Date de dernière modification réelle du contenu, pour le sitemap : dernier commit des fichiers sources,
    ou la date du jour s'ils ont des modifications non commitées. Sans source connue : date du jour."""
    if not fichiers:
        return TODAY
    dates = []
    for f in fichiers:
        if f not in _DATES:
            try:
                sale = subprocess.run(["git", "status", "--porcelain", "--", f], cwd=BASE, capture_output=True, text=True).stdout.strip()
                d = TODAY if sale else subprocess.run(["git", "log", "-1", "--format=%cs", "--", f], cwd=BASE,
                                                     capture_output=True, text=True).stdout.strip()
            except OSError:
                d = ""
            _DATES[f] = d or TODAY
        dates.append(_DATES[f])
    return max(dates)


def collect_sources(lang="fr"):
    """Pages rédigées à la main : src/pages (FR) ou src/langues/<lang>/pages, rangées sous leur chemin FR."""
    found = []
    racine = os.path.join(src_langue(lang), "pages")
    for dirpath, _dirs, files in os.walk(racine):
        if "index.html" not in files:
            continue
        rel_dir = os.path.relpath(dirpath, racine)
        path = "fr/" if rel_dir == "." else "fr/" + rel_dir.replace(os.sep, "/") + "/"
        meta, body = parse_front(read(os.path.join(dirpath, "index.html")))
        meta.setdefault("_sources", [os.path.relpath(os.path.join(dirpath, "index.html"), BASE)])
        found.append((path, meta, body))
    return found


def collect_generated(lang="fr"):
    """Pages à l'échelle produites par src/generators.py, avec les données de la langue."""
    gen_file = os.path.join(SRC, "generators.py")
    d = src_langue(lang)
    if not os.path.exists(gen_file) or not os.path.isdir(os.path.join(d, "data")):
        return []
    import importlib
    import generators
    importlib.reload(generators)
    return generators.build_all(d)


# ---------------------------------------------------------------- annexes

# Anciens fichiers de WordPress (Yoast) : leurs sitemaps et le flux renvoient vers les nouveaux équivalents
REDIR_WP = (("sitemap_index.xml", "sitemap.xml"), ("post-sitemap.xml", "sitemap.xml"), ("page-sitemap.xml", "sitemap.xml"),
            ("category-sitemap.xml", "sitemap.xml"), ("post_tag-sitemap.xml", "sitemap.xml"),
            ("author-sitemap.xml", "sitemap.xml"), ("feed/", "fr/ressources/blog/"))


def htaccess(redirections, langs=("fr",)):
    """Règles Apache (Infomaniak et la plupart des hébergeurs) : https sans www, racine vers /fr/,
    301 des anciennes adresses de neur-on.ai, page 404. Un hébergeur Nginx reprend les mêmes règles."""
    rx = lambda chemin: re.sub(r"([.+?()\[\]{}^$|])", r"\\\1", chemin.strip("/"))
    out = ["# Généré par build.py --production : ne pas modifier à la main (source : src/data/redirections.json)",
           "Options -MultiViews", "DirectorySlash On", "ErrorDocument 404 /404.html", "",
           "<IfModule mod_rewrite.c>", "RewriteEngine On", "",
           "# domaine sans www",
           "RewriteCond %{HTTP_HOST} ^www\\. [NC]", f"RewriteRule ^ {SITE}%{{REQUEST_URI}} [R=301,L,NE]",
           "# https (le second test évite une boucle derrière un proxy qui termine le TLS)",
           "RewriteCond %{HTTPS} !=on", "RewriteCond %{HTTP:X-Forwarded-Proto} !=https",
           f"RewriteRule ^ {SITE}%{{REQUEST_URI}} [R=301,L,NE]", "",
           "# racine : langue du navigateur parmi les langues publiées",
           *[x for l in langs if l != ("en" if "en" in langs else "fr")
             for x in (f"RewriteCond %{{HTTP:Accept-Language}} ^{l} [NC]", f"RewriteRule ^$ {SITE}/{l}/ [R=302,L]")],
           f"RewriteRule ^$ {SITE}/{'en' if 'en' in langs else 'fr'}/ [R=302,L]",
           '<IfModule mod_headers.c>', 'Header append Vary Accept-Language', '</IfModule>', "",
           "# anciens fichiers WordPress"]
    out += [f"RewriteRule ^{rx(a)}/?$ {SITE}/{b} [R=301,L]" for a, b in REDIR_WP]
    out += ["", "# anciennes pages de neur-on.ai (NE : garde le # des ancres)"]
    out += [f'RewriteRule ^{rx(r["ancien"])}/?$ {SITE}/{r["nouveau"].lstrip("/")} [R=301,L,NE]' for r in redirections]
    out += ["</IfModule>", "",
            "# cache : feuilles de style et scripts versionnés (?v=), images et polices",
            "<IfModule mod_expires.c>", "ExpiresActive On", 'ExpiresByType text/css "access plus 1 year"',
            'ExpiresByType application/javascript "access plus 1 year"', 'ExpiresByType image/webp "access plus 1 month"',
            'ExpiresByType image/jpeg "access plus 1 month"', 'ExpiresByType image/png "access plus 1 month"',
            'ExpiresByType image/svg+xml "access plus 1 month"', 'ExpiresByType text/html "access plus 0 seconds"', "</IfModule>",
            "<IfModule mod_deflate.c>",
            "AddOutputFilterByType DEFLATE text/html text/css application/javascript image/svg+xml application/json text/plain application/xml",
            "</IfModule>", ""]
    return "\n".join(out)


def reseau_404():
    """« 404 » dessiné en réseau de neurones : nœuds le long du tracé des chiffres, liaisons entre voisins,
    trois signaux qui parcourent les tracés (masqués si l'utilisateur réduit les animations)."""
    import math, random
    rnd = random.Random(404)
    ox, oy, H = 18, 14, 140
    traces = []
    for k, x0 in enumerate((ox, ox + 142, ox + 284)):
        if k == 1:  # le zéro : une ellipse
            traces.append(([(x0 + 50 + 46 * math.cos(t / 30 * 2 * math.pi), oy + 70 + 68 * math.sin(t / 30 * 2 * math.pi))
                            for t in range(31)], True))
        else:       # un quatre : diagonale, traverse, jambage
            traces.append(([(x0 + 72, oy + H), (x0 + 72, oy)], False))
            traces.append(([(x0 + 72, oy), (x0, oy + 94), (x0 + 104, oy + 94)], False))
    noeuds, liens, chemins = [], set(), []
    def ajoute(x, y):
        for i, (a, b) in enumerate(noeuds):
            if (a - x) ** 2 + (b - y) ** 2 < 49:
                return i
        noeuds.append((x + rnd.uniform(-1.6, 1.6), y + rnd.uniform(-1.6, 1.6)))
        return len(noeuds) - 1
    for pts, ferme in traces:
        echant = []
        for (x1, y1), (x2, y2) in zip(pts, pts[1:]):
            n = max(1, round(math.hypot(x2 - x1, y2 - y1) / 13))
            echant += [(x1 + (x2 - x1) * i / n, y1 + (y2 - y1) * i / n) for i in range(n)]
        if not ferme:
            echant.append(pts[-1])
        ids = [ajoute(x, y) for x, y in echant]
        for i, j in zip(ids, ids[1:] + ([ids[0]] if ferme else [])):
            if i != j:
                liens.add((min(i, j), max(i, j)))
        chemins.append("M" + " L".join(f"{noeuds[i][0]:.1f} {noeuds[i][1]:.1f}" for i in ids) + (" Z" if ferme else ""))
    # quelques liaisons transversales entre nœuds proches de tracés différents : l'effet « réseau »
    for i, (x, y) in enumerate(noeuds):
        proches = sorted((math.hypot(x - a, y - b), j) for j, (a, b) in enumerate(noeuds) if j != i)
        for d, j in proches[2:4]:
            if d < 30 and rnd.random() < .45:
                liens.add((min(i, j), max(i, j)))
    lignes = "".join(f'<line x1="{noeuds[i][0]:.1f}" y1="{noeuds[i][1]:.1f}" x2="{noeuds[j][0]:.1f}" y2="{noeuds[j][1]:.1f}"/>'
                     for i, j in sorted(liens))
    points = "".join(
        f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{3.3 if k % 5 == 0 else 2.2}" fill="{"#7FB0FF" if k % 5 == 0 else "#fff"}"'
        f' fill-opacity="{1 if k % 5 == 0 else .62}"/>' for k, (x, y) in enumerate(noeuds))
    signaux = "".join(
        f'<circle class="sig" r="3.6" fill="#fff" opacity="0"><animateMotion dur="{d}s" begin="{b}s" repeatCount="indefinite" path="{chemins[c]}"/>'
        f'<animate attributeName="opacity" values="0;1;1;0" keyTimes="0;.12;.85;1" dur="{d}s" begin="{b}s" repeatCount="indefinite"/></circle>'
        for c, d, b in ((1, 4.6, 0), (2, 7.5, 1.2), (4, 4.2, 2.4)))
    return ('<svg class="net" viewBox="0 0 420 170" role="img" aria-label="Le nombre 404 dessiné en réseau de neurones">'
            f'<g stroke="#96BCFF" stroke-opacity=".38" stroke-width="1">{lignes}</g><g>{points}</g><g>{signaux}</g></svg>')


def write_annexes(built):
    """built : [(langue, chemin FR, adresse publiée), …]."""
    paths = [frp for l, frp, _o in built if l == "fr"]
    langs = [l for l in ("fr", "de", "it", "en") if any(b[0] == l for b in built)]
    # racine : langue du navigateur parmi les langues publiées, anglais sinon (FR si l'anglais n'est pas encore publié)
    defaut = "en" if "en" in langs else "fr"
    liens = " · ".join(f'<a href="{l}/" hreflang="{HREFLANG[l]}">{NOMS_LANGUES[l]}</a>' for l in ("de", "fr", "it", "en") if l in langs)
    write(os.path.join(OUT, "index.html"),
          '<!DOCTYPE html>\n<html lang="en">\n<head>\n<meta charset="UTF-8">\n'
          '<meta name="robots" content="noindex">\n<title>Neur.on</title>\n'
          + "".join(f'<link rel="alternate" hreflang="{HREFLANG[l]}" href="{SITE}/{l}/">\n' for l in langs)
          + f'<link rel="alternate" hreflang="x-default" href="{SITE}/">\n'
          + '<script>(function(){var dispo=' + json.dumps(langs) + ',def="' + defaut + '";'
          + 'var nav=(navigator.languages||[navigator.language||""]).map(function(x){return String(x).slice(0,2).toLowerCase()});'
          + 'var l=nav.filter(function(x){return dispo.indexOf(x)>=0})[0]||def;location.replace(l+"/");})();</script>\n'
          + f'</head>\n<body><p>Neur.on : {liens}</p>\n<noscript><p>{liens}</p></noscript>\n</body>\n</html>\n')

    # page 404 : gabarit src/partials/404.html, servi depuis n'importe quelle profondeur (styles en ligne)
    fleche = ('<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" '
              'stroke-linejoin="round" aria-hidden="true"><path d="M5 12h14M13 6l6 6-6 6"/></svg>')
    # index des suggestions, par langue : [adresse publiée, titre]
    index = {l: [[o, re.sub(r"\s*·\s*Neur\.on$", "", PAGES[(l, p)]["title"] or PAGES[(l, p)]["short"])]
                 for ll, p, o in sorted(built) if ll == l and p not in ("fr/mentions-legales/", "fr/protection-des-donnees/")]
             for l in langs}
    liens_404 = ("fr/", "fr/corrext/", "fr/ressources/glossaire/", "fr/aide/", "fr/ressources/blog/", "fr/contact/",
                 "fr/mentions-legales/", "fr/protection-des-donnees/")
    page404 = (read(os.path.join(SRC, "partials", "404.html"))
               .replace("{{RESEAU}}", reseau_404())
               .replace("{{FEDLEX_CO}}", load_json_data("fedlex")["CO"]["url"])
               .replace("{{FLECHE_JS}}", json.dumps(fleche))
               .replace("{{FLECHE}}", fleche)
               .replace("{{TEXTES}}", json.dumps({l: v for l, v in json.load(open(os.path.join(SRC, "partials", "404-textes.json"),
                                                                                 encoding="utf-8")).items() if l in langs}, ensure_ascii=False))
               .replace("{{LIENS}}", json.dumps({l: {p: chemin_sortie(p, l) for p in liens_404 if p in DISPO[l]} for l in langs}))
               .replace("{{INDEX}}", json.dumps(index, ensure_ascii=False).replace("</", "<\\/")))
    write(os.path.join(OUT, "404.html"), page404)

    open(os.path.join(OUT, ".nojekyll"), "w").close()

    # robots
    if PRODUCTION:
        robots = read(os.path.join(SRC, "partials", "robots.production.txt"))
    else:
        robots = ("# Aperçu de travail : ne jamais indexer, pour ne pas concurrencer neur-on.ai\n"
                  "User-agent: *\nDisallow: /\n")
    write(os.path.join(OUT, "robots.txt"), robots)

    # anciennes adresses de neur-on.ai : une page de renvoi à chaque adresse (les 301 serveur viendront en production)
    red = load_json_data("redirections")
    for r in (red or {}).get("redirections", []):
        ancien, nouveau = r["ancien"].strip("/") + "/", r["nouveau"].lstrip("/")
        if ancien == "/":
            raise SystemExit("Redirection de la racine : interdite")
        if ancien in SORTIES:
            # l'ancienne adresse est redevenue une vraie page (ex. /de/impressum/) : la page prend sa place
            print(f"Redirection {ancien} ignorée : l'adresse est désormais une page du site")
            continue
        racine = "../" * ancien.count("/")
        write(os.path.join(OUT, ancien, "index.html"),
              '<!DOCTYPE html>\n<html lang="fr"><head><meta charset="UTF-8"><title>Page déplacée · Neur.on</title>'
              f'<meta name="robots" content="noindex"><link rel="canonical" href="{SITE}/{nouveau}">'
              f'<meta http-equiv="refresh" content="0; url={racine}{nouveau}">'
              f'<script>location.replace("{racine}{nouveau}"+"")</script></head>'
              f'<body><p>Cette page a déménagé : <a href="{racine}{nouveau}">voir la nouvelle adresse</a>.</p></body></html>\n')
    if PRODUCTION:
        write(os.path.join(OUT, ".htaccess"), htaccess((red or {}).get("redirections", []), langs))

    # sitemap
    prio = {"fr/": "1.0"}
    urls = []
    for l, p, o in sorted(built, key=lambda b: b[2]):
        pr = prio.get(p, "0.8" if p.count("/") <= 2 else "0.6")
        # un article garde sa date d'origine (front-matter ou générateur : lastmod), jamais celle du jour
        lm = PAGES.get((l, p), {}).get("lastmod") or TODAY
        alt = "".join(f'<xhtml:link rel="alternate" hreflang="{h}" href="{u}"/>' for h, u in alternates(p, DISPO, ROUTES, SITE))
        urls.append(f"  <url><loc>{SITE}/{o}</loc><lastmod>{lm}</lastmod><priority>{pr}</priority>{alt}</url>")
    write(os.path.join(OUT, "sitemap.xml"),
          '<?xml version="1.0" encoding="UTF-8"?>\n'
          '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml">\n'
          + "\n".join(urls) + "\n</urlset>\n")

    # llms.txt : en-tête rédigé, index des pages généré
    head = read(os.path.join(SRC, "partials", "llms-head.md"))
    groups = [
        ("Produit : la plateforme Corrext", ["fr/corrext/"]),
        ("Le moteur et la sécurité", ["fr/lexmachina/", "fr/securite-souverainete/",
                                      "fr/niveaux-de-qualite/", "fr/langues-et-formats/"]),
        ("Solutions par métier", ["fr/solutions/"]),
        ("Traduction par domaine et par langue", ["fr/traduction/"]),
        ("Comparatifs", ["fr/comparatif/"]),
        ("Ressources", ["fr/ressources/"]),
        ("Centre d'aide", ["fr/aide/"]),
        ("Entreprise", ["fr/a-propos/", "fr/contact/"]),
    ]
    used, lines = set(), []
    for titre, prefixes in groups:
        block = []
        for p in sorted(paths):
            if p in used:
                continue
            if any(p == pre or p.startswith(pre) for pre in prefixes):
                info = PAGES.get(("fr", p), {})
                label = info.get("title", p).split(" · ")[0]
                block.append(f"- [{label}]({SITE}/{p})")
                used.add(p)
        if block:
            lines.append(f"## {titre}\n\n" + "\n".join(block))
    # autres langues : une section par langue publiée
    for l, nom in (("de", "Deutsch"), ("it", "Italiano"), ("en", "English")):
        pages_l = sorted((o, PAGES[(l, p)]["title"].split(" · ")[0]) for ll, p, o in built if ll == l)
        if pages_l:
            lines.append(f"## {nom}\n\n" + "\n".join(f"- [{t}]({SITE}/{o})" for o, t in pages_l))
    write(os.path.join(OUT, "llms.txt"), head.rstrip() + "\n\n" + "\n\n".join(lines) + "\n")


def main():
    global ROUTES
    p_routes = os.path.join(SRC, "routes.json")
    ROUTES = Routes(json.load(open(p_routes, encoding="utf-8")) if os.path.exists(p_routes) else {})
    dossier_i18n = os.path.join(SRC, "i18n")
    langs = langues_actives()
    # 1. collecte de toutes les langues : il faut connaître toutes les versions avant d'écrire la moindre page
    par_langue, cles_manquantes = {}, {}
    for lang in langs:
        i18n.activer(lang, dossier_i18n)
        pages = collect_sources(lang) + collect_generated(lang)
        if lang != "fr":
            sans = sorted(p for p, _m, _b in pages if not chemin_sortie(p, lang))
            if sans:
                print(f"{lang} : {len(sans)} pages sans adresse dans src/routes.json, ignorées (ex. {sans[0]})")
            pages = [x for x in pages if chemin_sortie(x[0], lang)]
        par_langue[lang] = pages
        cles_manquantes[lang] = set(i18n.MANQUANTS)
    if PRODUCTION:
        exemples = [f"{l}:{path}" for l, pages in par_langue.items() for path, _m, body in pages if "temo-ex" in body]
        if exemples:
            sys.exit("Production refusée : témoignage d'exemple à remplacer sur " + ", ".join(exemples))
    if os.path.isdir(OUT):
        shutil.rmtree(OUT)
    os.makedirs(OUT, exist_ok=True)
    shutil.copytree(os.path.join(BASE, "assets"), os.path.join(OUT, "assets"),
                    ignore=shutil.ignore_patterns("*.map"))
    # Maquettes pour les développeurs (aperçu seulement, jamais en production)
    if not PRODUCTION and os.path.isdir(os.path.join(BASE, "maquettes")):
        shutil.copytree(os.path.join(BASE, "maquettes"), os.path.join(OUT, "maquettes"))

    # 2. registre : versions disponibles, adresses publiées, dates
    for lang, pages in par_langue.items():
        for path, meta, _body in pages:
            DISPO[lang].add(path)
            SORTIES.add(chemin_sortie(path, lang))
            PAGES[(lang, path)] = {"short": meta.get("short", path), "title": meta.get("title", ""),
                                   "lastmod": meta.get("lastmod") or date_contenu(meta.get("_sources") or sources_generees(path, lang))}

    # 3. écriture, langue par langue
    built = []
    generators = None
    if os.path.exists(os.path.join(SRC, "generators.py")):
        import generators
    for lang, pages in par_langue.items():
        i18n.activer(lang, dossier_i18n)
        if generators:
            generators.utiliser(src_langue(lang))
        built += [build_page(p, m, b, lang) for p, m, b in pages]
        cles_manquantes[lang] |= i18n.MANQUANTS
    i18n.activer("fr", dossier_i18n)
    for lang in langs:
        if lang != "fr" and cles_manquantes[lang]:
            sys.exit(f"{lang} : {len(cles_manquantes[lang])} textes d'interface sans traduction dans src/i18n/{lang}.json, "
                     "par exemple : " + " | ".join(sorted(cles_manquantes[lang])[:8]))
    write_annexes(built)

    par = {l: sum(1 for b in built if b[0] == l) for l in langs}
    print(f"{len(built)} pages générées dans docs/ ("
          + ", ".join(f"{l} {n}" for l, n in par.items()) + f" ; {'production' if PRODUCTION else 'aperçu, noindex'})")
    for lang in langs:
        if lang != "fr" and LIENS_MANQUANTS.get(lang):
            print(f"{lang} : {len(LIENS_MANQUANTS[lang])} liens vers des pages pas encore traduites (gardés en FR)")
    missing = set()
    for dirpath, _d, files in os.walk(OUT):
        for f in files:
            if not f.endswith(".html") or f == "404.html":
                continue
            missing.update(re.findall(r'data-cible="([^"]+)"', read(os.path.join(dirpath, f))))
    if missing:
        print("Pages encore à écrire (liens marqués « bientôt ») :")
        for m in sorted(missing):
            print("  ·", m)


if __name__ == "__main__":
    main()

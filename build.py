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

BASE = os.path.dirname(os.path.abspath(__file__))
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

PAGES = {}   # chemin logique ("fr/corrext/") -> {title, short, description, nav, prio}


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


def crumbs_for(path, short):
    """[(libellé, chemin ou None), …] du fil d'Ariane, racine exclue de la page courante."""
    if path == "fr/":
        return []
    items = [("Accueil", "fr/")]
    segs = path.strip("/").split("/")[1:]
    acc = "fr"
    for i, seg in enumerate(segs):
        acc += "/" + seg
        p = acc + "/"
        last = i == len(segs) - 1
        label = short if last else PAGES.get(p, {}).get("short", seg.replace("-", " ").capitalize())
        items.append((label, None if last else (p if p in PAGES else None)))
    return items


def neutralize_links(html):
    """Un lien vers une page non encore écrite perd son href : ni cliquable, ni suivi."""
    def fix(m):
        href = m.group(1)
        target = href.split("#")[0].split("?")[0]
        logical = re.sub(r"^(\.\./)+", "", target)
        if href.startswith(("http", "mailto:", "tel:", "#", "/")) or not logical:
            return m.group(0)
        if logical in PAGES or logical.startswith("assets/") or "assets/" in logical:
            return m.group(0)
        return '<a class="soon" aria-disabled="true" data-soon="bientôt" data-cible="%s"' % logical
    return re.sub(r'<a href="([^"]+)"', fix, html)


def render_nav_footer(part, path, navkey):
    s = part.replace("{{ROOT}}", "../" * path.count("/")).replace("{{NAV}}", navkey or "")
    return neutralize_links(s)


ORG_ID = f"{SITE}/#organisation"
PAIRES_LANG = {"allemand": "de", "francais": "fr", "italien": "it", "anglais": "en"}


def entites(path, meta, short, desc):
    """Données d'entité : qui publie le site, ce que chaque page propose (accueil, à propos, services, moteur)."""
    org = load_json_data("organisation")
    ref = {"@type": "Organization", "@id": ORG_ID, "name": org["name"], "url": org["url"]}
    out = []
    if path == "fr/":
        out.append({"@context": "https://schema.org", "@graph": [
            org, {"@type": "WebSite", "@id": f"{SITE}/#site", "url": f"{SITE}/", "name": "Neur.on",
                  "inLanguage": "fr-CH", "publisher": {"@id": ORG_ID}}]})
    elif path == "fr/a-propos/":
        out.append({"@context": "https://schema.org", "@graph": [
            org, {"@type": "AboutPage", "url": f"{SITE}/{path}", "name": meta.get("title", short),
                  "inLanguage": "fr-CH", "about": {"@id": ORG_ID}, "mainEntity": {"@id": ORG_ID}}]})
    elif path == "fr/lexmachina/":
        out.append({"@context": "https://schema.org", "@type": "SoftwareApplication", "name": "LexMachina",
                    "applicationCategory": "BusinessApplication", "operatingSystem": "Web",
                    "url": f"{SITE}/{path}", "description": desc, "inLanguage": "fr-CH", "publisher": ref})
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


def build_page(path, meta, body):
    """path : chemin logique terminé par / (ex. 'fr/corrext/')."""
    depth = path.count("/")
    root = "../" * depth
    title = meta.get("title", meta.get("short", "Neur.on"))
    desc = meta.get("description", "")
    canonical = meta.get("canonical") or f"{SITE}/{path}"
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
        body = re.sub(r"\{\{BLOG:entete:([a-z0-9-]+)\}\}", lambda m: generators.blog_entete(SRC, m.group(1), mots), body)
        body = re.sub(r"\{\{BLOG:recents:([a-z0-9-]+)\}\}", lambda m: generators.blog_recents(SRC, m.group(1)), body)
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
    items = crumbs_for(path, short)
    crumb_html = ""
    if items:
        lis = []
        for label, target in items:
            if target:
                lis.append('<li><a href="%s%s">%s</a></li>' % (root, target, label))
            else:
                lis.append('<li><span aria-current="page">%s</span></li>' % label)
        light = " crumbs-light" if meta.get("hero") in ("law", "read", "help") else ""
        # Centre d'aide et pages de lecture : fil d'Ariane en bandeau clair, sans héro sombre
        light = " crumbs-light crumbs-band" if meta.get("hero") == "aide" else light
        crumb_html = ('\n<nav class="crumbs%s" aria-label="Fil d\'Ariane"><div class="container"><ol>' % light
                      + "".join(lis) + "</ol></div></nav>\n")
        crumb_ld = {"@context": "https://schema.org", "@type": "BreadcrumbList",
                    "itemListElement": [
                        {"@type": "ListItem", "position": i + 1, "name": label,
                         "item": f"{SITE}/{target}" if target else f"{SITE}/{path}"}
                        for i, (label, target) in enumerate(items)]}
        lds.append(json.dumps(crumb_ld, ensure_ascii=False))
    lds += entites(path, meta, short, desc)

    # image de partage : celle de l'article s'il en a une, sinon l'image de marque (1200 x 630)
    og_image = f"{SITE}/assets/img/og-neuron.jpg"
    if meta.get("image"):
        # LinkedIn lit mal le WebP : copie JPG dans assets/img/blog/og/
        jpg = "assets/img/blog/og/" + os.path.splitext(os.path.basename(meta["image"]))[0] + ".jpg"
        og_image = f"{SITE}/{jpg}" if os.path.exists(os.path.join(BASE, jpg)) else f"{SITE}/{meta['image']}"
    og_alt = meta.get("image_alt") or "Neur.on, traduction par IA pour le droit, la fiscalité et la finance"
    lecture = re.match(r"fr/ressources/(blog|guides|etudes)/[^/]+/$", path) and path != "fr/ressources/blog/actualites/"
    og_type = "article" if lecture else "website"
    head = [
        '<!DOCTYPE html>', f'<html lang="{LANG}">', '<head>',
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
        f'<meta property="og:title" content="{esc(title)}">',
        f'<meta property="og:description" content="{esc(desc)}">',
        f'<meta property="og:url" content="{canonical}">',
        f'<meta property="og:type" content="{og_type}">',
        f'<meta property="og:image" content="{og_image}">',
        f'<meta property="og:image:alt" content="{esc(og_alt)}">',
        '<meta property="og:site_name" content="Neur.on">',
        '<meta property="og:locale" content="fr_CH">',
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

    nav = render_nav_footer(read(os.path.join(SRC, "partials", "nav.html")), path, navkey)
    foot = render_nav_footer(read(os.path.join(SRC, "partials", "footer.html")), path, navkey)

    scripts = [f'<script src="{root}assets/nav.js?v={ASSET_V}" defer></script>']
    if PRODUCTION and GA4_ID:
        scripts.append(f'<script src="{root}assets/consent.js?v={ASSET_V}" data-ga4="{GA4_ID}" data-privacy="{root}fr/protection-des-donnees/" defer></script>')
    for a in meta.get("assets", []) or []:
        scripts.append(f'<script src="{root}assets/{a}?v={ASSET_V}"></script>')

    html = "\n".join(head) + "\n<body>\n" + nav + crumb_html + \
           '\n<main id="main">\n' + body.strip() + "\n</main>\n\n" + foot + "\n" + \
           "\n".join(scripts) + "\n</body>\n</html>\n"
    write(os.path.join(OUT, path, "index.html"), html)
    return path


# ---------------------------------------------------------------- collecte

# Pages générées : fichiers de données dont dépend leur contenu (le gabarit et les partiels n'en font pas partie)
SOURCES_GENEREES = (("fr/ressources/blog/actualites/", ["src/data/actualites.json", "src/data/blog.json"]),
                    ("fr/ressources/glossaire/", ["src/data/glossaire.json"]),
                    ("fr/ressources/blog/", ["src/data/blog.json"]),
                    ("fr/solutions/", ["src/data/solutions.json"]),
                    ("fr/traduction/", ["src/data/domaines.json", "src/data/paires.json"]),
                    ("fr/aide/", ["src/data/aide.json"]))
_DATES = {}


def sources_generees(path):
    return next((f for pre, f in SOURCES_GENEREES if path.startswith(pre)), [])


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


def collect_sources():
    """Pages rédigées à la main dans src/pages."""
    found = []
    for dirpath, _dirs, files in os.walk(os.path.join(SRC, "pages")):
        if "index.html" not in files:
            continue
        rel_dir = os.path.relpath(dirpath, os.path.join(SRC, "pages"))
        path = "fr/" if rel_dir == "." else "fr/" + rel_dir.replace(os.sep, "/") + "/"
        meta, body = parse_front(read(os.path.join(dirpath, "index.html")))
        meta.setdefault("_sources", [os.path.relpath(os.path.join(dirpath, "index.html"), BASE)])
        found.append((path, meta, body))
    return found


def collect_generated():
    """Pages à l'échelle produites par src/generators.py."""
    gen_file = os.path.join(SRC, "generators.py")
    if not os.path.exists(gen_file):
        return []
    sys.path.insert(0, SRC)
    import importlib
    import generators
    importlib.reload(generators)
    return generators.build_all(SRC)


# ---------------------------------------------------------------- annexes

# Anciens fichiers de WordPress (Yoast) : leurs sitemaps et le flux renvoient vers les nouveaux équivalents
REDIR_WP = (("sitemap_index.xml", "sitemap.xml"), ("post-sitemap.xml", "sitemap.xml"), ("page-sitemap.xml", "sitemap.xml"),
            ("category-sitemap.xml", "sitemap.xml"), ("post_tag-sitemap.xml", "sitemap.xml"),
            ("author-sitemap.xml", "sitemap.xml"), ("feed/", "fr/ressources/blog/"))


def htaccess(redirections):
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
           "# racine : version française", f"RewriteRule ^$ {SITE}/fr/ [R=301,L]", "",
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


def write_annexes(paths):
    # redirection de la racine vers la langue par défaut
    write(os.path.join(OUT, "index.html"),
          '<!DOCTYPE html>\n<html lang="fr">\n<head>\n<meta charset="UTF-8">\n'
          '<meta name="robots" content="noindex">\n'
          '<meta http-equiv="refresh" content="0; url=fr/">\n'
          '<link rel="canonical" href="%s/fr/">\n<title>Neur.on</title>\n</head>\n'
          '<body><p>Redirection vers <a href="fr/">Neur.on</a>.</p>\n'
          '<script>location.replace("fr/");</script>\n</body>\n</html>\n' % SITE)

    # page 404 : servie depuis n'importe quelle profondeur, donc styles en ligne
    write(os.path.join(OUT, "404.html"),
          """<!DOCTYPE html>
<html lang="fr">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<meta name="robots" content="noindex">
<title>Page introuvable · Neur.on</title>
<style>
*{box-sizing:border-box;margin:0;padding:0}
body{font-family:'Inter',system-ui,-apple-system,sans-serif;background:linear-gradient(152deg,#0c2f7a 0%,#001B4C 54%,#001233 100%);color:#fff;min-height:100vh;display:flex;align-items:center;justify-content:center;padding:40px 24px;line-height:1.6}
.w{max-width:620px;text-align:center}
.lg{font-weight:900;font-size:26px;letter-spacing:-.03em;margin-bottom:34px;display:inline-block;color:#fff;text-decoration:none}
.lg span{color:#317BFF}
h1{font-size:clamp(28px,5vw,42px);font-weight:800;letter-spacing:-.03em;line-height:1.15;margin-bottom:16px}
p{color:rgba(255,255,255,.82);font-size:17px;margin-bottom:30px}
.b{display:inline-flex;align-items:center;gap:8px;padding:14px 24px;border-radius:10px;font-weight:600;font-size:15px;text-decoration:none;margin:0 6px 10px}
.b1{background:#1f5fd6;color:#fff}
.b2{border:1px solid rgba(255,255,255,.32);color:#fff}
</style>
</head>
<body>
<div class="w">
<a class="lg" href="/fr/">Neur<span>.</span>on</a>
<h1>Cette page n'existe pas</h1>
<p>Le lien est peut-être ancien, ou la page n'a pas encore été publiée. Reprenez depuis l'accueil ou depuis la plateforme Corrext.</p>
<a class="b b1" href="/fr/">Accueil</a><a class="b b2" href="/fr/corrext/">La plateforme Corrext</a>
</div>
<script>
/* Sur un aperçu servi dans un sous-dossier, les liens absolus sont reprefixes */
(function(){var m=location.pathname.match(/^\\/[^/]+\\//);
 if(m && m[0] !== "/fr/"){[].forEach.call(document.querySelectorAll("a[href^='/']"),function(a){
   a.setAttribute("href", m[0].replace(/\\/$/,"") + a.getAttribute("href"));});}})();
</script>
</body>
</html>
""")

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
        if ancien in paths or ancien == "/":
            raise SystemExit(f"Redirection {ancien} : l'adresse est déjà une page du site")
        racine = "../" * ancien.count("/")
        write(os.path.join(OUT, ancien, "index.html"),
              '<!DOCTYPE html>\n<html lang="fr"><head><meta charset="UTF-8"><title>Page déplacée · Neur.on</title>'
              f'<meta name="robots" content="noindex"><link rel="canonical" href="{SITE}/{nouveau}">'
              f'<meta http-equiv="refresh" content="0; url={racine}{nouveau}">'
              f'<script>location.replace("{racine}{nouveau}"+"")</script></head>'
              f'<body><p>Cette page a déménagé : <a href="{racine}{nouveau}">voir la nouvelle adresse</a>.</p></body></html>\n')
    if PRODUCTION:
        write(os.path.join(OUT, ".htaccess"), htaccess((red or {}).get("redirections", [])))

    # sitemap
    prio = {"fr/": "1.0"}
    urls = []
    for p in sorted(paths):
        pr = prio.get(p, "0.8" if p.count("/") <= 2 else "0.6")
        # un article garde sa date d'origine (front-matter ou générateur : lastmod), jamais celle du jour
        lm = PAGES.get(p, {}).get("lastmod") or TODAY
        urls.append(f"  <url><loc>{SITE}/{p}</loc><lastmod>{lm}</lastmod><priority>{pr}</priority></url>")
    write(os.path.join(OUT, "sitemap.xml"),
          '<?xml version="1.0" encoding="UTF-8"?>\n'
          '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
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
                info = PAGES.get(p, {})
                label = info.get("title", p).split(" · ")[0]
                block.append(f"- [{label}]({SITE}/{p})")
                used.add(p)
        if block:
            lines.append(f"## {titre}\n\n" + "\n".join(block))
    write(os.path.join(OUT, "llms.txt"), head.rstrip() + "\n\n" + "\n\n".join(lines) + "\n")


def main():
    pages = collect_sources() + collect_generated()
    if PRODUCTION:
        exemples = [path for path, _m, body in pages if "temo-ex" in body]
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

    for path, meta, _body in pages:
        PAGES[path] = {"short": meta.get("short", path), "title": meta.get("title", ""),
                       "lastmod": meta.get("lastmod") or date_contenu(meta.get("_sources") or sources_generees(path))}

    built = [build_page(p, m, b) for p, m, b in pages]
    write_annexes(built)

    print(f"{len(built)} pages générées dans docs/ "
          f"({'production' if PRODUCTION else 'aperçu, noindex'})")
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

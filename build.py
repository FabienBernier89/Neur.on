#!/usr/bin/env python3
"""Générateur du site Neur.on.

Sources : src/pages (pages rédigées), src/templates + src/data (pages à l'échelle),
src/partials (méga-menu et pied de page), assets/ (CSS et JS partagés).
Sortie : docs/ (servi par GitHub Pages et par le serveur local).

Usage : python3 build.py [--production]
En mode aperçu (défaut), chaque page porte noindex et robots.txt interdit tout :
l'aperçu GitHub Pages ne doit jamais concurrencer neur-on.ai dans l'index.
"""
import json, os, re, shutil, sys, datetime

BASE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(BASE, "src")
OUT = os.path.join(BASE, "docs")
SITE = "https://neur-on.ai"
LANG = "fr"
PRODUCTION = "--production" in sys.argv
TODAY = datetime.date.today().isoformat()
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
    "corrext-fast-translation.html": "fr/corrext/fast-translation/",
    "corrext-translation-project.html": "fr/corrext/translation-project/",
    "corrext-chnell.html": "fr/corrext/chnell/",
    "corrext-extraits-registre.html": "fr/corrext/extraits-registre-commerce/",
    "securite-souverainete.html": "fr/securite-souverainete/",
    "neuron-llm.html": "fr/neuron-llm/",
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


def render_nav_footer(part, path, navkey):
    s = part.replace("{{ROOT}}", "../" * path.count("/")).replace("{{NAV}}", navkey or "")
    # les liens vers des pages non encore construites ne sont pas cliquables
    def fix(m):
        href = m.group(1)
        target = href.split("#")[0]
        logical = re.sub(r"^(\.\./)+", "", target)
        if logical.startswith(("http", "mailto:", "#")) or not logical:
            return m.group(0)
        if logical in PAGES:
            return m.group(0)
        return '<a href="%s" class="soon" aria-disabled="true" tabindex="-1" data-soon="bientôt"' % href
    return re.sub(r'<a href="([^"]+)"', fix, s)


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
    body = body.replace('href="{{ROOT}}', 'href="' + root).replace("{{ROOT}}", root)

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
        crumb_html = ('\n<nav class="crumbs" aria-label="Fil d\'Ariane"><div class="container"><ol>'
                      + "".join(lis) + "</ol></div></nav>\n")
        crumb_ld = {"@context": "https://schema.org", "@type": "BreadcrumbList",
                    "itemListElement": [
                        {"@type": "ListItem", "position": i + 1, "name": label,
                         "item": f"{SITE}/{target}" if target else f"{SITE}/{path}"}
                        for i, (label, target) in enumerate(items)]}
        lds.append(json.dumps(crumb_ld, ensure_ascii=False))

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
        '<meta property="og:type" content="website">',
        '<meta property="og:site_name" content="Neur.on">',
        '<meta property="og:locale" content="fr_CH">',
        '<meta name="twitter:card" content="summary_large_image">',
        '<link rel="preconnect" href="https://fonts.googleapis.com">',
        '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>',
        '<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&display=swap" rel="stylesheet">',
        f'<link rel="icon" type="image/svg+xml" href="{root}assets/favicon.svg">',
        f'<link rel="apple-touch-icon" href="{root}assets/favicon.svg">',
        '<meta name="theme-color" content="#001B4C">',
        f'<link rel="stylesheet" href="{root}assets/neuron.css?v={ASSET_V}">',
    ]
    for st in styles:
        head.append("<style>" + st.strip() + "</style>")
    for ld in lds:
        head.append('<script type="application/ld+json">' + ld.strip() + "</script>")
    head.append("</head>")

    nav = render_nav_footer(read(os.path.join(SRC, "partials", "nav.html")), path, navkey)
    foot = render_nav_footer(read(os.path.join(SRC, "partials", "footer.html")), path, navkey)

    scripts = [f'<script src="{root}assets/nav.js?v={ASSET_V}" defer></script>']
    for a in meta.get("assets", []) or []:
        scripts.append(f'<script src="{root}assets/{a}?v={ASSET_V}"></script>')

    html = "\n".join(head) + "\n<body>\n" + nav + crumb_html + \
           '\n<main id="main">\n' + body.strip() + "\n</main>\n\n" + foot + "\n" + \
           "\n".join(scripts) + "\n</body>\n</html>\n"
    write(os.path.join(OUT, path, "index.html"), html)
    return path


# ---------------------------------------------------------------- collecte

def collect_sources():
    """Pages rédigées à la main dans src/pages."""
    found = []
    for dirpath, _dirs, files in os.walk(os.path.join(SRC, "pages")):
        if "index.html" not in files:
            continue
        rel_dir = os.path.relpath(dirpath, os.path.join(SRC, "pages"))
        path = "fr/" if rel_dir == "." else "fr/" + rel_dir.replace(os.sep, "/") + "/"
        meta, body = parse_front(read(os.path.join(dirpath, "index.html")))
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

    # sitemap
    prio = {"fr/": "1.0"}
    urls = []
    for p in sorted(paths):
        pr = prio.get(p, "0.8" if p.count("/") <= 2 else "0.6")
        urls.append(f"  <url><loc>{SITE}/{p}</loc><lastmod>{TODAY}</lastmod><priority>{pr}</priority></url>")
    write(os.path.join(OUT, "sitemap.xml"),
          '<?xml version="1.0" encoding="UTF-8"?>\n'
          '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
          + "\n".join(urls) + "\n</urlset>\n")

    # llms.txt : en-tête rédigé, index des pages généré
    head = read(os.path.join(SRC, "partials", "llms-head.md"))
    groups = [
        ("Produit : la plateforme Corrext", ["fr/corrext/"]),
        ("Le moteur et la sécurité", ["fr/neuron-llm/", "fr/securite-souverainete/",
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
    if os.path.isdir(OUT):
        shutil.rmtree(OUT)
    os.makedirs(OUT, exist_ok=True)
    shutil.copytree(os.path.join(BASE, "assets"), os.path.join(OUT, "assets"),
                    ignore=shutil.ignore_patterns("*.map"))

    pages = collect_sources() + collect_generated()
    for path, meta, _body in pages:
        PAGES[path] = {"short": meta.get("short", path), "title": meta.get("title", "")}

    built = [build_page(p, m, b) for p, m, b in pages]
    write_annexes(built)

    print(f"{len(built)} pages générées dans docs/ "
          f"({'production' if PRODUCTION else 'aperçu, noindex'})")
    missing = set()
    for dirpath, _d, files in os.walk(OUT):
        for f in files:
            if not f.endswith(".html") or f == "404.html":
                continue
            for href in re.findall(r'href="((?:\.\./)*[^":#]*/)"', read(os.path.join(dirpath, f))):
                logical = re.sub(r"^(\.\./)+", "", href)
                if logical and not logical.startswith(("http", "/")) and logical not in PAGES:
                    missing.add(logical)
    if missing:
        print("Pages encore à écrire (liens marqués « bientôt ») :")
        for m in sorted(missing):
            print("  ·", m)


if __name__ == "__main__":
    main()

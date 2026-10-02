"""Découpe des sources FR en segments à traduire, et réinjection des traductions.

Un segment est un passage de texte continu : le contenu d'un bloc (p, li, h2, td, text de SVG…) avec ses balises
en ligne, la valeur d'un attribut lisible (alt, aria-label, title, placeholder), une valeur du front-matter
(title, description, short), une chaîne d'un JSON de données ou d'un JSON-LD écrit dans la page.
Les balises en ligne et les jetons {{…}} sont remplacés par des marqueurs {n}…{/n} ou {n}, que LexMachina
restitue intacts (voir outils/CORREXT-MT.md)."""
import copy, html, json, re

EN_LIGNE = {"a", "strong", "b", "em", "i", "mark", "span", "abbr", "br", "q", "code", "small", "sup", "sub",
            "time", "u", "s", "tspan", "kbd"}
VIDES = {"br", "img", "wbr"}
ATTRS = ("alt", "aria-label", "title", "placeholder")
FRONT = ("title", "description", "short")
# clés JSON jamais traduites : identifiants, chemins, dimensions, équivalents officiels déjà fixés
TECH = {"slug", "icone", "vis", "href", "url", "src", "date", "maj", "w", "h", "voisins", "id", "ancre", "image",
        "vignette", "lien", "de", "fr", "it", "en", "exemple", "cle", "nav", "hero", "lastmod", "categorie",
        "sous_categorie", "auteur", "auteur_personne", "mentions", "date_affichee", "u", "outil", "espace",
        "temoignage_exemple", "exemple_flag", "type", "langues"}
LETTRE = re.compile(r"[A-Za-zÀ-ÖØ-öø-ÿ]")
JETON = re.compile(r"\{\{[^}]+\}\}")
CHEMIN = re.compile(r"^(https?:|mailto:|tel:|/|\{\{ROOT\}\}|fr/|assets/|#)")


def _nom(tag):
    m = re.match(r"</?\s*([a-zA-Z0-9-]+)", tag)
    return m.group(1).lower() if m else ""


def proteger(fragment):
    """HTML en ligne -> (texte à traduire avec marqueurs, table des marqueurs)."""
    jetons = re.findall(r"\{\{[^}]+\}\}|<[^>]+>|[^<{]+|[<{]", fragment)
    sortie, table, pile, n = [], {}, [], 0
    # numérotation : une ouverture ou un élément vide prend un numéro ; la fermeture reprend celui de l'ouverture
    fermees = set()
    ouvertures = []
    for i, j in enumerate(jetons):
        if j.startswith("<") and not j.startswith("</") and _nom(j) not in VIDES and not j.endswith("/>"):
            ouvertures.append(i)
    appariement = {}
    for i, j in enumerate(jetons):
        if j.startswith("</"):
            nom = _nom(j)
            for k in range(len(pile) - 1, -1, -1):
                if _nom(jetons[pile[k]]) == nom:
                    appariement[pile[k]] = i
                    fermees.add(i)
                    del pile[k:]
                    break
        elif j.startswith("<") and i in ouvertures:
            pile.append(i)
    num = {}
    for i, j in enumerate(jetons):
        if JETON.fullmatch(j) or (j.startswith("<") and not j.startswith("</")):
            n += 1
            num[i] = n
            if i in appariement:
                table[n] = {"ouvre": j, "ferme": jetons[appariement[i]]}
                num[appariement[i]] = n
                sortie.append("{%d}" % n)
            else:
                table[n] = {"vide": j}
                sortie.append("{%d}" % n)
        elif j.startswith("</"):
            if i in fermees:
                sortie.append("{/%d}" % num[i])
            else:  # fermeture orpheline : élément vide
                n += 1
                table[n] = {"vide": j}
                sortie.append("{%d}" % n)
        else:
            sortie.append(html.unescape(j))
    return "".join(sortie), table


_MARQ = re.compile(r"\{\s*(/?)\s*(\d+)\s*\}")


def restaurer(texte, table):
    """Texte traduit avec marqueurs -> HTML. Lève ValueError si un marqueur manque, est en double ou dans le désordre."""
    vus = {}
    for m in _MARQ.finditer(texte):
        vus.setdefault((m.group(1), int(m.group(2))), []).append(m.start())
    for n, e in table.items():
        if "vide" in e:
            if len(vus.get(("", n), [])) != 1:
                raise ValueError(f"marqueur {{{n}}} absent ou en double")
        else:
            o, f = vus.get(("", n), []), vus.get(("/", n), [])
            if len(o) != 1 or len(f) != 1 or o[0] > f[0]:
                raise ValueError(f"marqueurs {{{n}}}…{{/{n}}} absents, en double ou inversés")
    if any(int(m.group(2)) not in table for m in _MARQ.finditer(texte)):
        raise ValueError("marqueur inconnu")
    # espaces ajoutées par le moteur à l'intérieur d'une paire
    texte = re.sub(r"\{\s*(\d+)\s*\}(?=\S)|\{\s*(\d+)\s*\}\s+", lambda m: _ouvre(m, table), texte)
    texte = re.sub(r"\s+\{\s*/\s*(\d+)\s*\}|\{\s*/\s*(\d+)\s*\}", lambda m: "{/%s}" % (m.group(1) or m.group(2)), texte)
    morceaux, pos = [], 0
    for m in re.finditer(r"\{(/?)(\d+)\}", texte):
        morceaux.append(html.escape(texte[pos:m.start()], quote=False))
        e = table[int(m.group(2))]
        morceaux.append(e["vide"] if "vide" in e else (e["ferme"] if m.group(1) else e["ouvre"]))
        pos = m.end()
    morceaux.append(html.escape(texte[pos:], quote=False))
    return "".join(morceaux)


def _ouvre(m, table):
    n = int(m.group(1) or m.group(2))
    garde = "" if "vide" not in table[n] or m.group(1) else (" " if m.group(0).endswith(" ") else "")
    return "{%d}" % n + garde


def _a_du_texte(fragment):
    t = JETON.sub("", re.sub(r"<[^>]+>", "", fragment))
    return bool(LETTRE.search(html.unescape(t)))


def extraire_html(source):
    """Segments d'une page source (front-matter, blocs, attributs lisibles, JSON-LD)."""
    unites = []

    def ajoute(genre, debut, fin):
        brut = source[debut:fin]
        if genre in ("bloc",):
            texte, table = proteger(brut)
        elif genre == "ld":
            texte, table = json.loads('"' + brut + '"'), {}
        else:
            texte, table = html.unescape(brut), {}
        unites.append({"id": str(len(unites) + 1), "genre": genre, "debut": debut, "fin": fin,
                       "html": brut, "texte": texte, "table": table})

    corps = 0
    fm = re.match(r"\s*<!--page\s*(.*?)-->", source, re.S)
    if fm:
        for m in re.finditer(r"^(\w+):[ \t]*(.*)$", fm.group(1), re.M):
            if m.group(1) in FRONT and LETTRE.search(m.group(2)):
                ajoute("front", fm.start(1) + m.start(2), fm.start(1) + m.end(2))
        corps = fm.end()
    jetons = re.finditer(r"<!--.*?-->|<(script|style)\b[^>]*>.*?</\1\s*>|<[^>]+>|[^<]+", source[corps:], re.S)
    run = []

    def vide_run():
        if not run:
            return
        d, f = run[0][0], run[-1][1]
        while d < f and source[d].isspace():
            d += 1
        while f > d and source[f - 1].isspace():
            f -= 1
        if _a_du_texte(source[d:f]):
            ajoute("bloc", d, f)
        run.clear()

    for m in jetons:
        d, f, j = corps + m.start(), corps + m.end(), m.group(0)
        if j.startswith("<!--"):
            vide_run()
            continue
        if m.group(1):  # script ou style
            vide_run()
            if m.group(1).lower() == "script" and "application/ld+json" in j[:80]:
                for s in re.finditer(r'"(name|text|description|headline|alternateName|caption)"\s*:\s*"((?:[^"\\]|\\.)*)"', j):
                    if LETTRE.search(s.group(2)):
                        ajoute("ld", d + s.start(2), d + s.end(2))
            continue
        if j.startswith("<"):
            for a in re.finditer(r'\s(%s)="([^"]*)"' % "|".join(ATTRS), j):
                if LETTRE.search(a.group(2)) and not CHEMIN.match(a.group(2)):
                    ajoute("attr", d + a.start(2), d + a.end(2))
            if _nom(j) in EN_LIGNE:
                run.append((d, f))
            else:
                vide_run()
        else:
            run.append((d, f))
    vide_run()
    unites.sort(key=lambda u: u["debut"])
    for i, u in enumerate(unites, 1):
        u["id"] = str(i)
    return unites


def reinjecter_html(source, traductions):
    """traductions : {id: html traduit (déjà restauré)}. Les segments absents gardent le texte FR."""
    out = source
    for u in sorted(extraire_html(source), key=lambda u: -u["debut"]):
        t = traductions.get(u["id"])
        if t is None:
            continue
        if u["genre"] == "front":
            t = " ".join(t.split())
        elif u["genre"] == "attr":
            t = html.escape(t, quote=True)
        elif u["genre"] == "ld":
            t = json.dumps(t, ensure_ascii=False)[1:-1]
        out = out[:u["debut"]] + t + out[u["fin"]:]
    return out


def scripts_a_traduire(source):
    """Vrai si un script (hors JSON-LD) contient des chaînes de texte à traduire à la main."""
    for m in re.finditer(r"<script\b([^>]*)>(.*?)</script>", source, re.S):
        if "ld+json" in m.group(1):
            continue
        if re.search(r"""(['"`])(?=[^'"`\n]*\s)(?=[^'"`\n]*[A-Za-zÀ-ÿ]{3})[^'"`\n]{4,}\1""", m.group(2)):
            return True
    return False


def _parcours(o, chemin, fichier, unites):
    if isinstance(o, dict):
        for k, v in o.items():
            if k in TECH:
                continue
            _parcours(v, chemin + (k,), fichier, unites)
    elif isinstance(o, list):
        for i, v in enumerate(o):
            _parcours(v, chemin + (i,), fichier, unites)
    elif isinstance(o, str) and LETTRE.search(o) and not CHEMIN.match(o):
        texte, table = proteger(o)
        unites.append({"id": fichier + ":" + "/".join(map(str, chemin)), "chemin": chemin, "genre": "json",
                       "html": o, "texte": texte, "table": table})


def extraire_json(data, fichier):
    unites = []
    _parcours(data, (), fichier, unites)
    return unites


def reinjecter_json(data, traductions):
    out = copy.deepcopy(data)
    fichier = None
    for u in extraire_json(data, "_"):
        cle = u["id"].split(":", 1)[1]
        t = next((v for k, v in traductions.items() if k.split(":", 1)[-1] == cle), None)
        if t is None:
            continue
        cible = out
        for p in u["chemin"][:-1]:
            cible = cible[p]
        cible[u["chemin"][-1]] = t
    return out

"""Contrôle automatique des traductions du site, à lancer avant d'intégrer un lot traduit.

  python3 outils/controle_traductions.py de                          tout le contenu allemand
  python3 outils/controle_traductions.py de --seulement pages/corrext  fichiers dont le chemin contient ce motif

Chaque source traduite (src/langues/<lang>/pages, data et partials, plus src/i18n/<lang>.json) est comparée à son
original FR. Le rapport est trié par fichier et suivi d'un résumé par règle. Code de sortie 1 s'il reste un bloquant.

Règles (Tâche 6 du plan docs/superpowers/plans/2026-10-02-neuron-site-multilingue.md) :
  structure  bloquant       fichiers attendus présents, mêmes clés et longueurs de listes, valeurs techniques intactes
  balises    bloquant       même suite de balises, mêmes href/src et jetons {{…}} ; script modifié : avertissement
  restes_fr  bloquant       texte de plus de 12 mots dont plus de 8 % de mots outils français
  eszett     bloquant       ß dans un fichier DE (sauf un mot que la source FR cite déjà tel quel)
  tirets     bloquant       tiret cadratin ou demi-cadratin, n'importe où
  produits   bloquant       nom de produit perdu, ajouté ou de casse modifiée (écart d'une occurrence : avertissement)
  seo        avertissement  title hors de 30 à 62 caractères, description hors de 110 à 160
  termes     avertissement  terme FR de src/i18n/termes-<lang>.json sans son équivalent dans le segment traduit"""
import argparse, fnmatch, glob, html, json, os, re, sys
from collections import Counter, defaultdict

ICI = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.dirname(ICI)
sys.path.insert(0, ICI)
import segments as S  # noqa: E402

BLOQUANT, AVERT = "bloquant", "avertissement"
REGLES = ("structure", "balises", "restes_fr", "eszett", "tirets", "produits", "seo", "termes")
PARTIELS = ("nav.html", "footer.html")
# données propres au FR, jamais traduites (même liste que pont_corrext.sources) : tolérées dans une langue, pas exigées
NON_TRADUITS = ("redirections.json", "fedlex.json", "organisation.json")
STATUT = "statut_traduction"  # seule clé de front-matter propre à une page traduite

MOTS_OUTILS = {"le", "la", "les", "des", "une", "pour", "avec", "dans", "est", "sont", "qui", "que", "nous", "vous",
               "aux", "du", "au", "sur"}
# mots outils français qui sont aussi des mots courants de la langue cible : non comptés dans cette langue
AMBIGUS = {"de": {"des"}, "it": {"la", "le", "qui"}}
# petits mots qui relient les éléments d'un nom propre (« Banque Cantonale du Valais »)
LIAISONS = MOTS_OUTILS | {"de", "d", "l", "et"}
SEUIL_MOTS, SEUIL_TAUX = 12, 0.08

PRODUITS = sorted(("Neur.on", "Corrext", "LexMachina", "CHnell", "Fast lookup CHnell", "Highly sensitive content",
                   "Infomaniak"), key=len, reverse=True)  # du plus long au plus court : « CHnell » seul après « Fast lookup CHnell »
BORNES = {"title": (30, 62), "description": (110, 160)}
TIRETS = {"\u2014": "tiret cadratin (U+2014)", "\u2013": "demi-cadratin (U+2013)"}
GENRES = {"front": "front-matter", "bloc": "texte", "attr": "attribut", "ld": "JSON-LD"}
MAX_LIGNES = 20  # lignes affichées par fichier et par règle dans le rapport (le résumé compte tout)

_MOT = re.compile(r"[^\W\d_]+(?:['’][^\W\d_]+)*")
_MARQ = re.compile(r"\{/?\d+\}")
_JETONS = re.compile(r"\{\{[^}]+\}\}|\{/?\d+\}")
_BALISE = re.compile(r"<!--.*?-->|<(script|style)\b([^>]*)>(.*?)</\1\s*>|<(/?)([A-Za-z][\w:.-]*)[^>]*>", re.S | re.I)
_LIEN = re.compile(r"""\s(href|src)\s*=\s*(?:"([^"]*)"|'([^']*)')""", re.I)
_LIEN_LD = re.compile(r'"((?:https?:|mailto:|tel:|\{\{ROOT\}\}|/|fr/|assets/|#)[^"]*)"')
_LITTERAL = re.compile(r"""(['"`])((?=[^'"`\n]*\s)(?=[^'"`\n]*[A-Za-zÀ-ÿ]{3})[^'"`\n]{4,})\1""")
_LANG_FR = re.compile(r"""<([A-Za-z][\w-]*)\b[^>]*?\slang\s*=\s*["']fr(?:-[A-Za-z]+)?["'][^>]*>""", re.I)
_FM = re.compile(r"\s*<!--page\s*(.*?)-->", re.S)
_ESZETT = re.compile(r"[^\W\d_]*ß[^\W\d_]*")


# ---------- outils communs ----------

def _pb(fichier, gravite, regle, detail):
    return {"fichier": fichier, "gravite": gravite, "regle": regle, "detail": detail}


def _visible(t):
    """Texte affichable : les tirets interdits sont remplacés par leur code."""
    for c in TIRETS:
        t = t.replace(c, "[U+%04X]" % ord(c))
    return t


def _extrait(t, n=70):
    t = " ".join(str(t).split())
    return _visible(t if len(t) <= n else t[:n - 1] + "…")


def _autour(t, c):
    i = t.index(c)
    return _extrait(t[max(0, i - 35):i + 35])


def _plat(texte):
    """Texte d'un segment sans marqueurs {n} ni jetons {{…}}."""
    # un marqueur peut venir d'un paragraphe (<p> dans une chaîne JSON) : il sépare les mots
    return " ".join(_MARQ.sub(" ", S.JETON.sub(" ", texte)).split())


_BLOC = re.compile(r"</?(?:p|div|li|ul|ol|h[1-6]|br|td|th|tr|table|section|article|header|footer|nav|dt|dd|dl|"
                   r"blockquote|figcaption|summary|details|aside|main)\b[^>]*>", re.I)


def _texte_fragment(fragment):
    # une balise de bloc sépare deux mots ; une balise en ligne ne sépare rien (« Corr<b>ext</b> »)
    return _plat(html.unescape(re.sub(r"<[^>]+>", "", _BLOC.sub(" ", fragment))))


def _lieu(chemin, racine=None):
    """Chemin lisible dans un JSON, avec le slug de l'entrée quand il existe : « 3 (kuendigung)/faq/0/q »."""
    parts = [str(c) for c in chemin]
    if chemin and isinstance(racine, list) and isinstance(chemin[0], int) and chemin[0] < len(racine) \
            and isinstance(racine[chemin[0]], dict) and racine[chemin[0]].get("slug"):
        parts[0] = f"{chemin[0]} ({racine[chemin[0]]['slug']})"
    return "/".join(parts) or "(racine)"


def _sans_fr(txt):
    """Vide le contenu des éléments marqués lang="fr" : citations françaises volontaires."""
    pos = 0
    while True:
        m = _LANG_FR.search(txt, pos)
        if not m:
            return txt
        nom, pos = m.group(1).lower(), m.end()
        if nom in S.VIDES or nom == "html" or m.group(0).endswith("/>"):
            continue
        prof = 1
        for b in re.compile(r"<(/?)%s\b[^>]*>" % re.escape(nom), re.I).finditer(txt, pos):
            prof += -1 if b.group(1) else 1
            if prof == 0:
                txt = txt[:pos] + txt[b.start():]
                break


def _front(txt):
    m = _FM.match(txt)
    if not m:
        return None
    return {k: v.strip() for k, v in re.findall(r"^(\w+):[ \t]*(.*)$", m.group(1), re.M)}


# ---------- règles ----------

def _restes_fr(texte, lang):
    """(mots outils comptés, mots) si le texte semble resté en français, sinon None."""
    mots = [(m.group(0), m.start()) for m in _MOT.finditer(texte)]
    if len(mots) <= SEUIL_MOTS:
        return None
    outils = MOTS_OUTILS - AMBIGUS.get(lang, set())
    n = 0
    for i, (mot, debut) in enumerate(mots):
        if mot.lower() not in outils:
            continue
        if mot[0].isupper() and not _debut_de_phrase(texte, debut):
            continue  # nom propre : La Poste, Le Temps
        if _entre_noms_propres(mots, i):
            continue  # nom propre : Banque Cantonale du Valais
        n += 1
    return (n, len(mots)) if n / len(mots) > SEUIL_TAUX else None


def _debut_de_phrase(texte, debut):
    avant = texte[:debut].rstrip(" «“\"'( ")
    return not avant or avant[-1] in ".!?:"


def _entre_noms_propres(mots, i):
    g = i - 1
    while g >= 0 and mots[g][0].lower() in LIAISONS:
        g -= 1
    d = i + 1
    while d < len(mots) and mots[d][0].lower() in LIAISONS:
        d += 1
    return g >= 0 and d < len(mots) and mots[g][0][0].isupper() and mots[d][0][0].isupper()


def _eszett(fr, tr, fichier, lang):
    if lang != "de":
        return []
    trop = Counter(_ESZETT.findall(tr)) - Counter(_ESZETT.findall(fr))
    return [_pb(fichier, BLOQUANT, "eszett", f"« {mot} » ({n} fois) : pas de ß en allemand de Suisse, écrire « "
                                             f"{mot.replace('ß', 'ss')} »") for mot, n in sorted(trop.items())]


def _tirets_lignes(txt, fichier):
    out = []
    for no, ligne in enumerate(txt.splitlines(), 1):
        for c, nom in TIRETS.items():
            if c in ligne:
                n = ligne.count(c)
                out.append(_pb(fichier, BLOQUANT, "tirets",
                               f"ligne {no} : {nom}{f' ({n} fois)' if n > 1 else ''} : « {_autour(ligne, c)} »"))
    return out


def _tirets_chaine(t, fichier, lieu):
    return [_pb(fichier, BLOQUANT, "tirets", f"{lieu} : {nom} : « {_autour(t, c)} »")
            for c, nom in TIRETS.items() if c in t]


def _produits(fr, tr, fichier, pre=""):
    out = []
    for nom in PRODUITS:
        motif = re.compile(r"(?<![A-Za-z0-9./@])%s(?![A-Za-z0-9])(?!\.[a-z]{2,3}\b)" % re.escape(nom), re.I)
        fa = Counter(m.group(0) for m in motif.finditer(fr))
        fb = Counter(m.group(0) for m in motif.finditer(tr))
        fr, tr = motif.sub(" ", fr), motif.sub(" ", tr)
        for forme in sorted(fb):
            if forme not in fa and forme != nom:
                out.append(_pb(fichier, BLOQUANT, "produits", f"{pre}casse modifiée : « {forme} » au lieu de « {nom} »"))
        na, nb = sum(fa.values()), sum(fb.values())
        if na != nb:
            out.append(_pb(fichier, BLOQUANT if abs(na - nb) > 1 else AVERT, "produits",
                           f"{pre}« {nom} » : {na} dans la source, {nb} dans la traduction"))
    return out


def _seo(cle, valeur, fichier, pre):
    mini, maxi = BORNES[cle]
    n = len(html.unescape(re.sub(r"<[^>]+>", "", valeur)).strip())
    if mini <= n <= maxi:
        return []
    return [_pb(fichier, AVERT, "seo", f"{pre}{cle} de {n} caractères (attendu : {mini} à {maxi}) : « {_extrait(valeur)} »")]


def _charger_termes(base, lang):
    rel = f"src/i18n/termes-{lang}.json"
    p = os.path.join(base, rel)
    if not os.path.exists(p):
        return [], []
    try:
        data = json.load(open(p, encoding="utf-8"))
    except ValueError as e:
        return [], [_pb(rel, AVERT, "termes", f"base terminologique illisible : {e}")]
    termes = [(t["fr"].strip(), t[lang].strip()) for t in data if isinstance(t, dict)
              and isinstance(t.get("fr"), str) and isinstance(t.get(lang), str) and t["fr"].strip() and t[lang].strip()]
    return termes, []


def _termes(paires, termes, fichier):
    """paires : [(lieu, texte FR, texte traduit)] de segments correspondants."""
    out = []
    for fr, eq in termes:
        if fr.isupper() and len(fr) <= 6:
            # sigle (CO, PA, FF) : mot entier, casse exacte, sans pluriel
            motif = re.compile(r"(?<![^\W\d_])" + re.escape(fr) + r"(?![^\W\d_])")
        else:
            motif = re.compile(r"(?<![^\W\d_])" + r"[sx]?\s+".join(re.escape(m) for m in fr.split()) + r"[sx]?(?![^\W\d_])",
                               re.I)
        mots = _MOT.findall(eq)
        prefixes = [m[:5].casefold() for m in ([m for m in mots if len(m) >= 3] or mots)]
        for lieu, a, b in paires:
            if motif.search(a) and not all(p in b.casefold() for p in prefixes):
                out.append(_pb(fichier, AVERT, "termes", f"{lieu} : « {fr} » sans « {eq} » : « {_extrait(b)} »"))
    return out


# ---------- balises ----------

def _liens(balise, i):
    return [(i, m.group(1).lower(), m.group(2) if m.group(2) is not None else m.group(3)) for m in _LIEN.finditer(balise)]


def _analyse(txt):
    """Suite des balises, liens href/src, jetons, scripts et JSON-LD d'un document ou d'un fragment HTML.
    Commentaires ignorés ; contenu des style et des scripts hors JSON-LD mis à part."""
    a = {"noms": [], "liens": [], "scripts": [], "ld": []}
    hors, pos = [], 0
    for m in _BALISE.finditer(txt):
        hors.append(txt[pos:m.start()])
        pos = m.end()
        if m.group(0).startswith("<!--"):
            continue
        i = len(a["noms"])
        if m.group(1):
            nom = m.group(1).lower()
            ouvrante = "<%s%s>" % (m.group(1), m.group(2))
            a["noms"] += [nom, "/" + nom]
            a["liens"] += _liens(ouvrante, i)
            hors.append(ouvrante)
            if nom == "script":
                if "ld+json" in m.group(2).lower():
                    a["ld"].append(m.group(3))
                    hors.append(m.group(3))
                else:
                    a["scripts"].append(m.group(3))
            continue
        a["noms"].append(m.group(4) + m.group(5).lower())
        a["liens"] += _liens(m.group(0), i)
        hors.append(m.group(0))
    hors.append(txt[pos:])
    a["jetons"] = Counter(_JETONS.findall("".join(hors)))
    return a


def _comparer_balises(fr, tr, fichier, lieu=""):
    out = []
    pre = lieu + " : " if lieu else ""
    a, b = _analyse(fr), _analyse(tr)
    bl = lambda d: out.append(_pb(fichier, BLOQUANT, "balises", pre + d))
    av = lambda d: out.append(_pb(fichier, AVERT, "balises", pre + d))
    if a["noms"] != b["noms"]:
        na, nb = a["noms"], b["noms"]
        i = next((k for k, (x, y) in enumerate(zip(na, nb)) if x != y), min(len(na), len(nb)))
        att = "<%s>" % na[i] if i < len(na) else "fin du texte"
        tro = "<%s>" % nb[i] if i < len(nb) else "fin du texte"
        bl(f"suite de balises différente à la balise n° {i + 1} : {att} attendu, {tro} trouvé "
           f"(source : {len(na)} balises, traduction : {len(nb)})")
        ca, cb = Counter((x, v) for _, x, v in a["liens"]), Counter((x, v) for _, x, v in b["liens"])
        for (x, v), n in sorted((ca - cb).items()):
            bl(f"{x} absent ou modifié : « {v} »")
        for (x, v), n in sorted((cb - ca).items()):
            bl(f"{x} inattendu : « {v} »")
    else:
        da = {(i, x): v for i, x, v in a["liens"]}
        db = {(i, x): v for i, x, v in b["liens"]}
        for k in sorted(set(da) | set(db)):
            if da.get(k) != db.get(k):
                bl(f"{k[1]} modifié sur la balise n° {k[0] + 1} <{a['noms'][k[0]]}> : « {da.get(k, '(absent)')} » "
                   f"attendu, « {db.get(k, '(absent)')} » trouvé")
    for j, n in sorted((a["jetons"] - b["jetons"]).items()):
        bl(f"jeton {j} absent ({n} de moins que la source)")
    for j, n in sorted((b["jetons"] - a["jetons"]).items()):
        bl(f"jeton {j} en trop ({n} de plus que la source)")
    for k, (x, y) in enumerate(zip(a["ld"], b["ld"]), 1):
        try:
            json.loads(x)
            source_valide = True
        except ValueError:
            source_valide = False
        if source_valide:
            try:
                json.loads(y)
            except ValueError as e:
                bl(f"JSON-LD n° {k} invalide : {e}")
        la, lb = Counter(_LIEN_LD.findall(x)), Counter(_LIEN_LD.findall(y))
        for v in sorted(la - lb):
            bl(f"lien du JSON-LD n° {k} absent ou modifié : « {v} »")
        for v in sorted(lb - la):
            bl(f"lien du JSON-LD n° {k} inattendu : « {v} »")
    for k, (x, y) in enumerate(zip(a["scripts"], b["scripts"]), 1):
        if x != y:
            av(f"script modifié (script n° {k}) : à vérifier à la main")
            restes = [m.group(2) for m in _LITTERAL.finditer(y)
                      if m.group(2) in {n.group(2) for n in _LITTERAL.finditer(x)}]
            if restes:
                av(f"script contenant du français (script n° {k}) : « {_extrait(restes[0], 50)} » inchangé")
        elif S.scripts_a_traduire("<script>%s</script>" % x):
            av(f"script contenant du français (script n° {k}) : chaînes de texte à traduire à la main")
    return out


# ---------- contrôle par type de fichier ----------

def _controler_html(fr, tr, fichier, lang, termes):
    out = []
    fa, fb = _front(fr), _front(tr)
    if fa is not None:
        if fb is None:
            out.append(_pb(fichier, BLOQUANT, "structure", "front-matter <!--page … --> absent"))
        else:
            for k in fa:
                if k not in fb:
                    out.append(_pb(fichier, BLOQUANT, "structure", f"front-matter : clé « {k} » absente"))
                elif k not in S.FRONT and fa[k] != fb[k]:
                    out.append(_pb(fichier, BLOQUANT, "structure", f"front-matter : valeur technique « {k} » modifiée : "
                                                                   f"« {_extrait(fa[k])} » → « {_extrait(fb[k])} »"))
            for k in fb:
                if k not in fa and k != STATUT:
                    out.append(_pb(fichier, BLOQUANT, "structure", f"front-matter : clé « {k} » en trop"))
            for k in BORNES:
                if k in fb:
                    out += _seo(k, fb[k], fichier, "front-matter : ")
    out += _comparer_balises(fr, tr, fichier)
    for u in S.extraire_html(_sans_fr(tr)):
        r = _restes_fr(_plat(u["texte"]), lang)
        if r:
            out.append(_pb(fichier, BLOQUANT, "restes_fr", f"{GENRES[u['genre']]} : {r[0]} mots outils français sur "
                                                           f"{r[1]} : « {_extrait(_plat(u['texte']))} »"))
    out += _eszett(fr, tr, fichier, lang)
    out += _tirets_lignes(tr, fichier)
    ua, ub = S.extraire_html(fr), S.extraire_html(tr)
    out += _produits(" \n".join(_plat(u["texte"]) for u in ua), " \n".join(_plat(u["texte"]) for u in ub), fichier)
    if termes:
        groupes = defaultdict(lambda: ([], []))
        for cote, us in ((0, ua), (1, ub)):
            for u in us:
                groupes[u["genre"]][cote].append(_plat(u["texte"]))
        paires = []
        for g, (xa, xb) in groupes.items():
            if len(xa) == len(xb):
                paires += [(f"{GENRES[g]} n° {i}", a, b) for i, (a, b) in enumerate(zip(xa, xb), 1)]
            else:  # segments non alignés : comparaison sur l'ensemble du genre
                paires.append((f"{GENRES[g]} (ensemble)", " ".join(xa), " ".join(xb)))
        out += _termes(paires, termes, fichier)
    return out


def _genre_json(v):
    return "objet" if isinstance(v, dict) else "liste" if isinstance(v, list) else "texte" if isinstance(v, str) else "valeur"


def _structure(a, b, chemin, fichier, racine, out):
    bl = lambda d: out.append(_pb(fichier, BLOQUANT, "structure", d))
    lieu = _lieu(chemin, racine)
    if _genre_json(a) != _genre_json(b):
        bl(f"{lieu} : {_genre_json(a)} attendu, {_genre_json(b)} trouvé")
    elif isinstance(a, dict):
        for k in a:
            if k not in b:
                bl(f"clé absente : {_lieu(chemin + (k,), racine)}")
            elif k in S.TECH:
                if a[k] != b[k]:
                    bl(f"valeur technique modifiée : {_lieu(chemin + (k,), racine)} : "
                       f"« {_extrait(json.dumps(a[k], ensure_ascii=False))} » → « {_extrait(json.dumps(b[k], ensure_ascii=False))} »")
            else:
                _structure(a[k], b[k], chemin + (k,), fichier, racine, out)
        for k in b:
            if k not in a:
                bl(f"clé en trop : {_lieu(chemin + (k,), racine)}")
    elif isinstance(a, list):
        if len(a) != len(b):
            bl(f"liste de longueur différente : {lieu} ({len(a)} éléments dans la source, {len(b)} dans la traduction)")
        for i, (x, y) in enumerate(zip(a, b)):
            _structure(x, y, chemin + (i,), fichier, racine, out)
    elif isinstance(a, str):
        if S.CHEMIN.match(a) and a != b:  # chemin ou adresse : jamais traduit
            bl(f"lien modifié : {lieu} : « {_extrait(a)} » → « {_extrait(b)} »")
        elif S.IDENT.fullmatch(a) and a != b:  # identifiant (valeur d'énumération, slug) : jamais traduit
            bl(f"identifiant modifié : {lieu} : « {a} » → « {_extrait(b)} »")
    elif a != b:
        bl(f"valeur modifiée : {lieu} : {a!r} → {b!r}")


def _paralleles(a, b, chemin=()):
    """(chemin, texte FR, texte traduit) des chaînes traduisibles présentes des deux côtés."""
    if isinstance(a, dict) and isinstance(b, dict):
        for k in a:
            if k in b and k not in S.TECH:
                yield from _paralleles(a[k], b[k], chemin + (k,))
    elif isinstance(a, list) and isinstance(b, list):
        for i, (x, y) in enumerate(zip(a, b)):
            yield from _paralleles(x, y, chemin + (i,))
    elif isinstance(a, str) and isinstance(b, str):
        yield chemin, a, b


def _chaines(o, chemin=()):
    """(chemin, chaîne, est_une_clé) de tout un JSON."""
    if isinstance(o, dict):
        for k, v in o.items():
            yield chemin + (k,), k, True
            yield from _chaines(v, chemin + (k,))
    elif isinstance(o, list):
        for i, v in enumerate(o):
            yield from _chaines(v, chemin + (i,))
    elif isinstance(o, str):
        yield chemin, o, False


def _sans_fr_json(o):
    if isinstance(o, dict):
        return {k: _sans_fr_json(v) for k, v in o.items()}
    if isinstance(o, list):
        return [_sans_fr_json(v) for v in o]
    return _sans_fr(o) if isinstance(o, str) and "lang" in o else o


def _seo_json(o, chemin, fichier, racine, out):
    if isinstance(o, dict):
        for k, v in o.items():
            if k in S.TECH:
                continue
            if k in BORNES and isinstance(v, str):
                out += _seo(k, v, fichier, _lieu(chemin, racine) + " : " if chemin else "")
            else:
                _seo_json(v, chemin + (k,), fichier, racine, out)
    elif isinstance(o, list):
        for i, v in enumerate(o):
            _seo_json(v, chemin + (i,), fichier, racine, out)


def _controler_json(fr, tr_txt, fichier, lang, termes):
    try:
        tr = json.loads(tr_txt)
    except ValueError as e:
        return [_pb(fichier, BLOQUANT, "structure", f"JSON invalide : {e}")]
    out = []
    _structure(fr, tr, (), fichier, fr, out)
    for chemin, a, b in _paralleles(fr, tr):
        if "<" in a + b or "{" in a + b:
            out += _comparer_balises(a, b, fichier, _lieu(chemin, fr))
    for u in S.extraire_json(_sans_fr_json(tr), ""):
        r = _restes_fr(_plat(u["texte"]), lang)
        if r:
            out.append(_pb(fichier, BLOQUANT, "restes_fr", f"{_lieu(u['chemin'], fr)} : {r[0]} mots outils français "
                                                           f"sur {r[1]} : « {_extrait(_plat(u['texte']))} »"))
    out += _eszett("\n".join(c for _, c, _ in _chaines(fr)), "\n".join(c for _, c, _ in _chaines(tr)), fichier, lang)
    for chemin, c, est_cle in _chaines(tr):
        out += _tirets_chaine(c, fichier, _lieu(chemin, fr) + (" (clé)" if est_cle else ""))
    ua, ub = S.extraire_json(fr, ""), S.extraire_json(tr, "")
    ga, gb = defaultdict(list), defaultdict(list)
    for g, us in ((ga, ua), (gb, ub)):
        for u in us:
            g[u["chemin"][0] if u["chemin"] else ()].append(_plat(u["texte"]))
    for k in list(ga) + [k for k in gb if k not in ga]:  # une entrée du JSON = une page générée
        pre = _lieu((k,), fr) + " : " if k != () else ""
        out += _produits(" \n".join(ga.get(k, [])), " \n".join(gb.get(k, [])), fichier, pre)
    _seo_json(tr, (), fichier, fr, out)
    if termes:
        da = {u["chemin"]: _plat(u["texte"]) for u in ua}
        db = {u["chemin"]: _plat(u["texte"]) for u in ub}
        out += _termes([(_lieu(c, fr), da[c], db[c]) for c in da if c in db], termes, fichier)
    return out


def _controler_cles(cles, tr_txt, fichier, lang, termes):
    try:
        tr = json.loads(tr_txt)
    except ValueError as e:
        return [_pb(fichier, BLOQUANT, "structure", f"JSON invalide : {e}")]
    if not isinstance(tr, dict):
        return [_pb(fichier, BLOQUANT, "structure", "le dictionnaire doit être un objet {texte FR : traduction}")]
    cles = list(cles)
    out, paires = [], []
    for k in cles:
        if k not in tr:
            out.append(_pb(fichier, BLOQUANT, "structure", f"clé d'interface absente : « {_extrait(k)} »"))
    for k in tr:
        if k not in cles:
            out.append(_pb(fichier, AVERT, "structure", f"clé inconnue de src/i18n/cles.json : « {_extrait(k)} »"))
    for k in cles:
        v = tr.get(k)
        if v is None:
            continue
        lieu = f"« {_extrait(k, 40)} »"
        if not isinstance(v, str):
            out.append(_pb(fichier, BLOQUANT, "structure", f"{lieu} : texte attendu"))
            continue
        out += _comparer_balises(k, v, fichier, lieu)
        r = _restes_fr(_texte_fragment(_sans_fr(v)), lang)
        if r:
            out.append(_pb(fichier, BLOQUANT, "restes_fr", f"{lieu} : {r[0]} mots outils français sur {r[1]} : "
                                                           f"« {_extrait(_texte_fragment(v))} »"))
        out += _tirets_chaine(v, fichier, lieu)
        out += _produits(_texte_fragment(k), _texte_fragment(v), fichier, lieu + " : ")
        paires.append((lieu, _texte_fragment(k), _texte_fragment(v)))
    out += _eszett("\n".join(cles), "\n".join(v for v in tr.values() if isinstance(v, str)), fichier, lang)
    out += _termes(paires, termes, fichier)
    return out


# ---------- inventaire et point d'entrée ----------

def _rel(base, p):
    return os.path.relpath(p, base).replace(os.sep, "/")


def _attendus(base, lang):
    """[(source FR, cible traduite, genre)], chemins relatifs à base."""
    src, lg, out = os.path.join(base, "src"), f"src/langues/{lang}", []
    for p in sorted(glob.glob(os.path.join(src, "pages", "**", "index.html"), recursive=True)):
        r = _rel(os.path.join(src, "pages"), p)
        out.append((f"src/pages/{r}", f"{lg}/pages/{r}", "html"))
    for n in PARTIELS:
        if os.path.exists(os.path.join(src, "partials", n)):
            out.append((f"src/partials/{n}", f"{lg}/partials/{n}", "html"))
    for p in sorted(glob.glob(os.path.join(src, "data", "*.json"))):
        n = os.path.basename(p)
        if n not in NON_TRADUITS:
            out.append((f"src/data/{n}", f"{lg}/data/{n}", "json"))
    if os.path.exists(os.path.join(src, "i18n", "cles.json")):
        out.append(("src/i18n/cles.json", f"src/i18n/{lang}.json", "cles"))
    return out


def _presents(base, lang):
    """Sources traduites présentes (les dossiers brut/ et les fichiers à la racine de la langue sont ignorés)."""
    lg, out = os.path.join(base, "src", "langues", lang), set()
    for d in ("pages", "data", "partials"):
        for racine, dossiers, fichiers in os.walk(os.path.join(lg, d)):
            dossiers[:] = [x for x in dossiers if not x.startswith(".")]
            out |= {_rel(base, os.path.join(racine, f)) for f in fichiers if not f.startswith(".")}
    if os.path.exists(os.path.join(base, "src", "i18n", f"{lang}.json")):
        out.add(f"src/i18n/{lang}.json")
    return out


def _controler_fichier(base, fr, cible, genre, lang, termes):
    with open(os.path.join(base, fr), encoding="utf-8") as f:
        a = f.read()
    try:
        with open(os.path.join(base, cible), encoding="utf-8") as f:
            b = f.read()
    except UnicodeDecodeError as e:
        return [_pb(cible, BLOQUANT, "structure", f"fichier illisible en UTF-8 : {e}")]
    if genre == "html":
        return _controler_html(a, b, cible, lang, termes)
    if genre == "json":
        return _controler_json(json.loads(a), b, cible, lang, termes)
    return _controler_cles(json.loads(a), b, cible, lang, termes)


def controler(lang, base=SITE, seulement=None):
    """Problèmes de la langue lang : [{fichier, gravite, regle, detail}], triés par fichier.
    Liste vide si la langue n'a encore aucune source traduite. seulement : motif de chemin (sous-chaîne ou jokers)."""
    if lang == "fr":
        raise ValueError("le français est la langue de référence : rien à contrôler")
    presents = _presents(base, lang)
    if not presents:
        return []
    garde = lambda rel: not seulement or fnmatch.fnmatch(rel, f"*{seulement}*")
    termes, out = _charger_termes(base, lang)
    out = [p for p in out if garde(p["fichier"])]
    attendus = _attendus(base, lang)
    for fr, cible, genre in attendus:
        if not garde(cible):
            continue
        if cible not in presents:
            out.append(_pb(cible, BLOQUANT, "structure", f"fichier traduit manquant (source : {fr})"))
        else:
            out += _controler_fichier(base, fr, cible, genre, lang, termes)
    cibles = {c for _, c, _ in attendus}
    for cible in sorted(presents - cibles):
        if not garde(cible):
            continue
        nom = os.path.basename(cible)
        if cible == f"src/langues/{lang}/data/{nom}" and nom in NON_TRADUITS and os.path.exists(
                os.path.join(base, "src", "data", nom)):
            out += _controler_fichier(base, f"src/data/{nom}", cible, "json", lang, termes)
        else:
            out.append(_pb(cible, BLOQUANT, "structure", "fichier traduit en trop : aucune source FR correspondante"))
    return sorted(out, key=lambda p: (p["fichier"], p["gravite"] != BLOQUANT, REGLES.index(p["regle"])))


def _nb(n, mot):
    return f"{n} {mot}{'s' if n > 1 else ''}"


def rapport(pbs, lang, seulement=None):
    lignes = [f"Contrôle des traductions · {lang}" + (f" · fichiers « {seulement} »" if seulement else ""), ""]
    par_fichier = defaultdict(list)
    for p in pbs:
        par_fichier[p["fichier"]].append(p)
    for f in sorted(par_fichier):
        lignes.append(f)
        vus, caches = Counter(), Counter()
        for p in par_fichier[f]:
            vus[p["regle"]] += 1
            if vus[p["regle"]] > MAX_LIGNES:
                caches[p["regle"]] += 1
                continue
            lignes.append(f"  {p['gravite']:<13}  {p['regle']:<9}  {_visible(p['detail'])}")
        for r, n in caches.items():
            lignes.append(f"  {'':<13}  {r:<9}  … et {n} autres")
        lignes.append("")
    if not pbs:
        lignes += ["Aucun problème.", ""]
    b = Counter(p["regle"] for p in pbs if p["gravite"] == BLOQUANT)
    a = Counter(p["regle"] for p in pbs if p["gravite"] == AVERT)
    lignes.append(f"Résumé : {_nb(sum(b.values()), 'bloquant')}, {_nb(sum(a.values()), 'avertissement')}")
    lignes.append(f"  {'règle':<10} {'bloquants':>10} {'avertissements':>15}")
    lignes += [f"  {r:<10} {b[r]:>10} {a[r]:>15}" for r in REGLES]
    return "\n".join(lignes)


def main(argv=None, base=SITE):
    ap = argparse.ArgumentParser(description="Contrôle automatique des traductions du site Neur.on.")
    ap.add_argument("lang", help="langue à contrôler : de, it ou en")
    ap.add_argument("--seulement", metavar="MOTIF",
                    help="ne contrôler que les fichiers dont le chemin contient ce motif (jokers * et ? acceptés)")
    args = ap.parse_args(argv)
    try:
        pbs = controler(args.lang, base=base, seulement=args.seulement)
    except ValueError as e:
        print(e)
        return 2
    if not _presents(base, args.lang):
        print(f"Aucune source traduite pour « {args.lang} » : ni pages, ni données, ni partiels dans "
              f"src/langues/{args.lang}/, et pas de src/i18n/{args.lang}.json. Rien à contrôler.")
        return 0
    print(rapport(pbs, args.lang, args.seulement))
    return 1 if any(p["gravite"] == BLOQUANT for p in pbs) else 0


if __name__ == "__main__":
    sys.exit(main())

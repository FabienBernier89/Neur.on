"""Liste les littéraux passés à T() dans src/generators.py : src/i18n/cles.json."""
import ast, json, os

ICI = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.dirname(ICI)
arbre = ast.parse(open(os.path.join(SITE, "src", "generators.py"), encoding="utf-8").read())
cles = sorted({n.args[0].value for n in ast.walk(arbre)
               if isinstance(n, ast.Call) and getattr(n.func, "id", "") == "T"
               and n.args and isinstance(n.args[0], ast.Constant) and isinstance(n.args[0].value, str)})
# textes passés à T() par variable : constantes de generators.py et catégories des JSON
import sys
sys.path.insert(0, os.path.join(SITE, "src"))
import generators as G  # noqa: E402
autres = set(G.METIERS.values()) | {v[0] for v in G.SHARE.values()} | {x for o in G.BLOG_OUTILS for x in o[1:3]}
for nom, champs in (("blog", ("categorie", "sous_categorie")), ("actualites", ("categorie",))):
    for x in json.load(open(os.path.join(SITE, "src", "data", nom + ".json"), encoding="utf-8")):
        autres |= {x[c] for c in champs if x.get(c)}
org = json.load(open(os.path.join(SITE, "src", "data", "organisation.json"), encoding="utf-8"))
autres |= {org["description"]} | set(org.get("award", [])) | {b["description"] for b in org.get("brand", [])}
# textes d'interface écrits dans build.py (fil d'Ariane, liens « bientôt », image de partage, sélecteur)
arbre_b = ast.parse(open(os.path.join(SITE, "build.py"), encoding="utf-8").read())
autres |= {n.args[0].value for n in ast.walk(arbre_b) if isinstance(n, ast.Call) and getattr(n.func, "id", "") == "T"
           and n.args and isinstance(n.args[0], ast.Constant) and isinstance(n.args[0].value, str)}
cles = sorted(set(cles) | autres)
os.makedirs(os.path.join(SITE, "src", "i18n"), exist_ok=True)
json.dump(cles, open(os.path.join(SITE, "src", "i18n", "cles.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(len(cles), "clés")

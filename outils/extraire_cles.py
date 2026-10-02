"""Liste les littéraux passés à T() dans src/generators.py : src/i18n/cles.json."""
import ast, json, os

ICI = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.dirname(ICI)
arbre = ast.parse(open(os.path.join(SITE, "src", "generators.py"), encoding="utf-8").read())
cles = sorted({n.args[0].value for n in ast.walk(arbre)
               if isinstance(n, ast.Call) and getattr(n.func, "id", "") == "T"
               and n.args and isinstance(n.args[0], ast.Constant) and isinstance(n.args[0].value, str)})
os.makedirs(os.path.join(SITE, "src", "i18n"), exist_ok=True)
json.dump(cles, open(os.path.join(SITE, "src", "i18n", "cles.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(len(cles), "clés")

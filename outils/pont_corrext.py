"""Pont entre l'onglet Corrext connecté et le dépôt, pour la première traduction (LexMachina) du site.

  python3 outils/pont_corrext.py prepare de     découpe toutes les sources FR en textes uniques à traduire
  python3 outils/pont_corrext.py serve de       sert les lots à l'onglet Corrext (port 8812) et enregistre les traductions
  python3 outils/pont_corrext.py etat de        avancement
  python3 outils/pont_corrext.py reinjecter de  écrit les brouillons traduits dans src/langues/<lang>/

Le jeton de session Corrext reste dans l'onglet du navigateur : ce serveur ne le voit jamais (voir CORREXT-MT.md)."""
import glob, hashlib, json, os, re, sys, time
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

ICI = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.dirname(ICI)
SRC = os.path.join(SITE, "src")
sys.path.insert(0, ICI)
import segments as S  # noqa: E402

CIBLES = {"de": 46, "it": 140, "en": 56}
ORIGINE = "https://corrext.com"


def dossier(lang):
    d = os.path.join(SRC, "langues", lang, "brut")
    os.makedirs(d, exist_ok=True)
    return d


def cle(texte):
    return hashlib.sha1(texte.encode("utf-8")).hexdigest()[:16]


def sources():
    """(chemin relatif, genre) de toutes les sources FR à traduire."""
    out = [(os.path.relpath(p, SITE), "html") for p in sorted(glob.glob(os.path.join(SRC, "pages", "**", "index.html"), recursive=True))]
    out += [(os.path.relpath(p, SITE), "html") for p in (os.path.join(SRC, "partials", "nav.html"),
                                                          os.path.join(SRC, "partials", "footer.html"))]
    out += [(os.path.relpath(p, SITE), "json") for p in sorted(glob.glob(os.path.join(SRC, "data", "*.json")))
            if os.path.basename(p) not in ("redirections.json", "fedlex.json", "organisation.json")]
    if os.path.exists(os.path.join(SRC, "i18n", "cles.json")):
        out.append(("src/i18n/cles.json", "cles"))
    return out


def unites(rel, genre):
    p = os.path.join(SITE, rel)
    if genre == "html":
        return S.extraire_html(open(p, encoding="utf-8").read())
    data = json.load(open(p, encoding="utf-8"))
    if genre == "cles":
        return [dict(zip(("id", "texte", "table"), (str(i), *S.proteger(k)))) | {"html": k} for i, k in enumerate(data)]
    return S.extraire_json(data, os.path.basename(p))


def prepare(lang):
    textes = {}
    for rel, genre in sources():
        for u in unites(rel, genre):
            textes.setdefault(cle(u["texte"]), u["texte"])
    json.dump(textes, open(os.path.join(dossier(lang), "a_traduire.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=0)
    car = sum(len(t) for t in textes.values())
    print(f"{len(textes)} textes uniques, {car:,} caractères".replace(",", "'"))


def charge(lang, nom):
    p = os.path.join(dossier(lang), nom)
    return json.load(open(p, encoding="utf-8")) if os.path.exists(p) else {}


def serve(lang):
    a_traduire = charge(lang, "a_traduire.json")
    faits = charge(lang, "traductions.json")
    en_cours = {}
    chemin = os.path.join(dossier(lang), "traductions.json")

    class H(BaseHTTPRequestHandler):
        def _entetes(self, code=200):
            self.send_response(code)
            self.send_header("Access-Control-Allow-Origin", ORIGINE)
            self.send_header("Access-Control-Allow-Private-Network", "true")
            self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
            self.send_header("Access-Control-Allow-Headers", "Content-Type")
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.end_headers()

        def do_OPTIONS(self):
            self._entetes(204)

        def do_GET(self):
            if self.path.startswith("/relais"):
                # page chargée en cadre par l'onglet Corrext : elle parle au pont (même origine) et au parent par messages
                page = ("<!doctype html><meta charset=utf-8><script>"
                        "addEventListener('message',async e=>{if(e.origin!=='" + ORIGINE + "')return;const m=e.data||{};"
                        "let r;try{if(m.op==='lot')r=await (await fetch('/lot?n='+(m.n||25))).json();"
                        "else if(m.op==='etat')r=await (await fetch('/etat')).json();"
                        "else if(m.op==='resultat')r=await (await fetch('/resultat',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(m.donnees)})).json();"
                        "}catch(x){r={err:String(x)}}parent.postMessage({id:m.id,r},'" + ORIGINE + "')});"
                        "parent.postMessage({pret:true},'" + ORIGINE + "');</script>")
                self.send_response(200)
                self.send_header("Content-Type", "text/html; charset=utf-8")
                self.end_headers()
                self.wfile.write(page.encode())
                return
            if self.path.startswith("/lot"):
                n = int(re.search(r"n=(\d+)", self.path).group(1)) if "n=" in self.path else 25
                maintenant, lot, taille = time.time(), [], 0
                for k, t in a_traduire.items():
                    if k in faits or maintenant - en_cours.get(k, 0) < 180:
                        continue
                    if lot and (len(lot) >= n or taille + len(t) > 8000):
                        break
                    lot.append({"k": k, "texte": t}); taille += len(t); en_cours[k] = maintenant
                self._entetes(); self.wfile.write(json.dumps({"lot": lot, "cible": CIBLES[lang]}, ensure_ascii=False).encode())
            elif self.path.startswith("/etat"):
                self._entetes(); self.wfile.write(json.dumps({"total": len(a_traduire), "faits": len(faits)}).encode())
            else:
                self._entetes(404)

        def do_POST(self):
            corps = json.loads(self.rfile.read(int(self.headers.get("Content-Length", 0))) or b"[]")
            for r in corps:
                if r.get("k") in a_traduire and isinstance(r.get("traduction"), str) and r["traduction"].strip():
                    faits[r["k"]] = r["traduction"]
            json.dump(faits, open(chemin, "w", encoding="utf-8"), ensure_ascii=False, indent=0)
            self._entetes(); self.wfile.write(json.dumps({"ok": len(faits)}).encode())

        def log_message(self, *a):
            pass

    print(f"Pont {lang} sur http://localhost:8812 : {len(faits)}/{len(a_traduire)} déjà traduits")
    ThreadingHTTPServer(("127.0.0.1", 8812), H).serve_forever()


def etat(lang):
    a, f = charge(lang, "a_traduire.json"), charge(lang, "traductions.json")
    print(f"{len(f)}/{len(a)} textes traduits ({100 * len(f) // max(1, len(a))} %)")


def _traduit(u, faits, a_revoir, rel):
    t = faits.get(cle(u["texte"]))
    if t is None:
        return None
    try:
        return S.restaurer(t, u["table"])
    except ValueError as e:
        # marqueurs abîmés : texte sans balisage, jetons {{…}} remis en fin, à reprendre par l'agent d'adaptation
        plat = re.sub(r"\{\s*/?\s*\d+\s*\}", "", t)
        jetons = [e2["vide"] for e2 in u["table"].values() if "vide" in e2 and e2["vide"].startswith("{{")]
        a_revoir.append({"fichier": rel, "segment": u["id"], "probleme": str(e), "source": u["html"]})
        return S.html.escape(" ".join(plat.split()), quote=False) + "".join(" " + j for j in jetons)


def reinjecter(lang):
    faits = charge(lang, "traductions.json")
    a_revoir, manquants = [], 0
    base = os.path.join(SRC, "langues", lang)
    for rel, genre in sources():
        us = unites(rel, genre)
        trad = {}
        for u in us:
            t = _traduit(u, faits, a_revoir, rel)
            if t is None:
                manquants += 1
            else:
                trad[u["id"]] = t
        if genre == "html":
            src = open(os.path.join(SITE, rel), encoding="utf-8").read()
            cible = os.path.join(base, os.path.relpath(rel, "src"))
            os.makedirs(os.path.dirname(cible), exist_ok=True)
            open(cible, "w", encoding="utf-8").write(S.reinjecter_html(src, trad))
        elif genre == "json":
            data = json.load(open(os.path.join(SITE, rel), encoding="utf-8"))
            cible = os.path.join(base, "data", os.path.basename(rel))
            os.makedirs(os.path.dirname(cible), exist_ok=True)
            json.dump(S.reinjecter_json(data, trad), open(cible, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
        else:  # clés d'interface -> src/i18n/<lang>.json
            data = json.load(open(os.path.join(SITE, rel), encoding="utf-8"))
            sortie = {k: trad[str(i)] for i, k in enumerate(data) if str(i) in trad}
            json.dump(sortie, open(os.path.join(SRC, "i18n", f"{lang}.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    json.dump(a_revoir, open(os.path.join(dossier(lang), "a_revoir.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(f"Brouillons écrits dans src/langues/{lang}/ ; {len(a_revoir)} segments au balisage à reprendre ; {manquants} segments sans traduction")


if __name__ == "__main__":
    action, lang = sys.argv[1], sys.argv[2]
    {"prepare": prepare, "serve": serve, "etat": etat, "reinjecter": reinjecter}[action](lang)

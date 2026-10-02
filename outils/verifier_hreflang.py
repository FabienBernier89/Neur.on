"""Contrôle des alternates hreflang du site généré : chaque page cite ses versions, et chaque version la cite en retour.

  python3 outils/verifier_hreflang.py [dossier docs]

Vérifie aussi que chaque adresse citée existe, que la page se cite elle-même et que x-default pointe vers la racine."""
import glob, os, re, sys

SITE = "https://neur-on.ai"
LIEN = re.compile(r'<link rel="alternate" hreflang="([^"]+)" href="([^"]+)">')


def lire(docs):
    pages = {}
    for p in glob.glob(os.path.join(docs, "**", "index.html"), recursive=True):
        rel = os.path.relpath(os.path.dirname(p), docs).replace(os.sep, "/")
        if rel.startswith("maquettes"):
            continue  # maquettes pour les développeurs, hors du site
        url = f"{SITE}/" if rel == "." else f"{SITE}/{rel}/"
        h = open(p, encoding="utf-8").read()
        if 'http-equiv="refresh"' in h:
            continue  # page de renvoi d'une ancienne adresse
        pages[url] = dict((u, l) for l, u in LIEN.findall(h))
    return pages


def verifier(docs):
    pages = lire(docs)
    erreurs = []
    for url, alt in pages.items():
        if not alt:
            continue
        if url not in alt:
            erreurs.append(f"{url} : ne se cite pas elle-même")
        if alt.get(f"{SITE}/") != "x-default":
            erreurs.append(f"{url} : x-default absent ou faux")
        for u, l in alt.items():
            if l == "x-default":
                continue
            if u not in pages:
                erreurs.append(f"{url} : cite {u} ({l}), absente du site")
            elif url not in pages[u]:
                erreurs.append(f"{url} : {u} ({l}) ne la cite pas en retour")
            elif pages[u] != alt:
                erreurs.append(f"{url} : jeu d'alternates différent de {u}")
    return pages, erreurs


if __name__ == "__main__":
    docs = sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "docs")
    pages, erreurs = verifier(docs)
    avec = sum(1 for a in pages.values() if a)
    print(f"{len(pages)} pages, {avec} avec alternates, {len(erreurs)} erreurs")
    for e in erreurs[:50]:
        print("  · " + e)
    sys.exit(1 if erreurs else 0)

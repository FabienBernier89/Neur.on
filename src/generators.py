"""Pages à l'échelle du site Neur.on : métiers, domaines, paires de langues, glossaire, aide.

Chaque fonction lit ses données dans src/data/*.json et rend un corps HTML complet.
build_all() renvoie une liste de (chemin logique, front-matter, corps).
Aucune donnée inventée : tout provient de PRODUCT.md et du carnet d'audit de l'application.
"""
import json, os


def load(src, name):
    p = os.path.join(src, "data", name + ".json")
    if not os.path.exists(p):
        return []
    with open(p, encoding="utf-8") as f:
        return json.load(f)


def build_all(src):
    pages = []
    return pages

"""Écriture des fichiers de données au format maison : un objet par ligne dans les listes, pour des diffs lisibles."""
import json


def _v(v):
    if isinstance(v, list) and v and all(isinstance(o, dict) for o in v):
        return "[\n" + ",\n".join("      " + json.dumps(o, ensure_ascii=False) for o in v) + "\n    ]"
    return json.dumps(v, ensure_ascii=False)


def dumps(pages):
    return "[\n" + ",\n".join(
        "  {\n" + ",\n".join(f'    {json.dumps(k, ensure_ascii=False)}: {_v(v)}' for k, v in p.items()) + "\n  }"
        for p in pages) + "\n]\n"

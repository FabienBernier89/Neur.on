"""Textes d'interface des gabarits. La clé est le texte FR exact ; une clé absente est notée (le build échoue en fin de langue)."""
import json, os

_LANG, _DICT = "fr", {}
MANQUANTS = set()
MOIS = {"fr": "janvier février mars avril mai juin juillet août septembre octobre novembre décembre",
        "de": "Januar Februar März April Mai Juni Juli August September Oktober November Dezember",
        "it": "gennaio febbraio marzo aprile maggio giugno luglio agosto settembre ottobre novembre dicembre",
        "en": "January February March April May June July August September October November December"}


def activer(lang, dossier):
    global _LANG, _DICT
    _LANG = lang
    p = os.path.join(dossier, lang + ".json")
    _DICT = json.load(open(p, encoding="utf-8")) if lang != "fr" and os.path.exists(p) else {}
    MANQUANTS.clear()


def langue():
    return _LANG


def T(fr):
    if _LANG == "fr":
        return fr
    v = _DICT.get(fr)
    if v is None:
        MANQUANTS.add(fr)
        return fr
    return v


def date_longue(iso):
    a, m, j = (int(x) for x in iso[:10].split("-"))
    mois = MOIS[_LANG].split()[m - 1]
    if _LANG == "de":
        return f"{j}. {mois} {a}"
    if _LANG == "fr":
        return f"{'1er' if j == 1 else j} {mois} {a}"
    return f"{j} {mois} {a}"

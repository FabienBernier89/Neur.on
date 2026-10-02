"""Langues du site : adresses traduites, liens localisés, alternates hreflang.
Le chemin FR d'une page (« fr/traduction/contrats/ ») l'identifie dans toutes les langues."""
import re

LANGUES = ("fr", "de", "it", "en")
HREFLANG = {"fr": "fr-CH", "de": "de-CH", "it": "it-CH", "en": "en"}
OG_LOCALE = {"fr": "fr_CH", "de": "de_CH", "it": "it_CH", "en": "en_GB"}


class Routes:
    def __init__(self, table):
        self.t = table or {}

    def chemin(self, fr_path, lang):
        if lang == "fr":
            return fr_path
        return self.t.get(fr_path, {}).get(lang)


_LIEN = re.compile(r'(\{\{ROOT\}\}|https://neur-on\.ai/)(fr/[^"#?\s<>\']*)')


def localiser(html, lang, routes, existantes, site):
    """Remplace les liens FR par l'adresse de la langue quand la page y existe.
    existantes : chemins FR des pages publiées dans cette langue."""
    if lang == "fr":
        return html, set()
    manquants = set()

    def sub(m):
        pre, chemin = m.group(1), m.group(2)
        cle = chemin if chemin.endswith("/") else chemin + "/"
        cible = routes.chemin(cle, lang) if cle in existantes else None
        if not cible:
            manquants.add(cle)
            return m.group(0)
        return pre + cible
    return _LIEN.sub(sub, html), manquants


def alternates(fr_path, dispo, routes, site):
    """[(hreflang, url), …] des versions existantes, plus x-default ; vide si une seule langue."""
    out = [(HREFLANG[l], f"{site}/{routes.chemin(fr_path, l)}") for l in LANGUES
           if fr_path in dispo.get(l, set()) and routes.chemin(fr_path, l)]
    return out + [("x-default", f"{site}/")] if len(out) > 1 else []

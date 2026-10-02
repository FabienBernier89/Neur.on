"""Pages à l'échelle du site Neur.on : métiers, domaines, paires de langues, glossaire, aide.

Chaque famille lit ses données dans src/data/<famille>.json et rend un corps HTML qui réutilise
le socle CSS. build_all() renvoie une liste de (chemin logique, front-matter, corps).
Aucune donnée inventée : le contenu vient de PRODUCT.md, du carnet d'audit de l'application et
des textes de loi suisses publiés dans les langues officielles.
"""
import json, os, re

import i18n
from i18n import T, date_longue
from langues import HREFLANG

ARROW =('<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" '
         'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">'
         '<path d="M5 12h14M13 5l7 7-7 7"/></svg>')
CHECK = ('<span class="chk"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" '
         'stroke-linecap="round" stroke-linejoin="round"><polyline points="20 6 9 17 4 12"/>'
         '</svg></span>')
SHIELD = ('<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" '
          'stroke-linecap="round" stroke-linejoin="round"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7'
          'c0 6 8 10 8 10z"/></svg>')
GLOBE = ('<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" '
         'stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/>'
         '<path d="M2 12h20M12 2a15 15 0 0 1 0 20 15 15 0 0 1 0-20z"/></svg>')
SPARK = ('<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" '
         'stroke-linecap="round" stroke-linejoin="round"><path d="M12 2l1.8 5.2L19 9l-5.2 1.8'
         'L12 16l-1.8-5.2L5 9l5.2-1.8z"/></svg>')
ICONS = [SHIELD, GLOBE, SPARK]


NOM_LANGUE = {"fr": "Français", "it": "Italien", "en": "Anglais"}


def equivalent(d):
    """Équivalent affiché à côté du mot-vedette allemand d'une fiche : celui de la langue de la page,
    le français pour une page française ou allemande."""
    l = i18n.langue()
    return d[l] if l in ("it", "en") else d["fr"]


def langue_exemple(ex):
    """Seconde langue de la citation officielle d'une fiche du glossaire : celle de la page,
    le français pour une page allemande ou quand la loi n'a pas de version dans la langue."""
    l = i18n.langue()
    return l if l in ("it", "en") and ex.get(l) else "fr"


def load(src, name):
    p = os.path.join(src, "data", name + ".json")
    if not os.path.exists(p):
        return []
    with open(p, encoding="utf-8") as f:
        return json.load(f)


# ---------------------------------------------------------------- briques

_CARTES = None
# dossier des données de la langue en cours (src/data pour le FR, src/langues/<lang>/data sinon), fixé par utiliser()
_DONNEES = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")


def utiliser(src):
    """Prend les données de la langue en cours pour les briques appelées hors de build_all (cartes de héros)."""
    global _DONNEES, _CARTES
    _DONNEES, _CARTES = os.path.join(src, "data"), None
SYMB = {"y": '<span class="cmp-y">✓</span> ', "p": '<span class="cmp-p">⚠</span> ', "n": '<span class="cmp-n">✕</span> '}


def carte(nom):
    """Carte de droite des heros (src/data/cartes.json) : fiche, terme en quatre langues, extrait de tableau ou code."""
    global _CARTES
    if _CARTES is None:
        _CARTES = json.load(open(os.path.join(_DONNEES, "cartes.json"), encoding="utf-8"))
    c = _CARTES[nom]
    tete = f'<div class="sh"><b>{c["titre"]}</b><span>{c["droite"]}</span></div>'
    pied = f'<div class="sf">{c["pied"]}</div>' if c.get("pied") else ""
    if c["type"] == "terme":
        corps = "".join(f'<div class="sr{" first" if i == 0 else ""}"><i>{lab}</i><b lang="{k}">{c["mots"][k]}</b></div>'
                        for i, (k, lab) in enumerate((("de", T("Allemand")), ("fr", T("Français")), ("it", T("Italien")), ("en", T("Anglais")))))
        return f'<div class="law-spec hcarte">{tete}{corps}{pied}</div>'
    if c["type"] == "tableau":
        val = lambda v: SYMB[v[0]] + v[2:]
        corps = (f'<div class="tr hd"><span></span><span>{c["colonnes"][0]}</span><span class="c">{c["colonnes"][1]}</span></div>'
                 + "".join(f'<div class="tr"><span class="l">{l}</span><span>{val(x)}</span><span class="c">{val(y)}</span></div>'
                           for l, x, y in c["lignes"]))
        return f'<div class="law-spec hcarte htab">{tete}{corps}{pied}</div>'
    if c["type"] == "code":
        code = "".join(f'<span class="{k}">{v}</span>' if k != "t" else v for k, v in c["code"])
        return f'<div class="law-spec hcarte">{tete}<div class="hcode">{code}</div>{pied}</div>'
    corps = "".join(f'<div class="sr"><i>{k}</i><b>{v}</b></div>' for k, v in c["lignes"])
    return f'<div class="law-spec hcarte">{tete}{corps}{pied}</div>'


def hero(h1_lede, h1_rest, lead, nom_carte, ancre="#faits", ancre_txt=None):
    # Libellé par défaut traduit à l'appel, pas à l'import du module
    if ancre_txt is None:
        ancre_txt = T("Voir le détail")
    return f'''<section class="thero thero-carte">
  <div class="container">
    <div class="thero-grid">
      <div>
        <h1><em>{h1_lede}</em> {h1_rest}</h1>
        <p class="lead">{lead}</p>
        <div class="thero-cta">
          <a href="{{{{ROOT}}}}fr/contact/" class="btn btn-blue">{T("Demander une démo")} {ARROW}</a>
          <a href="{ancre}" class="btn btn-ghost">{ancre_txt}</a>
        </div>
      </div>
      {carte(nom_carte)}
    </div>
  </div>
</section>'''


def hero_job(lede, rest, lead, promesses, titre_fiche, ancre="#faits", ancre_txt=None):
    """Hero métier : le bleu nuit du produit, mais les repères forment une fiche de profil."""
    if ancre_txt is None:
        ancre_txt = T("Ce que Corrext change")
    ps = "".join(
        f'<span>{ICONS[i % 3]}<span><b>{p["t"]} :</b> {p["d"]}</span></span>'
        for i, p in enumerate(promesses))
    return f'''<section class="thero thero-job">
  <div class="container">
    <div class="thero-grid">
      <div>
        <h1><em>{lede}</em> {rest}</h1>
        <p class="lead">{lead}</p>
        <div class="thero-cta">
          <a href="{{{{ROOT}}}}fr/contact/" class="btn btn-blue">{T("Demander une démo")} {ARROW}</a>
          <a href="{ancre}" class="btn btn-ghost">{ancre_txt}</a>
        </div>
      </div>
      <div class="thero-promise"><span class="jh">{titre_fiche}</span>{ps}</div>
    </div>
  </div>
</section>'''


def hero_law(lede, rest, lead, spec, ancre="#faits", ancre_txt=None):
    """Hero des pages de matière juridique : la terminologie tient lieu de visuel."""
    if ancre_txt is None:
        ancre_txt = T("Ce que Corrext apporte")
    rows = "".join(
        f'<div class="sr{" first" if i == 0 else ""}"><i>{lab}</i><b>{spec["mots"][k]}</b></div>'
        for i, (k, lab) in enumerate((("de", T("Allemand")), ("fr", T("Français")),
                                      ("it", T("Italien")), ("en", T("Anglais")))))
    return f'''<section class="thero thero-law">
  <div class="container">
    <div class="thero-grid">
      <div>
        <h1><em>{lede}</em> {rest}</h1>
        <p class="lead">{lead}</p>
        <div class="thero-cta">
          <a href="{{{{ROOT}}}}fr/contact/" class="btn btn-blue">{T("Demander une démo")} {ARROW}</a>
          <a href="{ancre}" class="btn btn-ghost">{ancre_txt}</a>
        </div>
      </div>
      <div class="law-spec">
        <div class="sh"><b>{spec["titre"]}</b><span>{spec["compte"]}</span></div>
        {rows}
        <div class="sf">{spec["pied"]}</div>
      </div>
    </div>
  </div>
</section>'''


def facts(titre, intro, liens, lignes, ident="faits"):
    ls = "".join(f'<a href="{{{{ROOT}}}}{l["href"]}" class="feat-link">{l["txt"]} {ARROW}</a>'
                 for l in liens)
    fs = "".join(
        f'<div class="fact"><b>{f["k"]}</b><p>{f["v"]}'
        + (f'<small>{f["s"]}</small>' if f.get("s") else "") + "</p></div>" for f in lignes)
    return f'''<section class="facts" id="{ident}" style="padding:84px 0">
  <div class="container">
    <div class="facts-grid">
      <div class="facts-lead">
        <h2>{titre}</h2>
        <p>{intro}</p>
        <div class="links">{ls}</div>
      </div>
      <div class="facts-list">{fs}</div>
    </div>
  </div>
</section>'''


# ---------------------------------------------------------------- vignettes métier
# Miniatures de l'interface Corrext pour le bloc « outils » des pages métier.
# Les textes affichés sont de vraies sorties récoltées dans l'application (septembre 2026).

def _svg(d, w="2"):
    return (f'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="{w}" '
            f'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{d}</svg>')


V_CHECK = _svg('<path d="M20 6 9 17l-5-5"/>', "2.6")
V_LOCK = _svg('<rect x="5" y="11" width="14" height="10" rx="2"/><path d="M8 11V7a4 4 0 0 1 8 0v4"/>', "2.2")
V_SEARCH = _svg('<circle cx="11" cy="11" r="7"/><path d="m20 20-3.5-3.5"/>', "2.2")
V_BOOK = _svg('<path d="M4 19.5A2.5 2.5 0 0 1 6.5 17H20V3H6.5A2.5 2.5 0 0 0 4 5.5z"/>', "2")


def _win(titre, corps):
    return (f'<div class="jv-win" aria-hidden="true"><div class="jv-bar"><span class="d"></span>'
            f'<span class="d"></span><span class="d"></span><b>{titre}</b></div>'
            f'<div class="jv-body">{corps}</div></div>')


VIGNETTES = {
    "outil-texte": lambda: _win("Fast translation",
        '<div class="jv-langs">French → English <span>LexMachina</span></div>'
        '<div class="jv-2col"><div lang="fr">Le débiteur en demeure doit des intérêts moratoires au taux de 5% l\'an …</div>'
        '<div lang="en">The debtor in default shall owe default interest at the rate of 5% per annum …</div></div>'),
    "outil-projet": lambda: _win("Translation project",
        f'<div class="jv-steps"><span class="ok">{V_CHECK}Set-up</span><i></i>'
        f'<span class="ok">{V_CHECK}File overview</span><i></i><span class="cur">Quotes</span></div>'
        f'<div class="jv-opts"><div class="jv-opt on"><b>Internal review</b><span>{T("par vos équipes")}</span></div>'
        f'<div class="jv-opt"><b>Custom workflow</b><span>{T("traducteur juridique")}</span></div></div>'),
    "outil-chnell": lambda: _win("CHnell",
        f'<div class="jv-search">{V_SEARCH}<b>Verzugszins</b><span>German → French</span></div>'
        '<div class="jv-res"><div lang="de">… den fehlenden Betrag zuzüglich <mark>Verzugszins</mark> nicht mehr nachbelasten …</div>'
        '<div lang="fr">… prélever le montant manquant avec l\'<mark>intérêt moratoire</mark> …</div></div>'
        f'<div class="jv-src">{V_BOOK}{T("Feuille fédérale")}</div>'),
    # Même illustration que la page API : pas une documentation, le contrat d'interface fait foi.
    "outil-api": lambda: _win(T("API REST"),
        '<div class="jv-code"><span class="m">POST</span> /v1/translate\n{\n'
        '  <span class="k">"source_language"</span>: "de",\n  <span class="k">"target_language"</span>: "fr",\n'
        '  <span class="k">"engine"</span>: "lexmachina",\n  <span class="k">"domain"</span>: "banking"\n}</div>'
        f'<div class="jv-foot">{T("Illustration · le contrat d'interface est remis au cadrage")}</div>'),
    # Parcours auszug-hr.ch, données de démonstration de la page Extraits.
    "outil-extraits": lambda: _win("Commercial register extract",
        f'<div class="jv-search">{V_SEARCH}<b>Muster AG</b><span>CHE-000.000.000</span></div>'
        '<ul class="jv-list"><li><i></i>Corrext Certification</li><li><i></i>Notarized Certification</li>'
        '<li class="on"><i></i>Notarized &amp; Apostilled</li></ul>'),
    # Mode Highly sensitive : seul le moteur suisse reste sélectionnable, les autres sont grisés.
    "outil-lexmachina": lambda: _win("Translation engine",
        f'<div class="jv-chips"><span class="jv-chip dark">{V_LOCK}Highly sensitive</span></div>'
        f'<ul class="jv-list"><li class="on"><i></i>LexMachina<span>{T("Suisse")}</span></li>'
        '<li class="off"><i></i>DeepL Pro</li><li class="off"><i></i>Azure OpenAI GPT</li></ul>'),
}
OUTIL_VIS = {"fr/corrext/traduction-texte-et-document/": "outil-texte",
             "fr/corrext/gestion-de-projet/": "outil-projet", "fr/corrext/chnell/": "outil-chnell",
             "fr/corrext/api-on-premises/": "outil-api",
             "fr/corrext/extraits-registre-commerce/": "outil-extraits", "fr/lexmachina/": "outil-lexmachina"}


def outils_visuel(titre, items):
    ss = "".join(f'<a class="jv-tool" href="{{{{ROOT}}}}{s["href"]}">{VIGNETTES[OUTIL_VIS[s["href"]]]()}'
                 f'<b>{s["t"]}</b><span>{s["d"]}</span><em>{T("Découvrir l'outil")} {ARROW}</em></a>'
                 for s in items)
    return ('<section class="siblings jv-tools">\n  <div class="container">\n'
            f'    <h2>{titre}</h2>\n    <div class="jv-tgrid">{ss}</div>\n  </div>\n</section>')


# Pictogrammes du bloc « moments », un par situation métier
WS_ICONS = {k: _svg(v, "1.9") for k, v in {
    # Cabinets d'avocats
    "lot": '<path d="M9 3h7l4 4v11a2 2 0 0 1-2 2H9a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2z"/><path d="M16 3v4h4"/><path d="M4 7v12a2 2 0 0 0 2 2h9"/>',
    "pret": '<circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/>',
    "sentence": '<path d="M12 3v18M7 21h10M5 7h14"/><path d="m5 7-3 6a3 3 0 0 0 6 0z"/><path d="m19 7-3 6a3 3 0 0 0 6 0z"/>',
    # Domaine Contrats
    "immeuble": '<path d="M3 10.5 12 3l9 7.5"/><path d="M5 9v12h14V9"/><path d="M10 21v-6h4v6"/>',
    "financement": '<rect x="2.5" y="6" width="19" height="12" rx="2"/><circle cx="12" cy="12" r="2.5"/><path d="M6 9.5h.01M18 14.5h.01"/>',
    # Domaines du droit
    "reseau": '<circle cx="12" cy="5" r="2.5"/><circle cx="5" cy="19" r="2.5"/><circle cx="19" cy="19" r="2.5"/><path d="M12 7.5v4M12 11.5 6.5 17M12 11.5l5.5 5.5"/>',
    "envoi": '<path d="M22 2 11 13"/><path d="M22 2 15 22l-4-9-9-4z"/>',
    "calendrier": '<rect x="3" y="5" width="18" height="16" rx="2"/><path d="M3 10h18M8 3v4M16 3v4"/>',
    "alerte": '<path d="M12 3 2 20h20z"/><path d="M12 10v4M12 17h.01"/>',
    "ampoule": '<path d="M9 18h6M10 21h4"/><path d="M12 3a6 6 0 0 0-3.5 10.9c.6.5 1 1.2 1 2.1h5c0-.9.4-1.6 1-2.1A6 6 0 0 0 12 3z"/>',
    "etiquette": '<path d="M3 12V4a1 1 0 0 1 1-1h8l9 9-9 9z"/><circle cx="7.5" cy="7.5" r="1.5"/>',
    "certificat": '<circle cx="12" cy="9" r="6"/><path d="m9 14.5-1.5 6.5L12 19l4.5 2-1.5-6.5"/>',
    # Comparatif agence ou plateforme
    "eclair": '<path d="M13 2 3 14h9l-1 8 10-12h-9z"/>',
    # Pages produit et sécurité
    "loupe": '<circle cx="11" cy="11" r="7"/><path d="m20 20-3.5-3.5"/>',
    "equipe": '<circle cx="9" cy="8" r="3.5"/><path d="M2.5 20a6.5 6.5 0 0 1 13 0"/><path d="M16 4.5a3.5 3.5 0 0 1 0 7"/><path d="M18 14.5a6.5 6.5 0 0 1 3.5 5.5"/>',
    "verrou": '<rect x="5" y="11" width="14" height="10" rx="2"/><path d="M8 11V7a4 4 0 0 1 8 0v4"/>',
    "dossier": '<path d="M3 7a2 2 0 0 1 2-2h4l2 2h8a2 2 0 0 1 2 2v8a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"/>',
    "portail": '<rect x="3" y="4" width="18" height="16" rx="2"/><path d="M3 9h18"/><path d="M9 9v11"/>',
    # Banques et finance
    "bouclier": '<path d="M12 3 5 6v5c0 4.5 3 8.3 7 10 4-1.7 7-5.5 7-10V6z"/><path d="m9 12 2 2 4-4"/>',
    "signature": '<path d="M15 5l4 4L8 20H4v-4z"/><path d="M13 7l4 4"/><path d="M14 20h6"/>',
    "rapport": '<path d="M4 20h16"/><path d="M7 16v-4M12 16V7M17 16v-6"/>',
    # Directions juridiques
    "jauge": '<path d="M4 17a8 8 0 1 1 16 0"/><path d="m12 17 3.5-5.5"/><path d="M12 17h.01"/>',
    "courriel": '<rect x="3" y="5" width="18" height="14" rx="2"/><path d="m3 7 9 6 9-6"/><path d="M4 3l16 18"/>',
    "memoire": '<ellipse cx="12" cy="5.5" rx="7.5" ry="2.5"/><path d="M4.5 5.5v13c0 1.4 3.4 2.5 7.5 2.5s7.5-1.1 7.5-2.5v-13"/><path d="M4.5 12c0 1.4 3.4 2.5 7.5 2.5s7.5-1.1 7.5-2.5"/>',
    # Autorités et administration
    "marteau": '<path d="m14 13-8.4 8.4a2 2 0 0 1-2.8-2.8L11.2 10"/><path d="m16 16 6-6"/><path d="m8 8 6-6"/><path d="m9 7 8 8"/><path d="m21 11-8-8"/>',
    "institution": '<path d="M3 21h18"/><path d="M5 21V11M9.5 21V11M14.5 21V11M19 21V11"/><path d="M12 3 3 8h18z"/>',
    "globe": '<circle cx="12" cy="12" r="9"/><path d="M3 12h18"/><path d="M12 3a14 14 0 0 1 0 18 14 14 0 0 1 0-18"/>',
    # Fiduciaires et conseil
    "societe": '<rect x="5" y="3" width="14" height="18" rx="1.5"/><path d="M9 7h2M13 7h2M9 11h2M13 11h2M9 15h2M13 15h2"/>',
    "audit": '<rect x="8" y="2" width="8" height="4" rx="1"/><path d="M16 4h2a2 2 0 0 1 2 2v14a2 2 0 0 1-2 2H6a2 2 0 0 1-2-2V6a2 2 0 0 1 2-2h2"/><path d="m9 14 2 2 4-4"/>',
    "fiscal": '<rect x="5" y="3" width="14" height="18" rx="2"/><path d="M8 7h8"/><path d="M8 12h.01M12 12h.01M16 12h.01M8 16h.01M12 16h.01M16 16h.01"/>',
    # LegalTechs et éditeurs
    "base": '<path d="M2 4h6a4 4 0 0 1 4 4v13a3 3 0 0 0-3-3H2z"/><path d="M22 4h-6a4 4 0 0 0-4 4v13a3 3 0 0 1 3-3h7z"/>',
    "code": '<path d="m16 18 6-6-6-6"/><path d="m8 6-6 6 6 6"/>',
    "echange": '<path d="M8 3 4 7l4 4"/><path d="M4 7h16"/><path d="m16 21 4-4-4-4"/><path d="M20 17H4"/>',
}.items()}


# Métiers concernés par chaque domaine : liens vers les pages Solutions, sous les situations
METIERS = {"cabinets-avocats": "Cabinets d'avocats", "banques-finance": "Banques et finance",
           "directions-juridiques": "Directions juridiques", "autorites-administration": "Autorités et administration",
           "fiduciaires-conseil": "Fiduciaires et conseil", "editeurs-legaltech": "LegalTechs et éditeurs"}
DOMAINE_METIERS = {
    "contrats": ["cabinets-avocats", "directions-juridiques"],
    "droit-des-societes": ["fiduciaires-conseil", "cabinets-avocats"],
    "fusions-acquisitions": ["cabinets-avocats", "banques-finance"],
    "contentieux-arbitrage": ["cabinets-avocats", "directions-juridiques"],
    "banque-finance": ["banques-finance", "fiduciaires-conseil"],
    "compliance-finma": ["banques-finance", "directions-juridiques"],
    "rapports-annuels-financiers": ["fiduciaires-conseil", "banques-finance"],
    "fiscalite": ["fiduciaires-conseil", "cabinets-avocats"],
    "assurance": ["banques-finance", "directions-juridiques"],
    "propriete-intellectuelle": ["cabinets-avocats", "directions-juridiques"],
    "droit-du-travail": ["directions-juridiques", "cabinets-avocats"],
    "droit-penal": ["cabinets-avocats", "autorites-administration"],
}


def who(titre, items, metiers=None):
    """Bloc « situations » en cartes : pictogramme facultatif (clé vis) sur la ligne du titre, puis le texte.
    metiers : slugs de pages Solutions à proposer sous les cartes."""
    def ic(w):
        return f'<span class="ws-ic">{WS_ICONS[w["vis"]]}</span>' if w.get("vis") else ""
    ws = "".join(
        f'<article class="ws-item"><h3>{ic(w)}'
        f'<span><span class="pn">{w["a"]}.</span> {w["t"]}</span></h3><p>{w["p"]}</p></article>'
        for w in items)
    return ('<section class="who who-s">\n  <div class="container">\n'
            f'    <div class="sec-head"><h2>{titre}</h2></div>\n'
            f'    <div class="ws-grid">{ws}</div>\n'
            + (f'    <p class="ws-metiers">{T("Par métier :")} ' + " · ".join(
                f'<a href="{{{{ROOT}}}}fr/solutions/{m}/">{T(METIERS[m])}</a>' for m in metiers) + "</p>\n"
               if metiers else "")
            + '  </div>\n</section>')


def voisins(titre, items, lien=None):
    """Pages voisines en cartes : le terme phare dans deux langues (allemand et français par défaut), puis le nom et le résumé."""
    if lien is None:
        lien = T("Voir le domaine")

    def terme(v):
        t = v.get("terme")
        if not t:
            return ""
        langues = v.get("langues", ("de", "fr"))
        return ('<span class="vn-term">' + "".join(
            f'<span><i>{l.upper()}</i><b lang="{l}">{t[l]}</b></span>' for l in langues) + '</span>')
    cs = "".join(
        f'<a class="vn-card" href="{{{{ROOT}}}}{v["href"]}">{terme(v)}<b class="vn-t">{v["t"]}</b>'
        f'<span class="vn-d">{v["d"]}</span><em>{lien} {ARROW}</em></a>' for v in items)
    return ('<section class="vn">\n  <div class="container">\n'
            f'    <h2>{titre}</h2>\n    <div class="vn-grid">{cs}</div>\n  </div>\n</section>')


def temoignage(t):
    """Citation client. Sans citation fournie, l'emplacement s'affiche comme « à fournir » : jamais de texte inventé."""
    if not t or not t.get("citation"):
        attente = T("Témoignage client à fournir : deux ou trois phrases d'un associé ou d'une "
                    "associée sur un dossier concret traité avec Corrext, publiées avec son accord écrit.")
        return (f'<section class="temo temo-todo" aria-label="{T("Emplacement du témoignage client à fournir")}">\n'
                '  <div class="container"><figure class="temo-fig">\n'
                '    <span class="temo-mark" aria-hidden="true">«</span>\n'
                f'    <blockquote><p>{attente}</p></blockquote>\n'
                f'    <figcaption><b>{T("Prénom Nom")}</b><span>{T("Fonction, cabinet")}</span></figcaption>\n'
                '  </figure></div>\n</section>')
    # Un exemple n'est plus étiqueté à l'écran, mais la classe temo-ex reste : la garde de production de build.py s'appuie dessus.
    ex = t.get("exemple")
    return (f'<section class="temo{" temo-ex" if ex else ""}">\n  <div class="container"><figure class="temo-fig">\n'
            + '    <span class="temo-mark" aria-hidden="true">«</span>\n'
            f'    <blockquote><p>{t["citation"]}</p></blockquote>\n'
            f'    <figcaption><b>{t["auteur"]}</b><span>{t["fonction"]}</span></figcaption>\n'
            '  </figure></div>\n</section>')


def gov(question, texte, lien, etapes):
    es = "".join(f'<div>{ICONS[i % 3]}<span><b>{e["t"]}</b> {e["d"]}</span></div>'
                 for i, e in enumerate(etapes))
    return f'''<section class="gov">
  <div class="container">
    <div class="gov-box">
      <div>
        <h2>{question}</h2>
        <p>{texte}</p>
        <a href="{{{{ROOT}}}}{lien["href"]}" class="feat-link">{lien["txt"]} {ARROW}</a>
      </div>
      <div class="gov-steps">{es}</div>
    </div>
  </div>
</section>'''


def siblings(titre, items):
    ss = "".join(f'<a href="{{{{ROOT}}}}{s["href"]}"><b>{s["t"]}</b><span>{s["d"]}</span>{ARROW}</a>'
                 for s in items)
    return f'''<section class="siblings">
  <div class="container">
    <h2>{titre}</h2>
    <div class="siblings-row">{ss}</div>
  </div>
</section>'''


def faq(titre, items):
    ds = "".join(f'<details class="faq-item"><summary>{q["q"]}</summary><p>{q["r"]}</p></details>'
                 for q in items)
    ld = {"@context": "https://schema.org", "@type": "FAQPage",
          "mainEntity": [{"@type": "Question", "name": q["q"],
                          "acceptedAnswer": {"@type": "Answer", "text": q["r"]}} for q in items]}
    return ('<script type="application/ld+json">'
            + json.dumps(ld, ensure_ascii=False) + "</script>\n"
            f'''<section class="faq" id="faq">
  <div class="container">
    <div class="faq-head"><h2>{titre}</h2></div>
    <div class="faq-list">{ds}</div>
  </div>
</section>''')


def cta(titre, texte, second=None):
    sec = (f'<a href="{{{{ROOT}}}}{second["href"]}" class="btn-outline">{second["txt"]}</a>'
           if second else "")
    return f'''<section class="final-cta">
  <div class="container">
    <div class="final-cta-inner">
      <h2>{titre}</h2>
      <p>{texte}</p>
      <div class="final-cta-btns">
        <a href="{{{{ROOT}}}}fr/contact/" class="btn btn-blue">{T("Demander une démo")} {ARROW}</a>
        {sec}
      </div>
      <p class="micro">{T("Démo sur mesure · en français, allemand, italien ou anglais · hébergement 100% suisse")}</p>
    </div>
  </div>
</section>'''


_GLOSSAIRE = None


def fiche_glossaire(de):
    """Slug de la fiche du glossaire pour un terme allemand, s'il en a une."""
    global _GLOSSAIRE
    if _GLOSSAIRE is None:
        with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "data", "glossaire.json"), encoding="utf-8") as f:
            _GLOSSAIRE = {x["de"].lower(): x["slug"] for x in json.load(f)}
    # formes du texte de loi qui renvoient à une fiche nommée autrement
    alias = {"verzug des schuldners": "schuldnerverzug", "gewährleistung wegen mängel": "gewaehrleistung",
             "einzelarbeitsvertrag": "arbeitsvertrag", "fristlose auflösung": "fristlose-kuendigung",
             "überstundenarbeit": "ueberstunden"}
    return _GLOSSAIRE.get(de.lower()) or alias.get(de.lower())


def terms_table(termes, caption, titre=None):
    if titre is None:
        titre = T("Les équivalences officielles, dans les quatre langues")

    def terme(de):
        s = fiche_glossaire(de)
        return f'<a href="{{{{ROOT}}}}fr/ressources/glossaire/{s}/">{de}</a>' if s else de
    rows = "".join(
        f'<tr><td><b>{terme(t["de"])}</b></td><td>{t["fr"]}</td><td>{t["it"]}</td><td>{t["en"]}</td>'
        f'<td class="ref">{t["ref"]}</td></tr>' for t in termes)
    # Les retours à la ligne et l'indentation font partie de la clé : la sortie FR reste identique
    note = T("Équivalences tirées des textes officiels suisses, publiés en allemand,\n"
             "      français et italien. Dans Corrext, chaque terme s'ouvre en contexte dans\n"
             "      {0}, avec sa source.").format('<a href="{{ROOT}}fr/corrext/chnell/">Fast lookup CHnell</a>')
    return f'''<section class="tterms">
  <div class="container">
    <div class="sec-head"><h2>{titre}</h2>
      <p>{caption}</p></div>
    <div class="compare-wrap">
      <table class="cmp tterms-table">
        <thead><tr><th>{T("Allemand")}</th><th>{T("Français")}</th><th>{T("Italien")}</th><th>{T("Anglais")}</th><th>{T("Référence")}</th></tr></thead>
        <tbody>{rows}</tbody>
      </table>
    </div>
    <p class="tterms-note">{note}</p>
  </div>
</section>'''


TERMS_CSS = """<style>
.tterms{padding:84px 0;background:var(--bg);border-top:1px solid var(--line);border-bottom:1px solid var(--line)}
.tterms .sec-head{margin-bottom:34px}
.tterms-table{min-width:760px}
.tterms-table td{font-size:14px}
.tterms-table td b{color:var(--navy)}
.tterms-table td b a{color:inherit;text-decoration:underline;text-decoration-color:rgba(49,123,255,.45);text-underline-offset:3px}
.tterms-table td b a:hover{color:var(--blue-d);text-decoration-color:currentColor}
.tterms-table td.ref{font-size:13px;color:var(--muted);white-space:nowrap}
.tterms-note{margin:18px auto 0;font-size:13.5px;color:var(--muted);max-width:72ch;text-align:center;text-wrap:balance}
.tterms-note a{color:var(--blue-d);font-weight:600}
.tlaws{padding:84px 0}
.tlaws-grid{display:grid;grid-template-columns:1fr 1.25fr;gap:64px;align-items:start}
.tlaws-lead{position:sticky;top:96px;align-self:start}
.tlaws h2{font-size:clamp(28px,3.4vw,40px);margin-bottom:16px;max-width:16ch}
.tlaws-lead p{color:var(--muted);font-size:16.5px;line-height:1.65;max-width:46ch}
.tlaw{display:grid;grid-template-columns:auto 1fr;gap:16px;padding:16px 0;border-bottom:1px solid var(--line);align-items:baseline}
.tlaw:first-child{border-top:1px solid var(--line)}
.tlaw .ab{font-size:13px;font-weight:800;color:var(--blue-d);font-variant-numeric:tabular-nums;white-space:nowrap}
.tlaw b{display:block;font-size:14.5px;color:var(--ink)}
.tlaw b a{color:inherit;text-decoration:underline;text-decoration-color:rgba(49,123,255,.45);text-underline-offset:3px}
.tlaw b a:hover{color:var(--blue-d);text-decoration-color:currentColor}
.tlaw p{font-size:13.5px;color:var(--muted);line-height:1.55;margin-top:3px}
@media(max-width:940px){.tlaws-grid{grid-template-columns:1fr;gap:34px}.tlaws h2{max-width:none}.tlaws-lead{position:static}}
</style>"""


_FEDLEX = None


def fedlex(cle):
    """Adresse Fedlex (version française en vigueur) d'un texte, par abréviation ou par nom."""
    global _FEDLEX
    if _FEDLEX is None:
        with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "data", "fedlex.json"), encoding="utf-8") as f:
            _FEDLEX = json.load(f)
        for k, v in list(_FEDLEX.items()):
            _FEDLEX[v["nom"].lower()] = v
        for nom, k in (("loi sur la poursuite pour dettes et la faillite", "LP"),
                       ("loi fédérale sur le tribunal fédéral", "LTF"), ("code civil suisse", "CC")):
            _FEDLEX[nom] = _FEDLEX[k]
    v = _FEDLEX.get(cle) or _FEDLEX.get(cle.lower()) or _alias_loi(cle)
    if not v:
        return None
    # version linguistique du texte : allemand et italien existent pour tout le droit fédéral ; l'anglais au cas par cas
    lang = i18n.langue()
    if lang in ("de", "it"):
        return v["url"][:-2] + lang
    if lang == "en":
        return v.get("url_en") or v["url"][:-2] + "de"
    return v["url"]


_ALIAS = {}


def _alias_loi(nom):
    """Nom d'une loi dans la langue de la page -> fiche Fedlex, d'après la base terminologique (src/i18n/termes-<lang>.json)."""
    lang = i18n.langue()
    if lang == "fr":
        return None
    if lang not in _ALIAS:
        _ALIAS[lang] = {}
        p = os.path.join(os.path.dirname(os.path.abspath(__file__)), "i18n", f"termes-{lang}.json")
        if os.path.exists(p):
            for t in json.load(open(p, encoding="utf-8")):
                fr, tr = (t.get("fr") or "").strip(), (t.get(lang) or "").strip()
                v = _FEDLEX.get(fr) or _FEDLEX.get(fr.lower())
                if v and tr:
                    _ALIAS[lang][tr.lower()] = v
    return _ALIAS[lang].get(nom.lower().strip())


def lien_loi(nom, cle):
    u = fedlex(cle) or fedlex(nom)
    return f'<a href="{u}" rel="noopener" target="_blank">{nom}</a>' if u else nom


def laws_block(titre, intro, lois):
    ls = "".join(
        f'<div class="tlaw"><span class="ab">{l["abbr"]}</span><div><b>{lien_loi(l["nom"], l["abbr"])}</b>'
        f'<p>{l["note"]}</p></div></div>' for l in lois)
    return f'''<section class="tlaws">
  <div class="container">
    <div class="tlaws-grid">
      <div class="tlaws-lead"><h2>{titre}</h2><p>{intro}</p></div>
      <div class="tlaws-list">{ls}</div>
    </div>
  </div>
</section>'''


# ---------------------------------------------------------------- familles

def gen_solutions(src):
    pages = []
    data = load(src, "solutions")
    for d in data:
        body = "\n".join([
            hero_job(d["lede"], d["h1"], d["lead"], d["promesses"],
                     T("Ce métier, en trois points")),
            facts(d["facts_titre"], d["facts_intro"], d["facts_liens"], d["facts"]),
            who(d["who_titre"], d["who"]),
            gov(d["gov_q"], d["gov_p"], d["gov_lien"], d["gov_etapes"]),
            outils_visuel(d["outils_titre"], d["outils"]),
            temoignage(d.get("temoignage")),
            faq(d["faq_titre"], d["faq"]),
            cta(d["cta_t"], d["cta_p"], {"href": "fr/corrext/", "txt": T("Voir la plateforme")}),
        ])
        pages.append((f'fr/solutions/{d["slug"]}/',
                      {"title": d["title"], "description": d["description"],
                       "short": d["short"], "nav": "solutions"}, body))
    if data:
        cards = "".join(
            f'<a href="{{{{ROOT}}}}fr/solutions/{d["slug"]}/"><b>{d["short"]}</b>'
            f'<span>{d["resume"]}</span>{ARROW}</a>' for d in data)
        body = "\n".join([
            hero(T("Solutions."), T("Le même socle suisse, adapté à votre métier"),
                 T("Un cabinet d'avocats, une banque et une autorité cantonale ne traduisent ni les "
                   "mêmes documents, ni pour les mêmes raisons. Voici ce que Corrext change pour "
                   "chacun, avec les mêmes garanties de confidentialité."),
                 "solutions",
                 "#metiers", T("Voir les six métiers")),
            f'''<section class="siblings" id="metiers" style="padding:84px 0">
  <div class="container"><h2>{T("Par métier")}</h2>
    <div class="siblings-row solutions-row">{cards}</div></div>
</section>
<style>.solutions-row{{grid-template-columns:repeat(3,1fr)}}
@media(max-width:940px){{.solutions-row{{grid-template-columns:1fr}}}}</style>''',
            siblings(T("Explorer autrement"), [
                {"href": "fr/traduction/", "t": T("Par domaine du droit"),
                 "d": T("Douze domaines, leur terminologie et leurs textes de référence")},
                {"href": "fr/comparatif/", "t": T("Par comparaison"),
                 "d": T("Corrext face à DeepL, aux LLM généralistes et à l'agence externe")},
                {"href": "fr/corrext/", "t": T("Par outil"),
                 "d": T("Les quatre outils de la plateforme, démonstration à l'appui")}]),
            cta(T("Voyez Corrext sur les documents de votre métier"),
                T("Une démonstration sur mesure, menée par un spécialiste du droit suisse."),
                {"href": "fr/corrext/", "txt": T("Voir la plateforme")}),
        ])
        pages.append(("fr/solutions/", {
            "title": T("Solutions par métier · Neur.on, traduction juridique suisse"),
            "description": T("Avocats, banques, directions juridiques, autorités, fiduciaires, "
                             "éditeurs : ce que Corrext change pour chaque métier, stockage en Suisse compris."),
            "short": T("Solutions"), "nav": "solutions"}, body))
    return pages


def gen_domaines(src):
    pages, data = [], load(src, "domaines")
    for d in data:
        vois = [v for v in data if v["slug"] in d.get("voisins", [])][:3]
        t0 = d["termes"][0]
        spec = {"titre": T("Terminologie officielle"), "compte": T("{0} termes").format(len(d["termes"])),
                "mots": t0, "pied": T("{0} · vérifiable dans Fast lookup CHnell").format(t0["ref"])}
        body = "\n".join([
            TERMS_CSS,
            hero_law(d["lede"], d["h1"], d["lead"], spec),
            facts(d.get("facts_titre", T("Concrètement, dans Corrext")), d["definition"],
                  [{"href": "fr/corrext/traduction-texte-et-document/", "txt": T("Traduire un document maintenant")},
                   {"href": "fr/corrext/gestion-de-projet/", "txt": T("Commander une relecture juridique")}],
                  d["facts"]),
            terms_table(d["termes"], d["termes_note"], d.get("termes_titre", T("La terminologie officielle, dans les quatre langues"))),
            laws_block(d.get("lois_titre", T("Les textes de référence, cités au quotidien")), d["lois_intro"], d["lois"]),
            who(d["who_titre"], d["who"], DOMAINE_METIERS.get(d["slug"])),
            faq(d["faq_titre"], d["faq"]),
            voisins(T("Autres domaines"),
                    [{"href": f'fr/traduction/{v["slug"]}/', "t": v["short"], "d": v["resume"],
                      "terme": v["termes"][0]} for v in vois] or
                    [{"href": "fr/traduction/", "t": T("Tous les domaines"),
                      "d": T("Les douze domaines couverts")}]),
            cta(d["cta_t"], d["cta_p"], {"href": "fr/traduction/", "txt": T("Tous les domaines")}),
        ])
        pages.append((f'fr/traduction/{d["slug"]}/',
                      {"title": d["title"], "description": d["description"],
                       "short": d["short"], "nav": "solutions", "hero": "law"}, body))
    return pages


LANGUES = {"allemand": "de", "francais": "fr", "italien": "it", "anglais": "en"}


def gen_paires(src):
    pages, data = [], load(src, "paires")
    par_slug = {p["slug"]: p for p in data}
    for d in data:
        t0 = d["termes"][0]
        spec = {"titre": T("Un terme, quatre langues"), "compte": T("{0} termes").format(len(d["termes"])),
                "mots": t0, "pied": T("{0} · publié dans les langues officielles").format(t0["ref"])}
        body = "\n".join([
            TERMS_CSS,
            hero_law(d["lede"], d["h1"], d["lead"], spec, "#faits", T("Ce qui change dans cette paire")),
            facts(T("Cette paire de langues, en pratique"), d["definition"],
                  [{"href": "fr/corrext/traduction-texte-et-document/", "txt": T("Essayer sur un extrait de loi")},
                   {"href": "fr/langues-et-formats/", "txt": T("Toutes les langues et formats")}],
                  d["facts"]),
            terms_table(d["termes"], d["termes_note"]),
            who(d["who_titre"], d["who"]),
            faq(d["faq_titre"], d["faq"]),
            voisins(T("Autres paires de langues"),
                    [{"href": f'fr/traduction/{v}/', "t": t, "d": r,
                      "terme": par_slug[v]["termes"][0] if v in par_slug else None,
                      "langues": tuple(LANGUES[x] for x in v.split("-"))}
                     for v, t, r in d["voisins"]], T("Voir la paire")),
            cta(d["cta_t"], d["cta_p"], {"href": "fr/traduction/", "txt": T("Traduction par domaine")}),
        ])
        pages.append((f'fr/traduction/{d["slug"]}/',
                      {"title": d["title"], "description": d["description"],
                       "short": d["short"], "nav": "solutions", "hero": "law"}, body))
    return pages


def gen_traduction_hub(src):
    dom, pai = load(src, "domaines"), load(src, "paires")
    if not dom and not pai:
        return []
    dcards = "".join(
        f'<a href="{{{{ROOT}}}}fr/traduction/{d["slug"]}/"><b>{d["short"]}</b>'
        f'<span>{d["resume"]}</span>{ARROW}</a>' for d in dom)
    pcards = "".join(
        f'<a href="{{{{ROOT}}}}fr/traduction/{p["slug"]}/"><b>{p["short"]}</b>'
        f'<span>{p["resume"]}</span>{ARROW}</a>' for p in pai)
    body = "\n".join([
        hero(T("Traduction juridique et financière."), T("Par domaine du droit et par paire de langues"),
             T("Le vocabulaire d'un prospectus de fonds n'est pas celui d'une sentence arbitrale, et "
               "l'allemand juridique suisse n'est pas l'allemand de Berlin. Chaque page ci-dessous "
               "donne la terminologie officielle, les textes de référence et la façon dont Corrext "
               "les traite."),
             "traduction",
             "#domaines", T("Voir les domaines")),
        f'''<section class="siblings" id="domaines" style="padding:84px 0">
  <div class="container"><h2>{T("Par domaine du droit et de la finance")}</h2>
    <div class="siblings-row grid3">{dcards}</div></div>
</section>''',
        f'''<section class="siblings" id="langues" style="padding:0 0 84px">
  <div class="container"><h2>{T("Par paire de langues")}</h2>
    <div class="siblings-row grid3">{pcards}</div></div>
</section>
<style>.grid3{{grid-template-columns:repeat(3,1fr)}}
@media(max-width:940px){{.grid3{{grid-template-columns:1fr}}}}</style>''',
        cta(T("Votre domaine n'est pas dans la liste ?"),
            T("Corrext couvre 30 domaines dans son concordancier et 30 langues sur la plateforme. "
              "Dites-nous ce que vous traduisez."),
            {"href": "fr/corrext/chnell/", "txt": T("Voir Fast lookup CHnell")}),
    ])
    return [("fr/traduction/", {
        "title": T("Traduction juridique par domaine et par langue · Neur.on"),
        "description": T("Douze domaines du droit suisse et les principales paires de langues : "
                         "la terminologie officielle en allemand, français, italien et anglais, et ses sources."),
        "short": T("Traduction"), "nav": "solutions"}, body)]


def source_liee(source):
    """« Fedlex, Code des obligations » : le nom du texte renvoie à sa page Fedlex."""
    base, _, nom = source.partition(", ")
    u = fedlex(nom) if nom else None
    return f'{base}, <a href="{u}" rel="noopener" target="_blank">{nom}</a>' if u else source


def gen_glossaire(src):
    pages, data = [], load(src, "glossaire")
    if not data:
        return []
    css = """<style>
.gterm{padding:70px 0}
.gterm-grid{display:grid;grid-template-columns:1.1fr 1fr;gap:56px;align-items:start}
.gdef{font-size:18px;line-height:1.6;color:var(--ink);max-width:56ch}
.gmeta{margin-top:22px;display:flex;flex-wrap:wrap;gap:8px}
.gmeta span{font-size:12px;font-weight:700;background:var(--tint);color:var(--navy);border-radius:50px;padding:5px 12px}
.glangs{border-top:1px solid var(--line)}
.gnote{background:var(--bg);border:1px solid var(--line);border-radius:var(--r-bloc);padding:26px 28px}
.gnote p{font-size:14.5px;color:var(--text);line-height:1.65;margin-bottom:16px}
.glang{display:grid;grid-template-columns:96px 1fr;gap:14px;padding:13px 0;border-bottom:1px solid var(--line);align-items:baseline}
.glang i{font-style:normal;font-size:12px;font-weight:700;color:var(--muted);letter-spacing:.06em;text-transform:uppercase}
.glang b{font-size:16px;color:var(--ink)}
.gex{padding:0 0 84px}
.gex-box{background:var(--bg);border:1px solid var(--line);border-radius:var(--r-bloc);padding:32px 34px}
.gex-box h2{font-size:22px;margin-bottom:18px}
.gex-row{display:grid;grid-template-columns:1fr 1fr;gap:28px}
.gex-row div p{font-size:14.5px;line-height:1.6;color:var(--text)}
.gex-row div i{font-style:normal;display:block;font-size:12px;font-weight:700;color:var(--muted);text-transform:uppercase;letter-spacing:.06em;margin-bottom:7px}
.gex-row mark{background:#fff2a8;padding:0 2px}
.gsrc{margin-top:18px;font-size:13px;color:var(--muted)}
.gsrc a{color:var(--blue-d);text-decoration:underline;text-underline-offset:2px}
@media(max-width:940px){.gterm-grid,.gex-row{grid-template-columns:1fr;gap:28px}}
</style>"""
    for d in data:
        vois = [v for v in data if v["slug"] in d.get("voisins", [])][:3]
        body_hero = hero_law(
            d["de"], "· " + equivalent(d), d["lead"],
            {"titre": T("Le terme, quatre langues"), "compte": d["domaine"],
             "mots": {k: d[k] for k in ("de", "fr", "it", "en")},
             "pied": T("{0} · source : {1}").format(d["base"], d["source"])},
            "#definition", T("Lire la définition"))
        # Données structurées : le terme allemand, ses équivalents officiels et sa source
        ld_terme = {"@context": "https://schema.org", "@type": "DefinedTerm", "name": d["de"], "inLanguage": "de-CH",
                    "alternateName": [d["fr"], d["it"], d["en"]], "description": d["resume"],
                    "termCode": d["base"], "url": f'{SITE}/fr/ressources/glossaire/{d["slug"]}/',
                    "inDefinedTermSet": {"@type": "DefinedTermSet", "name": T("Glossaire juridique suisse"),
                                         "url": f"{SITE}/fr/ressources/glossaire/"}}
        # Les retours à la ligne et l'indentation font partie des clés : la sortie FR reste identique
        lex = langue_exemple(d["exemple"])
        gnote = T("Les lois fédérales suisses sont publiées en allemand, en français et en italien, et les\n"
                  "          trois versions font foi. L'équivalence ci-contre n'est donc pas une traduction d'usage :\n"
                  "          c'est le terme employé par le texte officiel lui-même.")
        gsrc = T("Source : {0}. Dans Corrext, ce segment et ceux qui l'entourent\n"
                 "        s'affichent dans {1},\n"
                 "        chacun avec sa référence.").format(
            source_liee(d["source"]), '<a href="{{ROOT}}fr/corrext/chnell/">Fast lookup CHnell</a>')
        body = "\n".join([css, '<script type="application/ld+json">' + json.dumps(ld_terme, ensure_ascii=False) + "</script>", body_hero,
            f'''<section class="gterm" id="definition">
  <div class="container">
    <div class="gterm-grid">
      <div>
        <h2>{T("Définition")}</h2>
        <p class="gdef">{d["definition"]}</p>
        <div class="gmeta"><span>{d["domaine"]}</span><span>{d["base"]}</span></div>
      </div>
      <div class="gnote">
        <p>{gnote}</p>
        <a class="feat-link" href="{{{{ROOT}}}}fr/ressources/glossaire/">{T("Tout le glossaire")} {ARROW}</a>
      </div>
    </div>
  </div>
</section>''',
            f'''<section class="gex">
  <div class="container">
    <div class="gex-box">
      <h2>{T("Le terme dans un texte officiel")}</h2>
      <div class="gex-row">
        <div><i>{T("Allemand")}</i><p lang="de">{d["exemple"]["de"]}</p></div>
        <div><i>{T(NOM_LANGUE[lex])}</i><p lang="{lex}">{d["exemple"][lex]}</p></div>
      </div>
      <p class="gsrc">{gsrc}</p>
    </div>
  </div>
</section>''',
            siblings(T("Termes voisins"),
                     [{"href": f'fr/ressources/glossaire/{v["slug"]}/',
                       "t": f'{v["de"]} · {equivalent(v)}', "d": v["resume"]} for v in vois] or
                     [{"href": "fr/ressources/glossaire/", "t": T("Tout le glossaire"),
                       "d": T("La terminologie juridique suisse en quatre langues")}]),
            cta(T("Cette terminologie, appliquée à vos documents"),
                T("Corrext vérifie chaque terme dans son contexte officiel et garde vos choix "
                  "cohérents d'un document à l'autre."),
                {"href": "fr/corrext/chnell/", "txt": T("Découvrir CHnell")}),
        ])
        pages.append((f'fr/ressources/glossaire/{d["slug"]}/', {
            "title": d["title"], "description": d["description"],
            "short": f'{d["de"]} · {equivalent(d)}', "nav": "ressources", "hero": "law"}, body))

    # index du glossaire
    rows = "".join(
        f'<a href="{{{{ROOT}}}}fr/ressources/glossaire/{d["slug"]}/" class="grow2">'
        f'<b lang="de">{d["de"]}</b><span class="fr">{d["fr"]}</span>'
        f'<span class="it" lang="it">{d["it"]}</span><span class="en" lang="en">{d["en"]}</span><span class="dom"><em>{d["domaine"]}</em></span></a>'
        for d in sorted(data, key=lambda x: x["de"].lower()))
    # En-tête de colonnes : chaque langue reste dans sa colonne, d'une ligne à l'autre
    entete = (f'<div class="ghead" aria-hidden="true"><span>{T("Allemand")}</span><span>{T("Français")}</span>'
              f'<span>{T("Italien")}</span><span>{T("Anglais")}</span><span>{T("Domaine")}</span></div>')
    body = "\n".join([
        """<style>
.glist{padding:84px 0}
.glist-head{margin-bottom:28px}
/* Colonnes de largeur fixe, identiques pour l'en-tête et chaque ligne : les termes s'alignent verticalement */
.ghead,.grow2{display:grid;grid-template-columns:minmax(0,1.1fr) minmax(0,1fr) minmax(0,1fr) minmax(0,1fr) 196px;column-gap:22px;align-items:baseline;padding:0 12px;margin:0 -12px}
.ghead{padding-bottom:10px;border-bottom:1px solid var(--line-2)}
.ghead span{font-size:11.5px;font-weight:700;letter-spacing:.07em;text-transform:uppercase;color:var(--muted)}
.grow2{padding-top:15px;padding-bottom:15px;border-bottom:1px solid var(--line);transition:background .15s}
.grow2:hover{background:rgba(49,123,255,.04)}
.grow2>*{min-width:0;overflow-wrap:anywhere}
.grow2 b{font-size:15.5px;color:var(--navy)}
.grow2 .fr{font-size:14.5px;color:var(--ink)}
.grow2 .it,.grow2 .en{font-size:14px;color:var(--muted)}
.grow2 .dom em{display:inline-block;font-style:normal;font-size:11.5px;font-weight:700;color:var(--blue-d);background:var(--tint);border-radius:50px;padding:4px 11px;white-space:nowrap}
@media(max-width:940px){.ghead{display:none}.grow2{grid-template-columns:1fr 1fr;gap:6px 14px}.grow2 .dom{grid-column:1 / -1}}
</style>""",
        hero(T("Glossaire juridique suisse."), T("Chaque terme dans les quatre langues, avec sa source"),
             T("Les lois suisses sont publiées en allemand, en français et en italien : dans ces "
               "trois langues, les équivalences ci-dessous sont les termes des textes officiels. "
               "L'anglais suit les traductions publiées sur Fedlex, qui n'ont pas force de loi. "
               "Chaque terme renvoie à son article et à sa source."),
             "glossaire",
             "#liste", T("Voir les termes")),
        f'''<section class="glist" id="liste">
  <div class="container">
    <div class="sec-head glist-head"><h2>{T("Les termes")}</h2>
      <p>{T("Classés par terme allemand. Le glossaire s'étoffe au fil des vérifications de nos\n        juristes-linguistes.")}</p></div>
    {entete}{rows}
  </div>
</section>''',
        cta(T("Votre terminologie, appliquée partout"),
            T("CHnell couvre 30 domaines et vos propres ressources s'y ajoutent."),
            {"href": "fr/corrext/chnell/", "txt": T("Découvrir CHnell")}),
    ])
    ld_set = {"@context": "https://schema.org", "@type": "DefinedTermSet", "name": T("Glossaire juridique suisse"),
              "inLanguage": ["de-CH", "fr-CH", "it-CH", "en"], "url": f"{SITE}/fr/ressources/glossaire/",
              "hasDefinedTerm": [{"@type": "DefinedTerm", "name": d["de"], "alternateName": [d["fr"], d["it"], d["en"]],
                                  "url": f'{SITE}/fr/ressources/glossaire/{d["slug"]}/'} for d in data]}
    body = '<script type="application/ld+json">' + json.dumps(ld_set, ensure_ascii=False) + "</script>\n" + body
    pages.append(("fr/ressources/glossaire/", {
        "title": T("Glossaire juridique suisse en quatre langues · Neur.on"),
        "description": T("52 termes du droit suisse en allemand, français, italien et anglais, avec "
                         "la base légale, la source officielle et un exemple tiré de la loi."),
        "short": T("Glossaire"), "nav": "ressources"}, body))
    return pages


def _js(s):
    """Texte inséré dans une chaîne JavaScript entre apostrophes : barre oblique inverse et apostrophe échappées."""
    return s.replace("\\", "\\\\").replace("'", "\\'")


def gen_aide(src):
    """Centre d'aide : accueil avec recherche, deux espaces (utilisateurs, administrateurs),
    une page par rubrique avec ses questions en accordéon (ancre par question)."""
    data = load(src, "aide")
    if not data:
        return []
    ESPACES = (("utilisateur", T("Utiliser Corrext"), T("Traduire, faire relire, vérifier un terme : les gestes du quotidien dans l'application.")),
               ("admin", T("Administrer Corrext"), T("Pour les administrateurs : membres et rôles, politique de moteurs, mémoires et terminologie de l'organisation.")))
    plat = lambda h: re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", h)).strip()

    def reponse(x):
        h = f'<p>{x["reponse"]}</p>'
        if x["etapes"]:
            h += '<ol class="hc-steps">' + "".join(f"<li>{e}</li>" for e in x["etapes"]) + "</ol>"
        if x.get("savoir"):
            h += f'<div class="hc-know"><b>{T("À savoir")}</b><ul>' + "".join(f"<li>{s}</li>" for s in x["savoir"]) + "</ul></div>"
        return h

    index = [{"q": x["question"], "t": plat(" ".join([x["reponse"]] + x["etapes"] + x.get("savoir", []))),
              "r": r["titre"], "e": T("Administrateurs") if r["espace"] == "admin" else T("Utilisateurs"),
              "u": f'{{{{ROOT}}}}fr/aide/{r["slug"]}/#{x["slug"]}'} for r in data for x in r["articles"]]
    recherche = lambda grande: f'''<form class="hc-search{" big" if grande else ""}" action="{{{{ROOT}}}}fr/aide/" role="search">
  <label class="sr-only" for="hc-q">{T("Rechercher dans le centre d'aide")}</label>
  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" aria-hidden="true"><circle cx="11" cy="11" r="7"/><path d="m20 20-3.5-3.5"/></svg>
  <input id="hc-q" name="q" type="search" autocomplete="off" placeholder="{T("Rechercher une question (ex : traduire un fichier, devis, ajouter un membre)")}">
  {'<div class="hc-results" id="hc-results" role="listbox" hidden></div>' if grande else ''}
</form>'''
    side = lambda courant: (f'<nav class="hc-side" aria-label="{T("Rubriques du centre d'aide")}">'
                            f'<a class="hc-back" href="{{{{ROOT}}}}fr/aide/"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M19 12H5M11 19l-7-7 7-7"/></svg>{T("Centre d'aide")}</a>') + "".join(
        f'<p class="hc-side-t">{titre}</p><ul>' + "".join(
            f'<li><a href="{{{{ROOT}}}}fr/aide/{r["slug"]}/"{" aria-current=\"page\"" if r["slug"] == courant else ""}>'
            f'<span class="ws-ic">{WS_ICONS[r["icone"]]}</span>{r["titre"]}</a></li>' for r in data if r["espace"] == esp) + "</ul>"
        for esp, titre, _ in ESPACES) + "</nav>"
    contact = cta(T("Une question reste sans réponse ?"),
                  T("Écrivez à team@corrext.com : l'équipe Neur.on répond en français, en allemand, en italien et en anglais, et vous aide à démarrer avec Corrext."),
                  {"href": "fr/contact/", "txt": T("Contacter l'équipe")})
    script_ancre = """<script>(function(){function o(){var h=decodeURIComponent(location.hash.slice(1));if(!h)return;var d=document.getElementById(h);if(d&&d.tagName==='DETAILS'){d.open=true;d.scrollIntoView({block:'start'});}}window.addEventListener('hashchange',o);o();})();</script>"""

    pages = []
    for r in data:
        n = len(r["articles"])
        qs = "".join(f'<details class="faq-item hc-q" id="{x["slug"]}"><summary>{x["question"].replace(" ?", "\u00a0?")}</summary><div class="hc-a">{reponse(x)}</div></details>'
                     for x in r["articles"])
        ld = {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
            {"@type": "Question", "name": x["question"], "acceptedAnswer": {"@type": "Answer", "text": plat(reponse(x))}} for x in r["articles"]]}
        espace = T("Administrateurs") if r["espace"] == "admin" else T("Utilisateurs")
        body = "\n".join([
            '<script type="application/ld+json">' + json.dumps(ld, ensure_ascii=False) + "</script>",
            f'''<section class="hc" id="questions">
  <div class="container">
    <div class="hc-grid">
      {side(r["slug"])}
      <div class="hc-main">
        <p class="hc-kicker">{T("Centre d'aide")} · {espace}</p>
        <h1 class="hc-h1">{r["titre"]}</h1>
        <p class="hc-intro">{r["lead"]}</p>
        <div class="faq-list hc-list">{qs}</div>
      </div>
    </div>
  </div>
</section>''',
            contact, script_ancre,
        ])
        pages.append((f'fr/aide/{r["slug"]}/', {"title": r["title"], "description": r["description"],
                                                 "short": r["titre"], "nav": "ressources", "hero": "aide"}, body))

    total = sum(len(r["articles"]) for r in data)
    blocs = "".join(
        f'''<section class="hc-space{" admin" if esp == "admin" else ""}" id="{esp}">
  <div class="container">
    <div class="hc-space-head"><span class="hc-badge">{T("Administrateurs") if esp == "admin" else T("Utilisateurs")}</span><h2>{titre}</h2><p>{texte}</p></div>
    <div class="hc-cards">''' + "".join(
            f'<a class="hc-card" href="{{{{ROOT}}}}fr/aide/{r["slug"]}/"><span class="ws-ic">{WS_ICONS[r["icone"]]}</span>'
            f'<b>{r["titre"]}</b><span class="d">{r["lead"]}</span><em>{T("{0} questions").format(len(r["articles"]))} {ARROW}</em></a>'
            for r in data if r["espace"] == esp) + '''</div>
  </div>
</section>''' for esp, titre, texte in ESPACES)
    moteur = """<script>(function(){var I=window.HC_INDEX||[],f=document.querySelector('.hc-search.big'),q=document.getElementById('hc-q'),box=document.getElementById('hc-results');if(!f||!q||!box)return;
function n(s){return (s||'').toLowerCase().normalize('NFD').replace(/[\\u0300-\\u036f]/g,'').replace(/[^a-z0-9' ]+/g,' ');}
var V=I.map(function(x){return {x:x,q:n(x.q),t:n(x.t),r:n(x.r)};});
function esc(s){return s.replace(/[&<>"]/g,function(c){return {'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c];});}
function cherche(v){var m=n(v).split(' ').filter(function(w){return w.length>1;});if(!m.length){box.hidden=true;box.innerHTML='';return [];}
var r=V.map(function(o){var s=0;m.forEach(function(w){if(o.q.indexOf(w)>-1)s+=4;if(o.r.indexOf(w)>-1)s+=2;if(o.t.indexOf(w)>-1)s+=1;});return {o:o,s:s};}).filter(function(a){return a.s>0;}).sort(function(a,b){return b.s-a.s;}).slice(0,8);
box.innerHTML=r.length?r.map(function(a){return '<a role="option" href="'+a.o.x.u+'"><b>'+esc(a.o.x.q)+'</b><span>'+esc(a.o.x.e)+' · '+esc(a.o.x.r)+'</span></a>';}).join(''):'<p class="none">""" + _js(T("Aucune réponse pour « {0} ». Essayez un autre mot, ou contactez l'équipe.")).format("'+esc(v)+'") + """</p>';box.hidden=false;return r;}
q.addEventListener('input',function(){cherche(q.value);});
f.addEventListener('submit',function(e){e.preventDefault();var r=cherche(q.value);if(r.length)location.href=r[0].o.x.u;});
var p=new URLSearchParams(location.search).get('q');if(p){q.value=p;cherche(p);}})();</script>"""
    body = "\n".join([
        f'''<section class="hc-hero">
  <div class="container">
    <p class="hc-kicker">{T("Centre d'aide")}</p>
    <h1>{T("Comment {0} vous aider\u00a0?").format(f'<span class="nw">{T("pouvons-nous")}</span>')}</h1>
    <p class="lead">{T("Toutes les réponses pour utiliser Corrext au quotidien et pour l'administrer, vérifiées dans l'application.")}</p>
    {recherche(True)}
  </div>
</section>''',
        blocs, contact,
        "<script>window.HC_INDEX=" + json.dumps(index, ensure_ascii=False).replace("</", "<\\/") + ";</script>", moteur,
    ])
    pages.append(("fr/aide/", {"hero": "aide", "title": T("Centre d'aide Corrext · Neur.on"),
                               "description": T("{0} réponses sur Corrext, vérifiées dans l'application : traduire, faire relire, vérifier un terme, sécurité, et administration de votre organisation.").format(total),
                               "short": T("Centre d'aide"), "nav": "ressources"}, body))
    return pages


# ============ BLOG ============
# Source unique : src/data/blog.json. Chaque entrée décrit un article ; "page": "manuelle" pour les
# articles de fond écrits à la main dans src/pages (ils appellent {{BLOG:entete:slug}} et
# {{BLOG:recents:slug}}), "page": "generee" pour les articles dont le corps est dans le JSON.
SITE = "https://neur-on.ai"
_SVG ='<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">'
BLOG_IC = {
    "auteur": _SVG + '<path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"/><circle cx="12" cy="7" r="4"/></svg>',
    "date": _SVG + '<rect x="3" y="4" width="18" height="18" rx="2"/><path d="M16 2v4M8 2v4M3 10h18"/></svg>',
    "duree": _SVG + '<circle cx="12" cy="12" r="10"/><path d="M12 6v6l4 2"/></svg>',
    "une": _SVG + '<path d="M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01z"/></svg>',
}
SHARE = {
    "li": ('Partager sur LinkedIn', 'https://www.linkedin.com/sharing/share-offsite/?url={u}',
           '<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M20.45 20.45h-3.56v-5.57c0-1.33-.02-3.04-1.85-3.04-1.85 0-2.14 1.45-2.14 2.94v5.67H9.35V9h3.41v1.56h.05c.48-.9 1.64-1.85 3.37-1.85 3.6 0 4.27 2.37 4.27 5.46v6.28zM5.34 7.43a2.06 2.06 0 1 1 0-4.13 2.06 2.06 0 0 1 0 4.13zM7.12 20.45H3.56V9h3.56v11.45zM22.22 0H1.77C.79 0 0 .77 0 1.73v20.54C0 23.23.79 24 1.77 24h20.45c.98 0 1.78-.77 1.78-1.73V1.73C24 .77 23.2 0 22.22 0z"/></svg>'),
    "x": ('Partager sur X', 'https://twitter.com/intent/tweet?url={u}&amp;text={t}',
          '<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M18.24 2.25h3.31l-7.23 8.26 8.5 11.24h-6.66l-5.21-6.82-5.97 6.82H1.67l7.73-8.84L1.25 2.25h6.83l4.71 6.23 5.45-6.23zm-1.16 17.52h1.83L7.08 4.13H5.12l11.96 15.64z"/></svg>'),
    "mail": ('Envoyer par e-mail', 'mailto:?subject={t}&amp;body={u}',
             _SVG + '<rect x="2" y="4" width="20" height="16" rx="2"/><path d="m22 6-10 7L2 6"/></svg>'),
}


BLOG_OUTILS = [
    ("jauge", "Corrext ou DeepL", "Le comparatif pour le droit suisse : lieu de traitement, terminologie, chaîne de relecture.", "fr/comparatif/deepl-traduction-juridique/"),
    ("bouclier", "Sécurité et souveraineté", "Serveurs suisses, mode Highly sensitive content, ISO 27001, nLPD et RGPD.", "fr/securite-souverainete/"),
    ("etiquette", "Glossaire quadrilingue", "Les termes du droit suisse en allemand, français, italien et anglais, avec leurs sources.", "fr/ressources/glossaire/"),
    ("rapport", "Guides", "Des méthodes longues et applicables : organiser la traduction, préparer un rapport annuel multilingue.", "fr/ressources/guides/"),
    ("loupe", "Centre d'aide", "Des réponses vérifiées dans l'application : traduire, faire relire, vérifier un terme, administrer Corrext.", "fr/aide/"),
    ("calendrier", "Actualités", "Prix, conférences, partenariats et presse : toutes les brèves de Neur.on depuis 2020.", "fr/ressources/blog/actualites/"),
]
LINKEDIN = "https://www.linkedin.com/company/neur-on"


def a_propos():
    """Encadré « À propos de Neur.on » en fin d'article : les liens restent hors des clés."""
    texte = T("Neur.on AI Solutions SA, à Fribourg, édite {0}, la plateforme suisse de traduction juridique et financière, "
              "et son moteur de traduction neuronale {1}, entraîné sur la donnée juridique et financière suisse.").format(
        '<a href="{{ROOT}}fr/corrext/">Corrext</a>', '<a href="{{ROOT}}fr/lexmachina/">LexMachina</a>')
    return f'<aside class="ar-about"><b>{T("À propos de Neur.on")}</b><p>{texte}</p></aside>'


def blog_outils():
    cartes = "".join(f'<a class="bl-seg-card" href="{{{{ROOT}}}}{u}"><span class="ws-ic">{WS_ICONS[ic]}</span><b>{T(t)}</b><span>{T(d)}</span></a>'
                     for ic, t, d, u in BLOG_OUTILS)
    return (f'<section class="bl-seg"><div class="container"><div class="sec-head"><span class="bl-k">{T("Ressources et outils")}</span>'
            f'<h2>{T("Pour passer de la lecture à la pratique")}</h2><p>{T("Un comparatif, une page sécurité, un glossaire quadrilingue, des guides, le centre d'aide et l'historique de nos actualités.")}'
            f'</p></div><div class="bl-seg-grid">{cartes}</div></div></section>')


def blog_linkedin():
    return ('<section class="bl-li"><div class="container"><div class="bl-li-band"><div><span class="bl-k">LinkedIn</span>'
            f'<h2>{T("Les nouveaux articles et actualités, dès leur parution")}</h2>'
            f'<p>{T("Neur.on publie ses articles, ses conférences et ses actualités sur sa page LinkedIn. Suivez-la pour ne rien manquer.")}</p></div>'
            f'<a class="btn btn-blue" href="{LINKEDIN}" target="_blank" rel="noopener">{T("Suivre Neur.on sur LinkedIn")} {ARROW}</a></div></div></section>')


def blog_articles(src):
    """Articles triés du plus récent au plus ancien."""
    return sorted(load(src, "blog"), key=lambda a: a["date"], reverse=True)


def blog_url(a):
    return f'fr/ressources/blog/{a["slug"]}/'


def blog_visuel(a, une=False):
    """Bandeau de carte : photo de l'article si elle existe, sinon dégradé bleu nuit ; catégorie et signature."""
    img = a.get("vignette") or a.get("image")
    tag = (f'<span class="bl-tag">{BLOG_IC["une"]}{T("À la une")}</span>' if une else f'<span class="bl-tag">{T(a["categorie"])}</span>')
    photo = (f'<img src="{{{{ROOT}}}}{img["src"]}" alt="" width="{img["w"]}" height="{img["h"]}" loading="lazy" decoding="async">'
             if img else "")
    return (f'<div class="bl-vis{" photo" if img else ""}">{photo}{tag}'
            f'<span class="bl-mark" aria-hidden="true">NEUR<span>.ON</span></span></div>')


def blog_carte(a):
    return (f'<a class="bl-card" href="{{{{ROOT}}}}{blog_url(a)}" data-cat="{a["categorie"]}">{blog_visuel(a)}'
            f'<div class="bl-body"><span class="bl-date"><time datetime="{a["date"]}">{date_longue(a["date"])}</time></span>'
            f'<h3>{a["titre"]}</h3><p>{a["extrait"]}</p><span class="bl-more">{T("Lire l'article")} {ARROW}</span></div></a>')


def blog_entete(src, slug, mots):
    """En-tête d'article : catégorie, titre, auteur, date, temps de lecture, partage."""
    a = next(x for x in load(src, "blog") if x["slug"] == slug)
    from urllib.parse import quote
    u, t = quote(f"{SITE}/{blog_url(a)}", safe=""), quote(a["titre"], safe="")
    partage = "".join(f'<a class="sh-{k}" href="{h.format(u=u, t=t)}"{"" if k == "mail" else " target=\"_blank\" rel=\"noopener\""} aria-label="{T(l)}">{svg}</a>'
                      for k, (l, h, svg) in SHARE.items())
    maj = f' · {T("mis à jour le {0}").format(date_longue(a["maj"]))}' if a.get("maj") and a["maj"] != a["date"] else ""
    return f'''<section class="ar-head">
  <div class="container"><div class="ar-col">
    <p class="bl-k">{T(a["categorie"])}{" · " + T(a["sous_categorie"]) if a.get("sous_categorie") else ""}</p>
    <h1>{a.get("h1", a["titre"])}</h1>
    <div class="ar-meta">
      <span>{BLOG_IC["auteur"]} <b>{a["auteur"]}</b></span>
      <span>{BLOG_IC["date"]} <time datetime="{a["date"]}">{date_longue(a["date"])}</time>{maj}</span>
      <span>{BLOG_IC["duree"]} {T("{0} min de lecture").format(max(1, round(mots / 220)))}</span>
    </div>
    <div class="ar-share" aria-label="{T("Partager cet article")}"><span>{T("Partager")}</span>{partage}</div>
  </div></div>
</section>'''


def blog_recents(src, slug):
    tous = [a for a in blog_articles(src) if a["slug"] != slug]
    cat = next((a["categorie"] for a in load(src, "blog") if a["slug"] == slug), None)
    meme = [a for a in tous if a["categorie"] == cat]
    autres = (meme + [a for a in tous if a not in meme])[:3]
    return (f'<section class="ar-latest"><div class="container"><h2>{T("Les derniers articles")}</h2><div class="bl-grid">'
            + "".join(blog_carte(a) for a in autres) + "</div></div></section>")


def blog_ld(a, mots):
    ld = {"@context": "https://schema.org", "@type": "BlogPosting", "headline": a["titre"],
          "description": a["description"], "datePublished": a["date"], "dateModified": a.get("maj", a["date"]),
          "inLanguage": HREFLANG[i18n.langue()], "wordCount": mots, "articleSection": T(a["categorie"]),
          "mainEntityOfPage": f"{SITE}/{blog_url(a)}",
          "author": ({"@type": "Person", "name": a["auteur_personne"]} if a.get("auteur_personne")
                     else {"@type": "Organization", "name": "Neur.on AI Solutions SA"}),
          "publisher": {"@type": "Organization", "name": "Neur.on AI Solutions SA", "url": SITE,
                        "logo": {"@type": "ImageObject", "url": f"{SITE}/assets/img/neuron-logo.png"}}}
    if a.get("image"):
        ld["image"] = f'{SITE}/{a["image"]["src"]}'
    if a.get("mentions"):
        ld["about"] = [{"@type": t, "name": n} for t, n in a["mentions"]]
    return '<script type="application/ld+json">' + json.dumps(ld, ensure_ascii=False) + "</script>"


def blog_hero():
    """Hero de la page Blog : chaque phrase passe par T()."""
    return f"""<section class="thero thero-read thero-centre">
  <div class="container">
    <div class="thero-grid">
      <div>
        <h1><em>{T("Blog.")}</em> {T("Ce qu'il faut savoir pour traduire le droit suisse")}</h1>
        <p class="lead">{T("Méthodes, analyses et retours de terrain sur la traduction juridique et financière en Suisse : terminologie des lois fédérales, achat de traduction, secret professionnel. Et les actualités de Neur.on depuis 2020. Les articles sont écrits par l'équipe juridique et linguistique de Neur.on.")}</p>
        <div class="thero-cta">
          <a href="{{{{ROOT}}}}fr/contact/" class="btn btn-blue">
            {T("Demander une démo")}
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"><path d="M5 12h14M13 5l7 7-7 7"/></svg>
          </a>
          <a href="#articles" class="btn btn-ghost">{T("Voir les articles")}</a>
        </div>
      </div>
      <div class="thero-promise">
        <span><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M4 19.5A2.5 2.5 0 0 1 6.5 17H20"/><path d="M6.5 2H20v20H6.5A2.5 2.5 0 0 1 4 19.5v-15A2.5 2.5 0 0 1 6.5 2z"/></svg><span><b>{T("Utile d'abord :")}</b> {T("terminologie, devis, secret professionnel, des réponses que l'on peut appliquer")}</span></span>
        <span><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="11" cy="11" r="7"/><path d="m20 20-3.5-3.5"/></svg><span><b>{T("Sources vérifiables :")}</b> {T("textes officiels suisses, ou observations datées dans l'application")}</span></span>
        <span><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 20h9M16.5 3.5a2.12 2.12 0 0 1 3 3L7 19l-4 1 1-4z"/></svg><span><b>{T("Signé par l'équipe :")}</b> {T("juristes et linguistes de Neur.on, en français, allemand, italien et anglais")}</span></span>
      </div>
    </div>
  </div>
</section>"""


def blog_fin():
    """Appel à l'action de fin de page Blog : chaque phrase passe par T()."""
    return f"""<section class="final-cta">
  <div class="container">
    <div class="final-cta-inner">
      <h2>{T("Ces sujets se voient mieux sur vos documents")}</h2>
      <p>{T("Une démo avec un spécialiste du droit suisse : terminologie, niveaux de relecture, modes de confidentialité, sur vos propres fichiers.")}</p>
      <div class="final-cta-btns">
        <a href="{{{{ROOT}}}}fr/contact/" class="btn btn-blue">
          {T("Demander une démo")}
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"><path d="M5 12h14M13 5l7 7-7 7"/></svg>
        </a>
        <a href="{{{{ROOT}}}}fr/corrext/" class="btn-outline">{T("Découvrir Corrext")}</a>
      </div>
      <p class="micro">{T("Démo sur mesure · en français, allemand, italien ou anglais · hébergement 100% suisse")}</p>
    </div>
  </div>
</section>"""


def gen_blog(src):
    """Blog : liste filtrable (article à la une, filtres, grille) et pages des articles générés."""
    arts = blog_articles(src)
    if not arts:
        return []
    pages = []
    for a in arts:
        if a.get("page") != "generee":
            continue
        corps = a["corps"]
        mots = len(re.sub(r"<[^>]+>", " ", corps).split())
        fig = ""
        if a.get("image"):
            i = a["image"]
            fig = (f'<figure class="ar-hero-img"><img src="{{{{ROOT}}}}{i["src"]}" alt="{i["alt"]}" width="{i["w"]}" height="{i["h"]}" fetchpriority="high">'
                   + (f'<figcaption>{i["legende"]}</figcaption>' if i.get("legende") else "") + "</figure>")
        body = "\n".join([
            blog_ld(a, mots),
            blog_entete(src, a["slug"], mots).replace("</div></div>\n</section>", f"{fig}</div></div>\n</section>", 1),
            f'''<section class="art">
  <div class="container">
    <div class="art-wrap">
      <div class="ar-brief"><b>{T("En bref")}</b><p>{a["bref"]}</p></div>
      {corps}
      {a_propos()}
    </div>
  </div>
</section>''',
            blog_recents(src, a["slug"]),
            cta(T("Voyez Corrext sur vos propres documents"),
                T("Une démonstration avec un spécialiste du droit suisse : terminologie, niveaux de relecture et modes de confidentialité, sur vos fichiers."),
                {"href": "fr/contact/", "txt": T("Demander une démo")}),
        ])
        pages.append((blog_url(a), {"title": a["title"], "description": a["description"], "short": a.get("court", a["titre"]),
                                    "nav": "ressources", "hero": "aide", "lastmod": a.get("maj", a["date"]),
                                    "image": a.get("image", {}).get("src"), "image_alt": a.get("image", {}).get("alt")}, body))

    une = arts[0]
    cats = []
    for a in arts:
        if a["categorie"] not in cats:
            cats.append(a["categorie"])
    n = lambda c: sum(1 for a in arts if a["categorie"] == c)
    filtres = (f'<button type="button" class="bl-chip" aria-pressed="true" data-f="">{T("Tous les articles")}</button>'
               + "".join(f'<button type="button" class="bl-chip" aria-pressed="false" data-f="{c}">{T(c)}<em>{n(c)}</em></button>' for c in cats if n(c)))
    une_html = f'''<section class="bl-feat" aria-label="{T("Article à la une")}">
  <div class="container">
    <a class="bl-feat-card" href="{{{{ROOT}}}}{blog_url(une)}">{blog_visuel(une, une=True)}
      <div class="bl-feat-body">
        <span class="bl-k">{T(une["categorie"])}</span>
        <h2>{une["titre"]}</h2>
        <p>{une["extrait"]}</p>
        <span class="feat-link">{T("Lire l'article")} {ARROW}</span>
        <div class="bl-meta"><span>{BLOG_IC["date"]} <time datetime="{une["date"]}">{date_longue(une["date"])}</time></span><span>{BLOG_IC["auteur"]} {une["auteur"]}</span></div>
      </div>
    </a>
  </div>
</section>'''
    script = """<script>(function(){var b=document.querySelectorAll('.bl-chip'),c=document.querySelectorAll('.bl-grid .bl-card'),v=document.querySelector('.bl-empty');
function f(x){b.forEach(function(e){e.setAttribute('aria-pressed',e.getAttribute('data-f')===x?'true':'false');});var k=0;c.forEach(function(e){var o=!x||e.getAttribute('data-cat')===x;e.hidden=!o;if(o)k++;});if(v)v.hidden=k>0;}
b.forEach(function(e){e.addEventListener('click',function(){f(e.getAttribute('data-f'));});});})();</script>"""
    liste = {"@context": "https://schema.org", "@type": "Blog", "name": T("Blog Neur.on"), "url": f"{SITE}/fr/ressources/blog/", "inLanguage": HREFLANG[i18n.langue()],
             "publisher": {"@type": "Organization", "name": "Neur.on AI Solutions SA"},
             "blogPost": [{"@type": "BlogPosting", "headline": a["titre"], "datePublished": a["date"], "url": f"{SITE}/{blog_url(a)}"} for a in arts]}
    body = "\n".join([
        '<script type="application/ld+json">' + json.dumps(liste, ensure_ascii=False) + "</script>",
        blog_hero(), une_html, blog_outils(),
        f'<section class="bl-filters" id="articles" aria-label="{T("Filtrer par catégorie")}"><div class="container">{filtres}</div></section>',
        f'<section class="bl-list"><div class="container"><div class="bl-grid">{"".join(blog_carte(a) for a in arts)}</div><p class="bl-empty" hidden>{T("Aucun article dans cette catégorie pour le moment.")}</p></div></section>',
        ('<section class="bl-actu"><div class="container"><a class="bl-actu-card" href="{{ROOT}}fr/ressources/blog/actualites/">'
         f'<span class="bl-k">{T("Actualités")}</span><b>{T("Toutes les brèves de Neur.on, année par année")}</b><span>{T("Prix, conférences, partenariats et presse depuis 2020.")} {ARROW}</span></a></div></section>')
        if load(src, "actualites") else "",
        blog_linkedin(), blog_fin(), script,
    ])
    pages.append(("fr/ressources/blog/", {"title": T("Blog Neur.on : droit suisse, traduction et actualités"),
                                           "description": T("Articles de fond sur la traduction juridique en Suisse (terminologie, devis, secret professionnel) et actualités de Neur.on : conférences, événements, presse."),
                                           "short": T("Blog"), "nav": "ressources", "hero": "read",
                                           "canonical": f"{SITE}/fr/ressources/blog/"}, body))
    return pages



def gen_actualites(src):
    """Actualités : toutes les brèves de Neur.on depuis 2020 sur une page, classées par année."""
    breves = load(src, "actualites")
    if not breves:
        return []
    # Les actualités devenues articles complets figurent aussi dans la frise : la page reprend tout l'ancien /news/
    articles = [{"num": a["slug"], "date": a["date"], "titre": a["titre"], "texte": f'<p>{a["extrait"]}</p>',
                 "categorie": a.get("sous_categorie", a["categorie"]), "article": blog_url(a), "image": a.get("vignette")}
                for a in load(src, "blog") if a["categorie"] == "Actualités"]
    data = sorted(breves + articles, key=lambda x: x["date"], reverse=True)
    annees = []
    for x in data:
        if x["date"][:4] not in annees:
            annees.append(x["date"][:4])
    def item(x):
        img = x.get("image")
        vis = (f'<img class="ac-img" src="{{{{ROOT}}}}{img["src"]}" alt="" width="{img["w"]}" height="{img["h"]}" loading="lazy" decoding="async">' if img else "")
        lien = x.get("lien_principal")
        if x.get("article"):
            titre = f'<a href="{{{{ROOT}}}}{x["article"]}">{x["titre"]}</a>'
            btn = f'<a class="ac-lien" href="{{{{ROOT}}}}{x["article"]}">{T("Lire l'article")} {ARROW}</a>'
        else:
            titre = x["titre"]
            btn = (f'<a class="ac-lien" href="{lien["url"]}" target="_blank" rel="noopener">{lien["libelle"]} {ARROW}</a>' if lien else "")
        return (f'<article class="ac-item{" ac-art" if x.get("article") else ""}" id="actu-{x["num"]}">{vis}<div class="ac-txt">'
                f'<p class="ac-meta"><time datetime="{x["date"]}">{date_longue(x["date"])}</time><span>{T(x["categorie"])}</span></p>'
                f'<h3>{titre}</h3><div class="ac-corps">{x["texte"]}</div>{btn}</div></article>')
    blocs = "".join(f'<section class="ac-annee" id="annee-{an}" aria-labelledby="t-{an}"><h2 id="t-{an}">{an}<em>{T("{0} actualités").format(sum(1 for x in data if x["date"][:4] == an))}</em></h2>'
                    + "".join(item(x) for x in data if x["date"][:4] == an) + "</section>" for an in annees)
    nav = "".join(f'<a class="bl-chip" href="#annee-{an}">{an}</a>' for an in annees)
    ld = {"@context": "https://schema.org", "@type": "CollectionPage", "name": T("Actualités de Neur.on"),
          "url": f"{SITE}/fr/ressources/blog/actualites/", "inLanguage": HREFLANG[i18n.langue()],
          "about": {"@type": "Organization", "name": "Neur.on AI Solutions SA"},
          "mainEntity": {"@type": "ItemList", "numberOfItems": len(data), "itemListElement": [
              {"@type": "ListItem", "position": i + 1, "item": {"@type": "NewsArticle", "headline": x["titre"], "datePublished": x["date"],
                                                               "url": f'{SITE}/{x["article"]}' if x.get("article") else f'{SITE}/fr/ressources/blog/actualites/#actu-{x["num"]}'}}
              for i, x in enumerate(data)]}}
    lead = T("Prix, conférences, partenariats, presse et recherche : {0} actualités, de la plus récente à la plus ancienne, "
             "dont {1} à lire en article complet dans le {2}.").format(
        len(data), len(articles), f'<a href="{{{{ROOT}}}}fr/ressources/blog/">{T("blog")}</a>')
    body = "\n".join([
        '<script type="application/ld+json">' + json.dumps(ld, ensure_ascii=False) + "</script>",
        f'''<section class="ar-head">
  <div class="container"><div class="ar-col">
    <p class="bl-k">{T("Actualités")}</p>
    <h1>{T("Toutes les actualités de Neur.on")}</h1>
    <p class="ac-lead">{lead}</p>
    <nav class="ac-nav" aria-label="{T("Aller à une année")}">{nav}</nav>
  </div></div>
</section>''',
        f'<section class="ac"><div class="container"><div class="ar-col">{blocs}</div></div></section>',
        cta(T("Voyez Corrext sur vos propres documents"),
            T("Une démonstration avec un spécialiste du droit suisse : terminologie, niveaux de relecture et modes de confidentialité, sur vos fichiers."),
            {"href": "fr/contact/", "txt": T("Demander une démo")}),
    ])
    return [("fr/ressources/blog/actualites/", {"title": T("Actualités de Neur.on depuis 2020 · Neur.on"),
                                                 "description": T("{0} actualités de Neur.on depuis {1} : prix et distinctions, conférences, partenariats, presse et recherche, classés par année.").format(len(data), annees[-1]),
                                                 "short": T("Actualités"), "nav": "ressources", "hero": "aide", "lastmod": data[0]["date"]}, body)]


def build_all(src):
    utiliser(src)
    pages = []
    pages += gen_solutions(src)
    pages += gen_domaines(src)
    pages += gen_paires(src)
    pages += gen_traduction_hub(src)
    pages += gen_glossaire(src)
    pages += gen_aide(src)
    pages += gen_blog(src)
    pages += gen_actualites(src)
    return pages

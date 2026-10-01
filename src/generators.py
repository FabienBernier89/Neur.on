"""Pages à l'échelle du site Neur.on : métiers, domaines, paires de langues, glossaire, aide.

Chaque famille lit ses données dans src/data/<famille>.json et rend un corps HTML qui réutilise
le socle CSS. build_all() renvoie une liste de (chemin logique, front-matter, corps).
Aucune donnée inventée : le contenu vient de PRODUCT.md, du carnet d'audit de l'application et
des textes de loi suisses publiés dans les langues officielles.
"""
import json, os, re

ARROW = ('<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" '
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


def load(src, name):
    p = os.path.join(src, "data", name + ".json")
    if not os.path.exists(p):
        return []
    with open(p, encoding="utf-8") as f:
        return json.load(f)


# ---------------------------------------------------------------- briques

_CARTES = None
SYMB = {"y": '<span class="cmp-y">✓</span> ', "p": '<span class="cmp-p">⚠</span> ', "n": '<span class="cmp-n">✕</span> '}


def carte(nom):
    """Carte de droite des heros (src/data/cartes.json) : fiche, terme en quatre langues, extrait de tableau ou code."""
    global _CARTES
    if _CARTES is None:
        _CARTES = json.load(open(os.path.join(os.path.dirname(__file__), "data", "cartes.json"), encoding="utf-8"))
    c = _CARTES[nom]
    tete = f'<div class="sh"><b>{c["titre"]}</b><span>{c["droite"]}</span></div>'
    pied = f'<div class="sf">{c["pied"]}</div>' if c.get("pied") else ""
    if c["type"] == "terme":
        corps = "".join(f'<div class="sr{" first" if i == 0 else ""}"><i>{lab}</i><b lang="{k}">{c["mots"][k]}</b></div>'
                        for i, (k, lab) in enumerate((("de", "Allemand"), ("fr", "Français"), ("it", "Italien"), ("en", "Anglais"))))
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


def hero(h1_lede, h1_rest, lead, nom_carte, ancre="#faits", ancre_txt="Voir le détail"):
    return f'''<section class="thero thero-carte">
  <div class="container">
    <div class="thero-grid">
      <div>
        <h1><em>{h1_lede}</em> {h1_rest}</h1>
        <p class="lead">{lead}</p>
        <div class="thero-cta">
          <a href="{{{{ROOT}}}}fr/contact/" class="btn btn-blue">Demander une démo {ARROW}</a>
          <a href="{ancre}" class="btn btn-ghost">{ancre_txt}</a>
        </div>
      </div>
      {carte(nom_carte)}
    </div>
  </div>
</section>'''


def hero_job(lede, rest, lead, promesses, titre_fiche, ancre="#faits", ancre_txt="Ce que Corrext change"):
    """Hero métier : le bleu nuit du produit, mais les repères forment une fiche de profil."""
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
          <a href="{{{{ROOT}}}}fr/contact/" class="btn btn-blue">Demander une démo {ARROW}</a>
          <a href="{ancre}" class="btn btn-ghost">{ancre_txt}</a>
        </div>
      </div>
      <div class="thero-promise"><span class="jh">{titre_fiche}</span>{ps}</div>
    </div>
  </div>
</section>'''


def hero_law(lede, rest, lead, spec, ancre="#faits", ancre_txt="Ce que Corrext apporte"):
    """Hero des pages de matière juridique : la terminologie tient lieu de visuel."""
    rows = "".join(
        f'<div class="sr{" first" if i == 0 else ""}"><i>{lab}</i><b>{spec["mots"][k]}</b></div>'
        for i, (k, lab) in enumerate((("de", "Allemand"), ("fr", "Français"),
                                      ("it", "Italien"), ("en", "Anglais"))))
    return f'''<section class="thero thero-law">
  <div class="container">
    <div class="thero-grid">
      <div>
        <h1><em>{lede}</em> {rest}</h1>
        <p class="lead">{lead}</p>
        <div class="thero-cta">
          <a href="{{{{ROOT}}}}fr/contact/" class="btn btn-blue">Demander une démo {ARROW}</a>
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


def hero_help(rubrique, titre, reponse, tags, ancre="#etapes", ancre_txt="Voir les étapes"):
    """Hero de documentation : la réponse d'abord, puis la fiche de l'article (outil, étapes, vérification)."""
    rows = "".join(f'<div class="sr{" first" if i == 0 else ""}"><i>{t["k"]}</i><b>{t["v"]}</b></div>'
                   for i, t in enumerate(tags))
    return f'''<section class="thero thero-help">
  <div class="container">
    <div class="thero-grid">
      <div>
        <h1><em>{rubrique}.</em> {titre}</h1>
        <p class="lead">{reponse}</p>
        <div class="thero-cta">
          <a href="{ancre}" class="btn btn-blue">{ancre_txt} {ARROW}</a>
          <a href="{{{{ROOT}}}}fr/contact/" class="btn btn-ghost">Demander une démo</a>
        </div>
      </div>
      <div class="law-spec"><div class="sh"><b>En bref</b><span>Centre d'aide</span></div>{rows}</div>
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
        '<div class="jv-opts"><div class="jv-opt on"><b>Internal review</b><span>par vos équipes</span></div>'
        '<div class="jv-opt"><b>Custom workflow</b><span>traducteur juridique</span></div></div>'),
    "outil-chnell": lambda: _win("CHnell",
        f'<div class="jv-search">{V_SEARCH}<b>Verzugszins</b><span>German → French</span></div>'
        '<div class="jv-res"><div lang="de">… den fehlenden Betrag zuzüglich <mark>Verzugszins</mark> nicht mehr nachbelasten …</div>'
        '<div lang="fr">… prélever le montant manquant avec l\'<mark>intérêt moratoire</mark> …</div></div>'
        f'<div class="jv-src">{V_BOOK}Feuille fédérale</div>'),
    # Même illustration que la page API : pas une documentation, le contrat d'interface fait foi.
    "outil-api": lambda: _win("API REST",
        '<div class="jv-code"><span class="m">POST</span> /v1/translate\n{\n'
        '  <span class="k">"source_language"</span>: "de",\n  <span class="k">"target_language"</span>: "fr",\n'
        '  <span class="k">"engine"</span>: "lexmachina",\n  <span class="k">"domain"</span>: "banking"\n}</div>'
        '<div class="jv-foot">Illustration · le contrat d\'interface est remis au cadrage</div>'),
    # Parcours auszug-hr.ch, données de démonstration de la page Extraits.
    "outil-extraits": lambda: _win("Commercial register extract",
        f'<div class="jv-search">{V_SEARCH}<b>Muster AG</b><span>CHE-000.000.000</span></div>'
        '<ul class="jv-list"><li><i></i>Corrext Certification</li><li><i></i>Notarized Certification</li>'
        '<li class="on"><i></i>Notarized &amp; Apostilled</li></ul>'),
    # Mode Highly sensitive : seul le moteur suisse reste sélectionnable, les autres sont grisés.
    "outil-lexmachina": lambda: _win("Translation engine",
        f'<div class="jv-chips"><span class="jv-chip dark">{V_LOCK}Highly sensitive</span></div>'
        '<ul class="jv-list"><li class="on"><i></i>LexMachina<span>Suisse</span></li>'
        '<li class="off"><i></i>DeepL Pro</li><li class="off"><i></i>Azure OpenAI GPT</li></ul>'),
}
OUTIL_VIS = {"fr/corrext/traduction-texte-et-document/": "outil-texte",
             "fr/corrext/gestion-de-projet/": "outil-projet", "fr/corrext/chnell/": "outil-chnell",
             "fr/corrext/api-on-premises/": "outil-api",
             "fr/corrext/extraits-registre-commerce/": "outil-extraits", "fr/lexmachina/": "outil-lexmachina"}


def outils_visuel(titre, items):
    ss = "".join(f'<a class="jv-tool" href="{{{{ROOT}}}}{s["href"]}">{VIGNETTES[OUTIL_VIS[s["href"]]]()}'
                 f'<b>{s["t"]}</b><span>{s["d"]}</span><em>Découvrir l\'outil {ARROW}</em></a>'
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


def who(titre, items):
    """Bloc « situations » en cartes : pictogramme facultatif (clé vis) sur la ligne du titre, puis le texte."""
    def ic(w):
        return f'<span class="ws-ic">{WS_ICONS[w["vis"]]}</span>' if w.get("vis") else ""
    ws = "".join(
        f'<article class="ws-item"><h3>{ic(w)}'
        f'<span><span class="pn">{w["a"]}.</span> {w["t"]}</span></h3><p>{w["p"]}</p></article>'
        for w in items)
    return ('<section class="who who-s">\n  <div class="container">\n'
            f'    <div class="sec-head"><h2>{titre}</h2></div>\n'
            f'    <div class="ws-grid">{ws}</div>\n  </div>\n</section>')


def voisins(titre, items, lien="Voir le domaine"):
    """Pages voisines en cartes : le terme phare dans deux langues (allemand et français par défaut), puis le nom et le résumé."""
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
        return ('<section class="temo temo-todo" aria-label="Emplacement du témoignage client à fournir">\n'
                '  <div class="container"><figure class="temo-fig">\n'
                '    <span class="temo-mark" aria-hidden="true">«</span>\n'
                '    <blockquote><p>Témoignage client à fournir : deux ou trois phrases d\'un associé ou d\'une '
                'associée sur un dossier concret traité avec Corrext, publiées avec son accord écrit.</p></blockquote>\n'
                '    <figcaption><b>Prénom Nom</b><span>Fonction, cabinet</span></figcaption>\n'
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
        <a href="{{{{ROOT}}}}fr/contact/" class="btn btn-blue">Demander une démo {ARROW}</a>
        {sec}
      </div>
      <p class="micro">Démo sur mesure · en français, allemand, italien ou anglais · hébergement 100% suisse</p>
    </div>
  </div>
</section>'''


def terms_table(termes, caption, titre="Les équivalences officielles, dans les quatre langues"):
    rows = "".join(
        f'<tr><td><b>{t["de"]}</b></td><td>{t["fr"]}</td><td>{t["it"]}</td><td>{t["en"]}</td>'
        f'<td class="ref">{t["ref"]}</td></tr>' for t in termes)
    return f'''<section class="tterms">
  <div class="container">
    <div class="sec-head"><h2>{titre}</h2>
      <p>{caption}</p></div>
    <div class="compare-wrap">
      <table class="cmp tterms-table">
        <thead><tr><th>Allemand</th><th>Français</th><th>Italien</th><th>Anglais</th><th>Référence</th></tr></thead>
        <tbody>{rows}</tbody>
      </table>
    </div>
    <p class="tterms-note">Équivalences tirées des textes officiels suisses, publiés en allemand,
      français et italien. Dans Corrext, chaque terme s'ouvre en contexte dans
      <a href="{{{{ROOT}}}}fr/corrext/chnell/">Fast lookup CHnell</a>, avec sa source.</p>
  </div>
</section>'''


TERMS_CSS = """<style>
.tterms{padding:84px 0;background:var(--bg);border-top:1px solid var(--line);border-bottom:1px solid var(--line)}
.tterms .sec-head{margin-bottom:34px}
.tterms-table{min-width:760px}
.tterms-table td{font-size:14px}
.tterms-table td b{color:var(--navy)}
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
.tlaw p{font-size:13.5px;color:var(--muted);line-height:1.55;margin-top:3px}
@media(max-width:940px){.tlaws-grid{grid-template-columns:1fr;gap:34px}.tlaws h2{max-width:none}.tlaws-lead{position:static}}
</style>"""


def laws_block(titre, intro, lois):
    ls = "".join(
        f'<div class="tlaw"><span class="ab">{l["abbr"]}</span><div><b>{l["nom"]}</b>'
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
                     "Ce métier, en trois points"),
            facts(d["facts_titre"], d["facts_intro"], d["facts_liens"], d["facts"]),
            who(d["who_titre"], d["who"]),
            gov(d["gov_q"], d["gov_p"], d["gov_lien"], d["gov_etapes"]),
            outils_visuel(d["outils_titre"], d["outils"]),
            temoignage(d.get("temoignage")),
            faq(d["faq_titre"], d["faq"]),
            cta(d["cta_t"], d["cta_p"], {"href": "fr/corrext/", "txt": "Voir la plateforme"}),
        ])
        pages.append((f'fr/solutions/{d["slug"]}/',
                      {"title": d["title"], "description": d["description"],
                       "short": d["short"], "nav": "solutions"}, body))
    if data:
        cards = "".join(
            f'<a href="{{{{ROOT}}}}fr/solutions/{d["slug"]}/"><b>{d["short"]}</b>'
            f'<span>{d["resume"]}</span>{ARROW}</a>' for d in data)
        body = "\n".join([
            hero("Solutions.", "Le même socle suisse, adapté à votre métier",
                 "Un cabinet d'avocats, une banque et une autorité cantonale ne traduisent ni les "
                 "mêmes documents, ni pour les mêmes raisons. Voici ce que Corrext change pour "
                 "chacun, avec les mêmes garanties de confidentialité.",
                 "solutions",
                 "#metiers", "Voir les six métiers"),
            f'''<section class="siblings" id="metiers" style="padding:84px 0">
  <div class="container"><h2>Par métier</h2>
    <div class="siblings-row solutions-row">{cards}</div></div>
</section>
<style>.solutions-row{{grid-template-columns:repeat(3,1fr)}}
@media(max-width:940px){{.solutions-row{{grid-template-columns:1fr}}}}</style>''',
            siblings("Explorer autrement", [
                {"href": "fr/traduction/", "t": "Par domaine du droit",
                 "d": "Douze domaines, leur terminologie et leurs textes de référence"},
                {"href": "fr/comparatif/", "t": "Par comparaison",
                 "d": "Corrext face à DeepL, aux LLM généralistes et à l'agence externe"},
                {"href": "fr/corrext/", "t": "Par outil",
                 "d": "Les quatre outils de la plateforme, démonstration à l'appui"}]),
            cta("Voyez Corrext sur les documents de votre métier",
                "Une démo personnalisée avec un expert qui connaît le droit suisse.",
                {"href": "fr/corrext/", "txt": "Voir la plateforme"}),
        ])
        pages.append(("fr/solutions/", {
            "title": "Solutions par métier · Neur.on, traduction juridique suisse",
            "description": "Cabinets d'avocats, banques, directions juridiques, autorités, "
                           "fiduciaires, éditeurs : ce que Corrext change pour chaque métier, "
                           "avec un stockage en Suisse et une relecture juridique à la carte.",
            "short": "Solutions", "nav": "solutions"}, body))
    return pages


def gen_domaines(src):
    pages, data = [], load(src, "domaines")
    for d in data:
        vois = [v for v in data if v["slug"] in d.get("voisins", [])][:3]
        t0 = d["termes"][0]
        spec = {"titre": "Terminologie officielle", "compte": f'{len(d["termes"])} termes',
                "mots": t0, "pied": f'{t0["ref"]} · vérifiable dans Fast lookup CHnell'}
        body = "\n".join([
            TERMS_CSS,
            hero_law(d["lede"], d["h1"], d["lead"], spec),
            facts(d.get("facts_titre", "Concrètement, dans Corrext"), d["definition"],
                  [{"href": "fr/corrext/traduction-texte-et-document/", "txt": "Traduire un document maintenant"},
                   {"href": "fr/corrext/gestion-de-projet/", "txt": "Commander une relecture juridique"}],
                  d["facts"]),
            terms_table(d["termes"], d["termes_note"], d.get("termes_titre", "La terminologie officielle, dans les quatre langues")),
            laws_block(d.get("lois_titre", "Les textes de référence, cités au quotidien"), d["lois_intro"], d["lois"]),
            who(d["who_titre"], d["who"]),
            faq(d["faq_titre"], d["faq"]),
            voisins("Autres domaines",
                    [{"href": f'fr/traduction/{v["slug"]}/', "t": v["short"], "d": v["resume"],
                      "terme": v["termes"][0]} for v in vois] or
                    [{"href": "fr/traduction/", "t": "Tous les domaines",
                      "d": "Les douze domaines couverts"}]),
            cta(d["cta_t"], d["cta_p"], {"href": "fr/traduction/", "txt": "Tous les domaines"}),
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
        spec = {"titre": "Un terme, quatre langues", "compte": f'{len(d["termes"])} termes',
                "mots": t0, "pied": f'{t0["ref"]} · publié dans les langues officielles'}
        body = "\n".join([
            TERMS_CSS,
            hero_law(d["lede"], d["h1"], d["lead"], spec, "#faits", "Ce qui change dans cette paire"),
            facts("Cette paire de langues, en pratique", d["definition"],
                  [{"href": "fr/corrext/traduction-texte-et-document/", "txt": "Essayer sur un extrait de loi"},
                   {"href": "fr/langues-et-formats/", "txt": "Toutes les langues et formats"}],
                  d["facts"]),
            terms_table(d["termes"], d["termes_note"]),
            who(d["who_titre"], d["who"]),
            faq(d["faq_titre"], d["faq"]),
            voisins("Autres paires de langues",
                    [{"href": f'fr/traduction/{v}/', "t": t, "d": r,
                      "terme": par_slug[v]["termes"][0] if v in par_slug else None,
                      "langues": tuple(LANGUES[x] for x in v.split("-"))}
                     for v, t, r in d["voisins"]], "Voir la paire"),
            cta(d["cta_t"], d["cta_p"], {"href": "fr/traduction/", "txt": "Traduction par domaine"}),
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
        hero("Traduction juridique et financière.", "Par domaine du droit et par paire de langues",
             "Le vocabulaire d'un prospectus de fonds n'est pas celui d'une sentence arbitrale, et "
             "l'allemand juridique suisse n'est pas l'allemand de Berlin. Chaque page ci-dessous "
             "donne la terminologie officielle, les textes de référence et la façon dont Corrext "
             "les traite.",
             "traduction",
             "#domaines", "Voir les domaines"),
        f'''<section class="siblings" id="domaines" style="padding:84px 0">
  <div class="container"><h2>Par domaine du droit et de la finance</h2>
    <div class="siblings-row grid3">{dcards}</div></div>
</section>''',
        f'''<section class="siblings" id="langues" style="padding:0 0 84px">
  <div class="container"><h2>Par paire de langues</h2>
    <div class="siblings-row grid3">{pcards}</div></div>
</section>
<style>.grid3{{grid-template-columns:repeat(3,1fr)}}
@media(max-width:940px){{.grid3{{grid-template-columns:1fr}}}}</style>''',
        cta("Votre domaine n'est pas dans la liste ?",
            "Corrext couvre 30 domaines dans son concordancier et 30 langues sur la plateforme. "
            "Dites-nous ce que vous traduisez.",
            {"href": "fr/corrext/chnell/", "txt": "Voir Fast lookup CHnell"}),
    ])
    return [("fr/traduction/", {
        "title": "Traduction juridique par domaine et par langue · Neur.on",
        "description": "Douze domaines du droit suisse et les principales paires de langues : "
                       "terminologie officielle en allemand, français, italien et anglais, textes "
                       "de référence et traitement dans Corrext.",
        "short": "Traduction", "nav": "solutions"}, body)]


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
.gnote{background:var(--bg);border:1px solid var(--line);border-radius:14px;padding:26px 28px}
.gnote p{font-size:14.5px;color:var(--text);line-height:1.65;margin-bottom:16px}
.glang{display:grid;grid-template-columns:96px 1fr;gap:14px;padding:13px 0;border-bottom:1px solid var(--line);align-items:baseline}
.glang i{font-style:normal;font-size:12px;font-weight:700;color:var(--muted);letter-spacing:.06em;text-transform:uppercase}
.glang b{font-size:16px;color:var(--ink)}
.gex{padding:0 0 84px}
.gex-box{background:var(--bg);border:1px solid var(--line);border-radius:18px;padding:32px 34px}
.gex-box h2{font-size:22px;margin-bottom:18px}
.gex-row{display:grid;grid-template-columns:1fr 1fr;gap:28px}
.gex-row div p{font-size:14.5px;line-height:1.6;color:var(--text)}
.gex-row div i{font-style:normal;display:block;font-size:12px;font-weight:700;color:var(--muted);text-transform:uppercase;letter-spacing:.06em;margin-bottom:7px}
.gex-row mark{background:#fff2a8;padding:0 2px}
.gsrc{margin-top:18px;font-size:13px;color:var(--muted)}
@media(max-width:940px){.gterm-grid,.gex-row{grid-template-columns:1fr;gap:28px}}
</style>"""
    for d in data:
        vois = [v for v in data if v["slug"] in d.get("voisins", [])][:3]
        body_hero = hero_law(
            d["de"], "· " + d["fr"], d["lead"],
            {"titre": "Le terme, quatre langues", "compte": d["domaine"],
             "mots": {k: d[k] for k in ("de", "fr", "it", "en")},
             "pied": f'{d["base"]} · source : {d["source"]}'},
            "#definition", "Lire la définition")
        body = "\n".join([css, body_hero,
            f'''<section class="gterm" id="definition">
  <div class="container">
    <div class="gterm-grid">
      <div>
        <h2>Définition</h2>
        <p class="gdef">{d["definition"]}</p>
        <div class="gmeta"><span>{d["domaine"]}</span><span>{d["base"]}</span></div>
      </div>
      <div class="gnote">
        <p>Les lois fédérales suisses sont publiées en allemand, en français et en italien, et les
          trois versions font foi. L'équivalence ci-contre n'est donc pas une traduction d'usage :
          c'est le terme employé par le texte officiel lui-même.</p>
        <a class="feat-link" href="{{{{ROOT}}}}fr/ressources/glossaire/">Tout le glossaire {ARROW}</a>
      </div>
    </div>
  </div>
</section>''',
            f'''<section class="gex">
  <div class="container">
    <div class="gex-box">
      <h2>Le terme dans un texte officiel</h2>
      <div class="gex-row">
        <div><i>Allemand</i><p>{d["exemple"]["de"]}</p></div>
        <div><i>Français</i><p>{d["exemple"]["fr"]}</p></div>
      </div>
      <p class="gsrc">Source : {d["source"]}. Dans Corrext, ce segment et ceux qui l'entourent
        s'affichent dans <a href="{{{{ROOT}}}}fr/corrext/chnell/">Fast lookup CHnell</a>,
        chacun avec sa référence.</p>
    </div>
  </div>
</section>''',
            siblings("Termes voisins",
                     [{"href": f'fr/ressources/glossaire/{v["slug"]}/',
                       "t": f'{v["de"]} · {v["fr"]}', "d": v["resume"]} for v in vois] or
                     [{"href": "fr/ressources/glossaire/", "t": "Tout le glossaire",
                       "d": "La terminologie juridique suisse en quatre langues"}]),
            cta("Cette terminologie, appliquée à vos documents",
                "Corrext vérifie chaque terme dans son contexte officiel et garde vos choix "
                "cohérents d'un document à l'autre.",
                {"href": "fr/corrext/chnell/", "txt": "Découvrir CHnell"}),
        ])
        pages.append((f'fr/ressources/glossaire/{d["slug"]}/', {
            "title": d["title"], "description": d["description"],
            "short": f'{d["de"]} · {d["fr"]}', "nav": "ressources", "hero": "law"}, body))

    # index du glossaire
    rows = "".join(
        f'<a href="{{{{ROOT}}}}fr/ressources/glossaire/{d["slug"]}/" class="grow2">'
        f'<b>{d["de"]}</b><span class="fr">{d["fr"]}</span>'
        f'<span class="it">{d["it"]}</span><span class="dom">{d["domaine"]}</span></a>'
        for d in sorted(data, key=lambda x: x["de"].lower()))
    body = "\n".join([
        """<style>
.glist{padding:84px 0}
.glist-head{margin-bottom:28px}
.grow2{display:grid;grid-template-columns:1.1fr 1.1fr 1.1fr auto;gap:18px;align-items:baseline;padding:15px 12px;margin:0 -12px;border-bottom:1px solid var(--line);transition:background .15s}
.grow2:first-of-type{border-top:1px solid var(--line)}
.grow2:hover{background:rgba(49,123,255,.04)}
.grow2 b{font-size:15.5px;color:var(--navy)}
.grow2 .fr{font-size:14.5px;color:var(--ink)}
.grow2 .it{font-size:14px;color:var(--muted)}
.grow2 .dom{font-size:11.5px;font-weight:700;color:var(--blue-d);background:var(--tint);border-radius:50px;padding:4px 11px;white-space:nowrap}
@media(max-width:940px){.grow2{grid-template-columns:1fr 1fr;gap:6px 14px}.grow2 .dom{grid-column:1 / -1;justify-self:start}}
</style>""",
        hero("Glossaire juridique suisse.", "Chaque terme dans les quatre langues, avec sa source",
             "Les lois suisses sont publiées en allemand, en français et en italien : les "
             "équivalences ci-dessous ne sont pas des traductions d'usage, ce sont les termes des "
             "textes officiels. Chacun renvoie à son article et à sa source.",
             "glossaire",
             "#liste", "Voir les termes"),
        f'''<section class="glist" id="liste">
  <div class="container">
    <div class="sec-head glist-head"><h2>Les termes</h2>
      <p>Classés par terme allemand. Le glossaire s'étoffe au fil des vérifications de nos
        juristes-linguistes.</p></div>
    {rows}
  </div>
</section>''',
        cta("Votre terminologie, appliquée partout",
            "CHnell couvre 30 domaines et vos propres ressources s'y ajoutent.",
            {"href": "fr/corrext/chnell/", "txt": "Découvrir CHnell"}),
    ])
    pages.append(("fr/ressources/glossaire/", {
        "title": "Glossaire juridique suisse en quatre langues · Neur.on",
        "description": "La terminologie du droit suisse dans les quatre langues, avec la base "
                       "légale et la source officielle de chaque terme. Vérifiable en contexte "
                       "dans le concordancier CHnell de Corrext.",
        "short": "Glossaire", "nav": "ressources"}, body))
    return pages


def gen_aide(src):
    """Centre d'aide : accueil avec recherche, deux espaces (utilisateurs, administrateurs),
    une page par rubrique avec ses questions en accordéon (ancre par question)."""
    data = load(src, "aide")
    if not data:
        return []
    ESPACES = (("utilisateur", "Utiliser Corrext", "Traduire, faire relire, vérifier un terme : les gestes du quotidien dans l'application."),
               ("admin", "Administrer Corrext", "Pour les administrateurs : membres et rôles, politique de moteurs, mémoires et terminologie de l'organisation."))
    plat = lambda h: re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", h)).strip()

    def reponse(x):
        h = f'<p>{x["reponse"]}</p>'
        if x["etapes"]:
            h += '<ol class="hc-steps">' + "".join(f"<li>{e}</li>" for e in x["etapes"]) + "</ol>"
        if x.get("savoir"):
            h += '<div class="hc-know"><b>À savoir</b><ul>' + "".join(f"<li>{s}</li>" for s in x["savoir"]) + "</ul></div>"
        return h

    index = [{"q": x["question"], "t": plat(" ".join([x["reponse"]] + x["etapes"] + x.get("savoir", []))),
              "r": r["titre"], "e": "Administrateurs" if r["espace"] == "admin" else "Utilisateurs",
              "u": f'{{{{ROOT}}}}fr/aide/{r["slug"]}/#{x["slug"]}'} for r in data for x in r["articles"]]
    recherche = lambda grande: f'''<form class="hc-search{" big" if grande else ""}" action="{{{{ROOT}}}}fr/aide/" role="search">
  <label class="sr-only" for="hc-q">Rechercher dans le centre d'aide</label>
  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" aria-hidden="true"><circle cx="11" cy="11" r="7"/><path d="m20 20-3.5-3.5"/></svg>
  <input id="hc-q" name="q" type="search" autocomplete="off" placeholder="Rechercher une question (ex : traduire un fichier, devis, ajouter un membre)">
  {'<div class="hc-results" id="hc-results" role="listbox" hidden></div>' if grande else ''}
</form>'''
    side = lambda courant: '<nav class="hc-side" aria-label="Rubriques du centre d\'aide">' + "".join(
        f'<p class="hc-side-t">{titre}</p><ul>' + "".join(
            f'<li><a href="{{{{ROOT}}}}fr/aide/{r["slug"]}/"{" aria-current=\"page\"" if r["slug"] == courant else ""}>'
            f'<span class="ws-ic">{WS_ICONS[r["icone"]]}</span>{r["titre"]}</a></li>' for r in data if r["espace"] == esp) + "</ul>"
        for esp, titre, _ in ESPACES) + "</nav>"
    contact = cta("Vous ne trouvez pas votre réponse ?",
                  "Notre équipe vous répond en français, allemand, italien et anglais, à team@corrext.com, et vous accompagne dans la prise en main de Corrext.",
                  {"href": "fr/contact/", "txt": "Contacter l'équipe"})
    script_ancre = """<script>(function(){function o(){var h=decodeURIComponent(location.hash.slice(1));if(!h)return;var d=document.getElementById(h);if(d&&d.tagName==='DETAILS'){d.open=true;d.scrollIntoView({block:'start'});}}window.addEventListener('hashchange',o);o();})();</script>"""

    pages = []
    for r in data:
        n = len(r["articles"])
        qs = "".join(f'<details class="faq-item hc-q" id="{x["slug"]}"><summary>{x["question"].replace(" ?", "\u00a0?")}</summary><div class="hc-a">{reponse(x)}</div></details>'
                     for x in r["articles"])
        ld = {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
            {"@type": "Question", "name": x["question"], "acceptedAnswer": {"@type": "Answer", "text": plat(reponse(x))}} for x in r["articles"]]}
        espace = "Administrateurs" if r["espace"] == "admin" else "Utilisateurs"
        body = "\n".join([
            '<script type="application/ld+json">' + json.dumps(ld, ensure_ascii=False) + "</script>",
            hero_help(r["titre"], r["h1"], r["lead"],
                      [{"k": "Espace", "v": espace}, {"k": "Questions", "v": str(n)},
                       {"k": "Outil", "v": r["outil"]}, {"k": "Vérifié", "v": "septembre 2026"}],
                      "#questions", "Voir les questions"),
            f'''<section class="hc" id="questions">
  <div class="container">
    <div class="hc-grid">
      {side(r["slug"])}
      <div class="hc-main">
        {recherche(False)}
        <p class="hc-kicker">{espace} · {n} questions</p>
        <h2 class="hc-h2">{r["titre"]}</h2>
        <div class="faq-list hc-list">{qs}</div>
      </div>
    </div>
  </div>
</section>''',
            contact, script_ancre,
        ])
        pages.append((f'fr/aide/{r["slug"]}/', {"title": r["title"], "description": r["description"],
                                                 "short": r["titre"], "nav": "ressources", "hero": "help"}, body))

    total = sum(len(r["articles"]) for r in data)
    blocs = "".join(
        f'''<section class="hc-space{" admin" if esp == "admin" else ""}" id="{esp}">
  <div class="container">
    <div class="hc-space-head"><span class="hc-badge">{"Administrateurs" if esp == "admin" else "Utilisateurs"}</span><h2>{titre}</h2><p>{texte}</p></div>
    <div class="hc-cards">''' + "".join(
            f'<a class="hc-card" href="{{{{ROOT}}}}fr/aide/{r["slug"]}/"><span class="ws-ic">{WS_ICONS[r["icone"]]}</span>'
            f'<b>{r["titre"]}</b><span class="d">{r["lead"]}</span><em>{len(r["articles"])} questions {ARROW}</em></a>'
            for r in data if r["espace"] == esp) + '''</div>
  </div>
</section>''' for esp, titre, texte in ESPACES)
    tags = "".join(f'<a href="{{{{ROOT}}}}fr/aide/{u}">{t}</a>' for t, u in (
        ("Traduire des fichiers", "traduction-texte-et-document/#traduire-des-fichiers"), ("Mode Highly sensitive", "premiers-pas/#mode-highly-sensitive"),
        ("Obtenir un devis", "gestion-de-projet/#devis-et-delai"), ("Ajouter un membre", "admin-organisation/#ajouter-un-membre")))
    moteur = """<script>(function(){var I=window.HC_INDEX||[],f=document.querySelector('.hc-search.big'),q=document.getElementById('hc-q'),box=document.getElementById('hc-results');if(!f||!q||!box)return;
function n(s){return (s||'').toLowerCase().normalize('NFD').replace(/[\\u0300-\\u036f]/g,'').replace(/[^a-z0-9' ]+/g,' ');}
var V=I.map(function(x){return {x:x,q:n(x.q),t:n(x.t),r:n(x.r)};});
function esc(s){return s.replace(/[&<>"]/g,function(c){return {'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c];});}
function cherche(v){var m=n(v).split(' ').filter(function(w){return w.length>1;});if(!m.length){box.hidden=true;box.innerHTML='';return [];}
var r=V.map(function(o){var s=0;m.forEach(function(w){if(o.q.indexOf(w)>-1)s+=4;if(o.r.indexOf(w)>-1)s+=2;if(o.t.indexOf(w)>-1)s+=1;});return {o:o,s:s};}).filter(function(a){return a.s>0;}).sort(function(a,b){return b.s-a.s;}).slice(0,8);
box.innerHTML=r.length?r.map(function(a){return '<a role="option" href="'+a.o.x.u+'"><b>'+esc(a.o.x.q)+'</b><span>'+esc(a.o.x.e)+' · '+esc(a.o.x.r)+'</span></a>';}).join(''):'<p class="none">Aucune réponse pour « '+esc(v)+' ». Essayez un autre mot, ou contactez l\\'équipe.</p>';box.hidden=false;return r;}
q.addEventListener('input',function(){cherche(q.value);});
f.addEventListener('submit',function(e){e.preventDefault();var r=cherche(q.value);if(r.length)location.href=r[0].o.x.u;});
var p=new URLSearchParams(location.search).get('q');if(p){q.value=p;cherche(p);}})();</script>"""
    body = "\n".join([
        f'''<section class="thero thero-help thero-hc">
  <div class="container">
    <div class="thero-grid">
      <div>
        <p class="hc-kicker">Centre d'aide Corrext</p>
        <h1>Comment pouvons-nous vous aider ?</h1>
        <p class="lead">{total} réponses vérifiées dans l'application, de votre première traduction à l'administration de votre organisation.</p>
        {recherche(True)}
        <div class="hc-tags"><span>Recherches fréquentes :</span>{tags}</div>
        <div class="hc-spaces"><a href="#utilisateur">Je l'utilise</a><a href="#admin">Je l'administre</a></div>
      </div>
    </div>
  </div>
</section>''',
        blocs, contact,
        "<script>window.HC_INDEX=" + json.dumps(index, ensure_ascii=False).replace("</", "<\\/") + ";</script>", moteur,
    ])
    pages.append(("fr/aide/", {"hero": "help", "title": "Centre d'aide Corrext · Neur.on",
                               "description": f"{total} réponses sur Corrext, vérifiées dans l'application : traduire, faire relire, vérifier un terme, sécurité, et administration de votre organisation.",
                               "short": "Centre d'aide", "nav": "ressources"}, body))
    return pages


def build_all(src):
    pages = []
    pages += gen_solutions(src)
    pages += gen_domaines(src)
    pages += gen_paires(src)
    pages += gen_traduction_hub(src)
    pages += gen_glossaire(src)
    pages += gen_aide(src)
    return pages

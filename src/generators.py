"""Pages à l'échelle du site Neur.on : métiers, domaines, paires de langues, glossaire, aide.

Chaque famille lit ses données dans src/data/<famille>.json et rend un corps HTML qui réutilise
le socle CSS. build_all() renvoie une liste de (chemin logique, front-matter, corps).
Aucune donnée inventée : le contenu vient de PRODUCT.md, du carnet d'audit de l'application et
des textes de loi suisses publiés dans les langues officielles.
"""
import json, os

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

def hero(h1_lede, h1_rest, lead, promesses, ancre="#faits", ancre_txt="Voir le détail"):
    ps = "".join(
        f'<span>{ICONS[i % 3]}<span><b>{p["t"]} :</b> {p["d"]}</span></span>'
        for i, p in enumerate(promesses))
    return f'''<section class="thero">
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
      <div class="thero-promise">{ps}</div>
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


def hero_help(rubrique, titre, reponse, tags):
    """Hero de documentation : la réponse d'abord, la promesse nulle part."""
    ts = "".join(f'<span><b>{t["k"]} :</b> {t["v"]}</span>' for t in tags)
    return f'''<section class="thero thero-help">
  <div class="container">
    <div class="thero-grid">
      <div>
        <h1><em>{rubrique}.</em> {titre}</h1>
        <p class="lead">{reponse}</p>
      </div>
      <div class="htags">{ts}</div>
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


def who(titre, items):
    ws = "".join(f'<div class="who-item"><h3><span class="pn">{w["a"]}.</span> {w["t"]}</h3>'
                 f'<p>{w["p"]}</p></div>' for w in items)
    return f'''<section class="who">
  <div class="container">
    <div class="sec-head"><h2>{titre}</h2></div>
    <div class="who-grid">{ws}</div>
  </div>
</section>'''


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


def terms_table(termes, caption):
    rows = "".join(
        f'<tr><td><b>{t["de"]}</b></td><td>{t["fr"]}</td><td>{t["it"]}</td><td>{t["en"]}</td>'
        f'<td class="ref">{t["ref"]}</td></tr>' for t in termes)
    return f'''<section class="tterms">
  <div class="container">
    <div class="sec-head"><h2>La terminologie de ce domaine, dans les quatre langues</h2>
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
.tterms-note{margin-top:16px;font-size:13.5px;color:var(--muted);max-width:70ch}
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
            hero(d["lede"], d["h1"], d["lead"], d["promesses"], "#faits", "Ce que Corrext change"),
            facts(d["facts_titre"], d["facts_intro"], d["facts_liens"], d["facts"]),
            who(d["who_titre"], d["who"]),
            gov(d["gov_q"], d["gov_p"], d["gov_lien"], d["gov_etapes"]),
            siblings("Les outils que ce métier utilise le plus", d["outils"]),
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
                 [{"t": "Six métiers", "d": "des usages documentés, pas des promesses génériques"},
                  {"t": "Un socle commun", "d": "stockage en Suisse, moteurs au choix, relecture à la carte"},
                  {"t": "Treize domaines", "d": "du contrat au droit administratif, avec la terminologie officielle"}],
                 "#metiers", "Voir les six métiers"),
            f'''<section class="siblings" id="metiers" style="padding:84px 0">
  <div class="container"><h2>Par métier</h2>
    <div class="siblings-row solutions-row">{cards}</div></div>
</section>
<style>.solutions-row{{grid-template-columns:repeat(3,1fr)}}
.solutions-row a{{border-bottom:1px solid var(--line)}}
.solutions-row a:nth-child(3n){{border-right:0}}
.solutions-row a:nth-last-child(-n+3){{border-bottom:0}}
@media(max-width:940px){{.solutions-row{{grid-template-columns:1fr}}}}</style>''',
            siblings("Explorer autrement", [
                {"href": "fr/traduction/", "t": "Par domaine du droit",
                 "d": "Treize domaines, leur terminologie et leurs textes de référence"},
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
            facts("Traduire ce domaine, concrètement", d["definition"],
                  [{"href": "fr/corrext/fast-translation/", "txt": "Traduire un document maintenant"},
                   {"href": "fr/corrext/translation-project/", "txt": "Commander une relecture juridique"}],
                  d["facts"]),
            terms_table(d["termes"], d["termes_note"]),
            laws_block("Les textes que ce domaine cite tous les jours", d["lois_intro"], d["lois"]),
            who(d["who_titre"], d["who"]),
            faq(d["faq_titre"], d["faq"]),
            siblings("Domaines voisins",
                     [{"href": f'fr/traduction/{v["slug"]}/', "t": v["short"], "d": v["resume"]}
                      for v in vois] or
                     [{"href": "fr/traduction/", "t": "Tous les domaines",
                       "d": "Les treize domaines couverts"}]),
            cta(d["cta_t"], d["cta_p"], {"href": "fr/traduction/", "txt": "Tous les domaines"}),
        ])
        pages.append((f'fr/traduction/{d["slug"]}/',
                      {"title": d["title"], "description": d["description"],
                       "short": d["short"], "nav": "solutions", "hero": "law"}, body))
    return pages


def gen_paires(src):
    pages, data = [], load(src, "paires")
    for d in data:
        t0 = d["termes"][0]
        spec = {"titre": "Un terme, quatre langues", "compte": f'{len(d["termes"])} termes',
                "mots": t0, "pied": f'{t0["ref"]} · publié dans les langues officielles'}
        body = "\n".join([
            TERMS_CSS,
            hero_law(d["lede"], d["h1"], d["lead"], spec, "#faits", "Ce qui change dans cette paire"),
            facts("Cette paire de langues, en pratique", d["definition"],
                  [{"href": "fr/corrext/fast-translation/", "txt": "Essayer sur un extrait de loi"},
                   {"href": "fr/langues-et-formats/", "txt": "Toutes les langues et formats"}],
                  d["facts"]),
            terms_table(d["termes"], d["termes_note"]),
            who(d["who_titre"], d["who"]),
            faq(d["faq_titre"], d["faq"]),
            siblings("Autres paires de langues",
                     [{"href": f'fr/traduction/{v}/', "t": t, "d": r}
                      for v, t, r in d["voisins"]]),
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
             [{"t": "Treize domaines", "d": "du contrat au droit administratif, terminologie à l'appui"},
              {"t": "Sources officielles", "d": "Fedlex, Feuille fédérale, FINMA, jurisprudence du Tribunal fédéral"},
              {"t": "Quatre langues natives", "d": "allemand, français, italien et anglais avec Neur.on LLM"}],
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
.grid3 a{{border-bottom:1px solid var(--line)}}
.grid3 a:nth-child(3n){{border-right:0}}
@media(max-width:940px){{.grid3{{grid-template-columns:1fr}}.grid3 a{{border-right:0}}}}</style>''',
        cta("Votre domaine n'est pas dans la liste ?",
            "Corrext couvre 26 domaines dans son concordancier et 30 langues sur la plateforme. "
            "Dites-nous ce que vous traduisez.",
            {"href": "fr/corrext/chnell/", "txt": "Voir Fast lookup CHnell"}),
    ])
    return [("fr/traduction/", {
        "title": "Traduction juridique par domaine et par langue · Neur.on",
        "description": "Treize domaines du droit suisse et les principales paires de langues : "
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
             [{"t": "Quatre langues", "d": "allemand, français, italien et anglais pour chaque terme"},
              {"t": "Sources officielles", "d": "Fedlex, Feuille fédérale, administrations fédérales"},
              {"t": "Vérifiable", "d": "chaque terme s'ouvre en contexte dans Fast lookup CHnell"}],
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
            "CHnell couvre 26 domaines et vos propres ressources s'y ajoutent.",
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
    pages, data = [], load(src, "aide")
    if not data:
        return []
    css = """<style>
.hsteps{padding:70px 0}
.hsteps-grid{display:grid;grid-template-columns:1fr 1.2fr;gap:56px;align-items:start}
.hsteps-grid > div:first-child{position:sticky;top:96px;align-self:start}
.hanswer{font-size:18px;line-height:1.6;color:var(--ink);max-width:52ch}
.hol{counter-reset:s;border-top:1px solid var(--line)}
.hol li{counter-increment:s;list-style:none;display:grid;grid-template-columns:30px 1fr;gap:16px;padding:16px 0;border-bottom:1px solid var(--line);font-size:15px;line-height:1.6;color:var(--text)}
.hol li > span{display:block}
.hol li::before{content:counter(s);display:flex;align-items:center;justify-content:center;width:26px;height:26px;border-radius:50%;background:var(--navy);color:#fff;font-size:12.5px;font-weight:800}
.hol li b{color:var(--ink)}
.hnote{padding:0 0 84px}
.hnote-box{background:var(--tint);border:1px solid var(--line);border-radius:18px;padding:30px 32px}
.hnote-box h2{font-size:20px;margin-bottom:14px}
.hnote-box ul{list-style:none}
.hnote-box li{display:grid;grid-template-columns:auto 1fr;gap:12px;padding:9px 0;font-size:14.5px;line-height:1.55;color:var(--text)}
.hnote-box li svg{width:17px;height:17px;color:var(--blue-d);margin-top:3px}
@media(max-width:940px){.hsteps-grid{grid-template-columns:1fr;gap:30px}.hsteps-grid > div:first-child{position:static}}
</style>"""
    for rub in data:
        for art in rub["articles"]:
            steps = "".join(f"<li><span>{e}</span></li>" for e in art["etapes"])
            notes = "".join(
                f'<li>{ICONS[i % 3]}<span>{n}</span></li>' for i, n in enumerate(art.get("savoir", [])))
            ld = {"@context": "https://schema.org", "@type": "HowTo", "name": art["titre"],
                  "description": art["reponse"],
                  "step": [{"@type": "HowToStep", "position": i + 1,
                            "text": s.replace("<b>", "").replace("</b>", "")}
                           for i, s in enumerate(art["etapes"])]}
            autres = [a for a in rub["articles"] if a["slug"] != art["slug"]][:3]
            body = "\n".join([css,
                '<script type="application/ld+json">' + json.dumps(ld, ensure_ascii=False) + "</script>",
                hero_help(rub["titre"], art["titre"], art["reponse"],
                          [{"k": "Outil", "v": rub["outil"]},
                           {"k": "Étapes", "v": str(len(art["etapes"]))},
                           {"k": "Vérifié", "v": "septembre 2026"}]),
                f'''<section class="hsteps">
  <div class="container">
    <div class="hsteps-grid">
      <div><h2>Les étapes</h2>
        <p class="hanswer">{len(art["etapes"])} étapes dans l'application. Les libellés entre
          guillemets sont ceux affichés par Corrext, en anglais.</p>
        <a class="feat-link" href="{{{{ROOT}}}}fr/aide/{rub["slug"]}/">Tous les articles
          « {rub["titre"]} » {ARROW}</a></div>
      <div><ol class="hol">{steps}</ol></div>
    </div>
  </div>
</section>''',
                (f'''<section class="hnote">
  <div class="container"><div class="hnote-box"><h2>À savoir</h2><ul>{notes}</ul></div></div>
</section>''' if notes else ""),
                siblings("Autres articles de cette rubrique",
                         [{"href": f'fr/aide/{rub["slug"]}/{a["slug"]}/', "t": a["titre"],
                           "d": a["reponse"][:96] + "…"} for a in autres] or
                         [{"href": "fr/aide/", "t": "Centre d'aide", "d": "Toutes les rubriques"}]),
                cta("Une question que cet article ne couvre pas ?",
                    "Nos spécialistes répondent en français, allemand, italien et anglais.",
                    {"href": "fr/aide/", "txt": "Parcourir le centre d'aide"}),
            ])
            pages.append((f'fr/aide/{rub["slug"]}/{art["slug"]}/', {
                "title": art["title"], "description": art["description"],
                "short": art["titre"], "nav": "ressources", "hero": "help"}, body))

        # index de rubrique
        cards = "".join(
            f'<a href="{{{{ROOT}}}}fr/aide/{rub["slug"]}/{a["slug"]}/"><b>{a["titre"]}</b>'
            f'<span>{a["reponse"][:110]}…</span>{ARROW}</a>' for a in rub["articles"])
        body = "\n".join([
            hero_help(rub["titre"], rub["h1"], rub["lead"],
                      [{"k": "Outil", "v": rub["outil"]},
                       {"k": "Articles", "v": str(len(rub["articles"]))},
                       {"k": "Vérifié", "v": "septembre 2026"}]),
            f'''<section class="siblings" id="articles" style="padding:84px 0">
  <div class="container"><h2>Les articles de cette rubrique</h2>
    <div class="siblings-row grid2">{cards}</div></div>
</section>
<style>.grid2{{grid-template-columns:repeat(2,1fr)}}
.grid2 a{{border-bottom:1px solid var(--line)}}
.grid2 a:nth-child(2n){{border-right:0}}
@media(max-width:940px){{.grid2{{grid-template-columns:1fr}}.grid2 a{{border-right:0}}}}</style>''',
            cta("Besoin d'un accompagnement ?",
                "Une démo personnalisée vaut souvent mieux qu'une page d'aide.",
                {"href": "fr/aide/", "txt": "Centre d'aide"}),
        ])
        pages.append((f'fr/aide/{rub["slug"]}/', {
            "title": rub["title"], "description": rub["description"],
            "short": rub["titre"], "nav": "ressources", "hero": "help"}, body))

    # index général du centre d'aide
    blocks = "".join(
        f'<a href="{{{{ROOT}}}}fr/aide/{r["slug"]}/"><b>{r["titre"]}</b>'
        f'<span>{r["lead"][:110]}…</span>{ARROW}</a>' for r in data)
    total = sum(len(r["articles"]) for r in data)
    body = "\n".join([
        hero_help("Centre d'aide Corrext", "Comment faire, étape par étape",
                  f"{total} articles tirés de l'application telle qu'elle fonctionne, sans jargon et "
                  "sans promesse. Chaque procédure a été vérifiée dans Corrext en septembre 2026.",
                  [{"k": "Rubriques", "v": str(len(data))},
                   {"k": "Articles", "v": str(total)},
                   {"k": "Vérifié", "v": "septembre 2026"}]),
        f'''<section class="siblings" id="rubriques" style="padding:84px 0">
  <div class="container"><h2>Les rubriques</h2>
    <div class="siblings-row grid2">{blocks}</div></div>
</section>
<style>.grid2{{grid-template-columns:repeat(2,1fr)}}
.grid2 a{{border-bottom:1px solid var(--line)}}
.grid2 a:nth-child(2n){{border-right:0}}
@media(max-width:940px){{.grid2{{grid-template-columns:1fr}}.grid2 a{{border-right:0}}}}</style>''',
        cta("Vous ne trouvez pas votre réponse ?",
            "Demandez une démo : un spécialiste vous montre le geste sur vos propres documents.",
            {"href": "fr/corrext/", "txt": "Voir la plateforme"}),
    ])
    pages.append(("fr/aide/", {
        "hero": "help",
        "title": "Centre d'aide Corrext · Neur.on",
        "description": "Prendre en main Corrext : traduire un texte ou des fichiers, créer un "
                       "projet de traduction, obtenir un devis, chercher un terme dans CHnell, "
                       "commander un extrait certifié, comprendre où vont vos données.",
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

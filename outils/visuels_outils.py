"""Illustrations des héros des cinq pages outils de Corrext.

Ce ne sont pas des reproductions de l'interface : chaque visuel représente la fonction de l'outil
(traduire, commander une relecture, vérifier un terme, relire, certifier un extrait), dans une même
famille graphique : cartes translucides sur le bleu nuit, traits bleu ciel, accents bleu vif.
Une animation discrète par visuel ; elle disparaît si l'utilisateur limite les animations.

Usage : python3 outils/visuels_outils.py
Écrit chaque SVG directement dans src/pages/corrext/<page>/index.html, entre <!-- visuel:debut --> et
<!-- visuel:fin --> (au premier passage, remplace la carte {{CARTE:…}} du héro).
"""
import os, re

ICI = os.path.dirname(os.path.abspath(__file__))
PAGES = os.path.join(ICI, "..", "src", "pages", "corrext")

# Palette du site
SKY, SKY2, BLUE, PALE, NAVY = "#7FB0FF", "#96BCFF", "#317BFF", "#E3ECFF", "#001B4C"


def defs(p):
    """Dégradés et filtres communs, préfixés pour éviter les collisions d'identifiants."""
    return f'''<defs>
<linearGradient id="{p}g" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#fff" stop-opacity=".13"/><stop offset="1" stop-color="#fff" stop-opacity=".05"/></linearGradient>
<linearGradient id="{p}a" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{SKY2}"/><stop offset="1" stop-color="{BLUE}"/></linearGradient>
<radialGradient id="{p}h"><stop offset="0" stop-color="{BLUE}" stop-opacity=".55"/><stop offset="1" stop-color="{BLUE}" stop-opacity="0"/></radialGradient>
<radialGradient id="{p}w"><stop offset="0" stop-color="#fff" stop-opacity=".95"/><stop offset=".4" stop-color="{SKY2}" stop-opacity=".45"/><stop offset="1" stop-color="{BLUE}" stop-opacity="0"/></radialGradient>
<filter id="{p}s" x="-20%" y="-20%" width="140%" height="160%"><feDropShadow dx="0" dy="14" stdDeviation="14" flood-color="#000a24" flood-opacity=".45"/></filter>
</defs>'''


def carte(x, y, w, h, p, r=10, extra=""):
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{r}" fill="url(#{p}g)" stroke="#fff" stroke-opacity=".18" filter="url(#{p}s)" {extra}/>'


def lignes(x, y, largeurs, couleur="#fff", op=".34", pas=16, h=6):
    return "".join(f'<rect x="{x}" y="{y + i * pas}" width="{w}" height="{h}" rx="{h / 2}" fill="{couleur}" fill-opacity="{op}"/>' for i, w in enumerate(largeurs))


def puce(x, y, txt, p, fond=None):
    fond = fond or f"url(#{p}a)"
    return (f'<rect x="{x}" y="{y}" width="34" height="20" rx="10" fill="{fond}"/>'
            f'<text x="{x + 17}" y="{y + 14}" text-anchor="middle" font-family="Inter, system-ui, sans-serif" font-size="10.5" font-weight="700" fill="#fff" letter-spacing=".04em">{txt}</text>')


def svg(p, label, corps):
    return (f'<svg class="tvis-svg" viewBox="0 0 520 400" width="520" height="400" role="img" aria-label="{label}" focusable="false">'
            f'<style>@media (prefers-reduced-motion:reduce){{.tvis-svg .anim{{display:none}}}}</style>'
            f'{defs(p)}<ellipse cx="260" cy="205" rx="250" ry="175" fill="url(#{p}h)" opacity=".55"/>{corps}</svg>')


def traduction():
    p = "vt"
    gauche = carte(36, 64, 176, 236, p) + lignes(56, 112, [130, 112, 136, 96, 124, 70, 118, 104], op=".3") + puce(56, 80, "DE", p, "rgba(255,255,255,.16)")
    gauche += f'<rect x="56" y="144" width="62" height="6" rx="3" fill="{SKY2}"/>'  # terme repéré dans la source
    droite = carte(308, 64, 176, 184, p) + lignes(328, 112, [124, 136, 104, 130, 92, 120], SKY2, ".55", pas=18) + puce(328, 80, "FR", p)
    droite += f'<rect x="328" y="148" width="70" height="6" rx="3" fill="#fff"/>'
    flux = (f'<path d="M214 150 C 238 150 236 182 230 182" fill="none" stroke="{SKY}" stroke-opacity=".55" stroke-width="1.8"/>'
            f'<path d="M290 182 C 284 182 282 150 306 150" fill="none" stroke="{SKY}" stroke-opacity=".55" stroke-width="1.8"/>')
    moteur = (f'<circle cx="260" cy="182" r="46" fill="url(#{p}h)"/>'
              f'<circle cx="260" cy="182" r="30" fill="url(#{p}a)" stroke="#fff" stroke-opacity=".5"/>'
              f'<path d="M248 176h18m-6-6 6 6-6 6M272 190h-18m6-6-6 6 6 6" fill="none" stroke="#fff" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"/>')
    # alternatives : trois propositions, chacune attribuée à son moteur (pastille de couleur)
    alts = ""
    for i in range(3):
        y = 262 + i * 34
        alts += (f'<rect x="308" y="{y}" width="176" height="26" rx="8" fill="#fff" fill-opacity="{(".16", ".1", ".07")[i]}" stroke="#fff" stroke-opacity="{(".3", ".16", ".12")[i]}"/>'
                 f'<circle cx="323" cy="{y + 13}" r="4.5" fill="{(SKY2, BLUE, "#fff")[i]}"/>'
                 f'<rect x="336" y="{y + 10}" width="{(118, 96, 106)[i]}" height="6" rx="3" fill="#fff" fill-opacity="{(".7", ".42", ".32")[i]}"/>')
    # influx animé : du terme source vers la traduction, en passant par le moteur
    anim = (f'<g class="anim"><circle r="5" fill="url(#{p}w)"><animateMotion dur="3.2s" repeatCount="indefinite" '
            f'path="M118 147 C 170 147 214 150 230 170 C 244 188 276 188 290 170 C 306 152 340 151 398 151" keyPoints="0;1;1" keyTimes="0;.7;1" calcMode="linear"/>'
            f'<animate attributeName="opacity" values="0;1;1;0;0" keyTimes="0;.08;.62;.7;1" dur="3.2s" repeatCount="indefinite"/></circle></g>')
    return svg(p, "Illustration : un document allemand traduit en français par un moteur central, avec plusieurs propositions de traduction",
               gauche + droite + flux + moteur + alts + anim)


def projet():
    p = "vp"
    # fichiers déposés
    fichiers = ""
    for i, (x, y) in enumerate(((40, 96), (56, 118), (72, 140))):
        fichiers += (f'<path d="M{x} {y + 8}a8 8 0 0 1 8-8h70l24 24v104a8 8 0 0 1-8 8h-86a8 8 0 0 1-8-8z" fill="url(#{p}g)" stroke="#fff" stroke-opacity=".2" filter="url(#{p}s)"/>'
                     f'<path d="M{x + 78} {y}v18a6 6 0 0 0 6 6h18" fill="none" stroke="#fff" stroke-opacity=".3"/>')
    fichiers += lignes(88, 182, [70, 58, 74, 46], op=".32", pas=14)
    # tunnel en trois étapes
    etapes = carte(196, 112, 128, 150, p)
    for i in range(3):
        cy = 140 + i * 44
        etapes += (f'<circle cx="222" cy="{cy}" r="11" fill="{"url(#" + p + "a)" if i < 2 else "rgba(255,255,255,.12)"}" stroke="#fff" stroke-opacity=".35"/>'
                   f'<text x="222" y="{cy + 4}" text-anchor="middle" font-family="Inter, system-ui, sans-serif" font-size="11" font-weight="700" fill="#fff">{i + 1}</text>'
                   f'<rect x="242" y="{cy - 3}" width="{(64, 56, 48)[i]}" height="6" rx="3" fill="#fff" fill-opacity="{(".5", ".42", ".25")[i]}"/>')
    etapes += f'<path d="M222 151v18M222 195v18" stroke="{SKY}" stroke-opacity=".6" stroke-width="2" stroke-dasharray="3 4"/>'
    # devis
    devis = carte(344, 82, 140, 196, p) + lignes(362, 106, [84, 104, 72], op=".38", pas=16)
    devis += f'<path d="M362 160h104" stroke="#fff" stroke-opacity=".18"/>' + lignes(362, 174, [96, 60], op=".28", pas=16)
    devis += (f'<rect x="362" y="218" width="104" height="30" rx="8" fill="url(#{p}a)"/>'
              f'<rect x="374" y="230" width="44" height="6" rx="3" fill="#fff" fill-opacity=".9"/><rect x="430" y="230" width="24" height="6" rx="3" fill="#fff" fill-opacity=".9"/>')
    devis += (f'<circle cx="478" cy="88" r="17" fill="#fff"/><path d="M470 88l6 6 10-11" fill="none" stroke="{BLUE}" stroke-width="2.8" stroke-linecap="round" stroke-linejoin="round"/>')
    # relecteur et échéance
    bas = (carte(196, 286, 128, 52, p, 26) + f'<circle cx="222" cy="312" r="14" fill="url(#{p}a)"/><circle cx="222" cy="307" r="5" fill="#fff"/>'
           f'<path d="M213 320a10 7 0 0 1 18 0" fill="#fff"/>' + lignes(244, 303, [62, 44], op=".42", pas=14))
    bas += carte(344, 296, 140, 46, p, 12) + "".join(
        f'<rect x="{358 + i * 17}" y="{311}" width="11" height="11" rx="3" fill="{"#fff" if i == 5 else "rgba(255,255,255,.2)"}"/>' for i in range(7))
    fleches = (f'<path d="M168 190h20" stroke="{SKY}" stroke-opacity=".6" stroke-width="2" marker-end=""/>'
               f'<path d="M182 184l6 6-6 6M330 186h8M332 180l6 6-6 6" fill="none" stroke="{SKY}" stroke-opacity=".7" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>')
    anim = (f'<g class="anim"><circle cx="222" cy="228" r="11" fill="none" stroke="#fff" stroke-width="2">'
            f'<animate attributeName="r" values="11;19" dur="2.4s" repeatCount="indefinite"/>'
            f'<animate attributeName="opacity" values=".8;0" dur="2.4s" repeatCount="indefinite"/></circle></g>')
    return svg(p, "Illustration : des fichiers déposés passent par trois étapes de commande et aboutissent à un devis validé, avec un relecteur et une échéance",
               fichiers + etapes + devis + bas + fleches + anim)


def chnell():
    p = "vc"
    corps = carte(40, 54, 440, 300, p, 14)
    corps += puce(64, 74, "DE", p, "rgba(255,255,255,.16)") + puce(276, 74, "FR", p)
    rangs = ((150, 40), (96, 70), (176, 48), (120, 36), (88, 62))
    for i, (w, pos) in enumerate(rangs):
        y = 112 + i * 46
        corps += (f'<rect x="60" y="{y}" width="196" height="34" rx="8" fill="#fff" fill-opacity=".06"/>'
                  f'<rect x="272" y="{y}" width="190" height="34" rx="8" fill="#fff" fill-opacity=".06"/>'
                  f'<rect x="72" y="{y + 9}" width="{w}" height="5" rx="2.5" fill="#fff" fill-opacity=".3"/>'
                  f'<rect x="72" y="{y + 20}" width="{w - 30}" height="5" rx="2.5" fill="#fff" fill-opacity=".22"/>'
                  f'<rect x="284" y="{y + 9}" width="{w - 6}" height="5" rx="2.5" fill="{SKY2}" fill-opacity=".5"/>'
                  f'<rect x="284" y="{y + 20}" width="{w - 40}" height="5" rx="2.5" fill="{SKY2}" fill-opacity=".36"/>'
                  f'<rect x="{72 + pos}" y="{y + 8}" width="34" height="7" rx="3.5" fill="{SKY2}"/>'
                  f'<rect x="{284 + pos + 6}" y="{y + 8}" width="38" height="7" rx="3.5" fill="#fff"/>'
                  f'<path d="M{106 + pos} {y + 11.5}C {190} {y + 11.5} {230} {y + 11.5} {290 + pos} {y + 11.5}" fill="none" stroke="{SKY}" stroke-opacity=".25" stroke-dasharray="2 4"/>'
                  f'<text x="450" y="{y + 22}" text-anchor="middle" font-family="Georgia, serif" font-size="15" font-weight="700" fill="{SKY2}">§</text>')
    loupe = (f'<g class="anim"><g><circle cx="190" cy="0" r="44" fill="#fff" fill-opacity=".08" stroke="#fff" stroke-width="3" stroke-opacity=".85"/>'
             f'<path d="M222 32l30 30" stroke="#fff" stroke-width="9" stroke-linecap="round" stroke-opacity=".9"/>'
             f'<animateTransform attributeName="transform" type="translate" values="0 140;0 232;0 186;0 140" keyTimes="0;.4;.7;1" dur="9s" repeatCount="indefinite" calcMode="spline" keySplines=".45 0 .55 1;.45 0 .55 1;.45 0 .55 1"/></g></g>')
    return svg(p, "Illustration : un terme surligné dans des segments allemands et français alignés, examiné à la loupe dans son contexte officiel",
               corps + loupe)


def editeur():
    p = "ve"
    corps = carte(36, 58, 448, 290, p, 14)
    corps += f'<rect x="36" y="58" width="448" height="38" rx="14" fill="#fff" fill-opacity=".06"/>' + lignes(56, 74, [70], op=".4") + lignes(140, 74, [46, ], op=".22")
    # anneau d'avancement
    corps += (f'<circle cx="452" cy="77" r="11" fill="none" stroke="#fff" stroke-opacity=".18" stroke-width="3.5"/>'
              f'<circle cx="452" cy="77" r="11" fill="none" stroke="{SKY2}" stroke-width="3.5" stroke-dasharray="41 70" transform="rotate(-90 452 77)" stroke-linecap="round"/>')
    etats = ("ok", "ok", "ok", "edit", "vide")
    for i, e in enumerate(etats):
        y = 110 + i * 46
        bord = f' stroke="{SKY2}" stroke-width="1.6"' if e == "edit" else ' stroke="#fff" stroke-opacity=".08"'
        corps += (f'<rect x="54" y="{y}" width="412" height="36" rx="8" fill="#fff" fill-opacity="{".1" if e == "edit" else ".045"}"{bord}/>'
                  f'<rect x="68" y="{y + 10}" width="{(150, 120, 164, 136, 110)[i]}" height="5" rx="2.5" fill="#fff" fill-opacity=".3"/>'
                  f'<rect x="68" y="{y + 21}" width="{(96, 130, 84, 118, 92)[i]}" height="5" rx="2.5" fill="#fff" fill-opacity=".2"/>'
                  f'<path d="M258 {y + 6}v24" stroke="#fff" stroke-opacity=".12"/>'
                  f'<rect x="272" y="{y + 10}" width="{(132, 116, 140, 100, 0)[i]}" height="5" rx="2.5" fill="{SKY2}" fill-opacity=".55"/>'
                  f'<rect x="272" y="{y + 21}" width="{(88, 120, 92, 0, 0)[i]}" height="5" rx="2.5" fill="{SKY2}" fill-opacity=".4"/>')
        if e == "ok":
            corps += f'<circle cx="446" cy="{y + 18}" r="9" fill="url(#{p}a)"/><path d="M441.5 {y + 18}l3 3 6-6.5" fill="none" stroke="#fff" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>'
        else:
            corps += f'<circle cx="446" cy="{y + 18}" r="9" fill="none" stroke="#fff" stroke-opacity=".3" stroke-width="1.6"/>'
    # propositions sous le segment en cours, curseur dans la traduction de ce segment
    corps += (f'<rect x="300" y="290" width="184" height="78" rx="10" fill="{NAVY}" fill-opacity=".94" stroke="{SKY2}" stroke-opacity=".5" filter="url(#{p}s)"/>'
              + f'<path d="M318 304l3-7 3 7 7 3-7 3-3 7-3-7-7-3z" fill="{SKY2}"/>'
              + "".join(f'<rect x="338" y="{302 + k * 18}" width="{(126, 104, 116)[k]}" height="6" rx="3" fill="#fff" fill-opacity="{(".75", ".45", ".32")[k]}"/>' for k in range(3)))
    anim = (f'<g class="anim"><rect x="374" y="255" width="2" height="16" fill="#fff"><animate attributeName="opacity" values="1;1;0;0" keyTimes="0;.5;.5;1" dur="1.1s" repeatCount="indefinite"/></rect></g>')
    return svg(p, "Illustration : un éditeur de relecture en deux colonnes, segments confirmés un à un, segment en cours avec des propositions de reformulation",
               corps + anim)


def extraits():
    p = "vx"
    # extrait d'origine, en retrait, et traduction certifiée au premier plan
    fond = (f'<g transform="rotate(-6 170 200)">{carte(70, 70, 190, 250, p)}{lignes(92, 110, [120, 96, 136, 88, 110], op=".22", pas=18)}'
            f'{puce(92, 84, "DE", p, "rgba(255,255,255,.14)")}</g>')
    doc = carte(200, 56, 220, 286, p, 12)
    doc += f'<rect x="200" y="56" width="220" height="44" rx="12" fill="url(#{p}a)" fill-opacity=".9"/>' + puce(218, 68, "FR", p, "rgba(255,255,255,.22)")
    doc += lignes(262, 74, [92], "#fff", ".85")
    doc += lignes(220, 118, [170, 150, 176, 132], op=".3", pas=18)
    doc += (f'<rect x="220" y="196" width="180" height="58" rx="8" fill="#fff" fill-opacity=".06" stroke="#fff" stroke-opacity=".12"/>'
            + lignes(232, 208, [70, 96], op=".28", pas=16) + lignes(320, 208, [64, 50], SKY2, ".5", pas=16))
    doc += lignes(220, 272, [96, 70], op=".22", pas=16)
    # sceau de certification et rubans
    sceau = (f'<path d="M376 300l-12 46 18-10 10 18 8-44z" fill="{BLUE}"/><path d="M404 300l12 46-18-10-10 18-8-44z" fill="{SKY}"/>'
             f'<circle cx="390" cy="292" r="36" fill="url(#{p}a)" stroke="#fff" stroke-opacity=".6" stroke-width="2"/>'
             f'<circle cx="390" cy="292" r="27" fill="none" stroke="#fff" stroke-opacity=".7" stroke-dasharray="2 3"/>'
             f'<path d="M378 292l8 8 16-17" fill="none" stroke="#fff" stroke-width="3.2" stroke-linecap="round" stroke-linejoin="round"/>')
    # apostille : étiquette à étoile
    apost = (f'<g transform="rotate(8 458 140)"><rect x="428" y="118" width="62" height="44" rx="8" fill="url(#{p}g)" stroke="#fff" stroke-opacity=".3"/>'
             f'<path d="M459 128l3.5 7 7.5 1-5.5 5.3 1.3 7.5-6.8-3.6-6.8 3.6 1.3-7.5-5.5-5.3 7.5-1z" fill="{SKY2}"/></g>')
    anim = (f'<g class="anim"><circle cx="390" cy="292" r="36" fill="none" stroke="#fff" stroke-width="2">'
            f'<animate attributeName="r" values="36;52" dur="2.8s" repeatCount="indefinite"/><animate attributeName="opacity" values=".7;0" dur="2.8s" repeatCount="indefinite"/></circle></g>')
    return svg(p, "Illustration : un extrait du registre du commerce allemand et sa traduction française certifiée, avec un sceau et une apostille",
               fond + doc + sceau + apost + anim)


VISUELS = {"traduction-texte-et-document": traduction, "gestion-de-projet": projet, "chnell": chnell,
           "editeur-de-relecture": editeur, "extraits-registre-commerce": extraits}


def main():
    for page, f in VISUELS.items():
        chemin = os.path.join(PAGES, page, "index.html")
        s = open(chemin, encoding="utf-8").read()
        bloc = '<!-- visuel:debut --><figure class="tvis">' + f() + "</figure><!-- visuel:fin -->"
        s, n = re.subn(r"<!-- visuel:debut -->.*?<!-- visuel:fin -->", lambda m: bloc, s, flags=re.S)
        if n == 0:
            s, n = re.subn(r"\{\{CARTE:[a-z-]+\}\}", lambda m: bloc, s, count=1)
        if n != 1:
            raise SystemExit(f"Emplacement du visuel introuvable : {page}")
        open(chemin, "w", encoding="utf-8").write(s)
        print("visuel écrit :", page)


if __name__ == "__main__":
    main()

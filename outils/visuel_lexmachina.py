"""Visuel du hero LexMachina : un réseau neuronal en forme de galaxie spirale, rendu en PNG à fond transparent.

Usage : python3 outils/visuel_lexmachina.py
Produit assets/img/lexmachina-reseau.png (1040 × 800 px, affiché en 520 × 400).
Le dessin est déterministe (graine fixe) : même image à chaque exécution.
"""
import math, os, random, subprocess, tempfile

W, H = 520, 400
ICI = os.path.dirname(os.path.abspath(__file__))
SORTIE = os.path.join(ICI, "..", "assets", "img", "lexmachina-reseau.png")
CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
rnd = random.Random(230)


def projeter(x, y):
    """Galaxie vue de biais : aplatissement vertical puis légère rotation."""
    y *= .58
    a = math.radians(-16)
    return W / 2 + x * math.cos(a) - y * math.sin(a), H / 2 + x * math.sin(a) + y * math.cos(a)


BRAS = 3


def spirale(b, t, jr=0.0, ja=0.0):
    r = 16 + 215 * t ** .9 + jr
    th = b * 2 * math.pi / BRAS + 3.4 * math.pi * t ** .75 + ja
    return projeter(r * math.cos(th), r * math.sin(th))


def points():
    """Neurones le long des bras (dans l'ordre du bras) et au cœur."""
    bras = []
    for b in range(BRAS):
        ligne = []
        for i in range(84):
            t = (i + rnd.random() * .6) / 84
            x, y = spirale(b, t, rnd.gauss(0, 3 + 9 * t), rnd.gauss(0, .045))
            ligne.append((x, y, 1 - t))
        bras.append(ligne)
    coeur = []
    for _ in range(26):
        r = abs(rnd.gauss(0, 13)); th = rnd.random() * 2 * math.pi
        coeur.append((*projeter(r * math.cos(th), r * math.sin(th)), 1.0))
    return bras, coeur


def svg():
    bras, coeur = points()
    pts = [p for ligne in bras for p in ligne] + coeur
    fils = []
    def fil(p, q, o, w, c="url(#fil)"):
        fils.append(f'<line x1="{p[0]:.1f}" y1="{p[1]:.1f}" x2="{q[0]:.1f}" y2="{q[1]:.1f}" stroke="{c}" stroke-opacity="{o:.2f}" stroke-width="{w:.2f}"/>')
    for ligne in bras:
        for k in range(len(ligne) - 1):
            p, q = ligne[k], ligne[k + 1]
            fil(p, q, .25 + .55 * p[2], .5 + 1.1 * p[2])
            if k + 3 < len(ligne) and rnd.random() < .35:
                fil(p, ligne[k + 3], .12 + .3 * p[2], .5)
    # Liaisons transverses entre voisins proches : la toile du réseau
    vus = set()
    for i, p in enumerate(pts):
        for j in sorted(range(len(pts)), key=lambda j: (pts[j][0] - p[0]) ** 2 + (pts[j][1] - p[1]) ** 2)[1:3]:
            d = math.dist(p[:2], pts[j][:2]); cle = tuple(sorted((i, j)))
            if d < 30 and cle not in vus:
                vus.add(cle); fil(p, pts[j], .1 + .35 * max(p[2], pts[j][2]), .45)
    for _ in range(14):
        i, j = rnd.randrange(len(pts)), rnd.randrange(len(pts))
        if 80 < math.dist(pts[i][:2], pts[j][:2]) < 180:
            fil(pts[i], pts[j], .16, .5, "#bcd5ff")
    poussiere = []
    for _ in range(420):
        b, t = rnd.randrange(BRAS), rnd.random()
        x, y = spirale(b, t, rnd.gauss(0, 10 + 22 * t), rnd.gauss(0, .14))
        poussiere.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{rnd.uniform(.35, 1):.2f}" fill="#d6e5ff" fill-opacity="{rnd.uniform(.1, .55):.2f}"/>')
    noeuds = []
    for x, y, e in pts:
        brillant = rnd.random() < .16 or e > .93
        noeuds.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{3 + 5 * e + (3 if brillant else 0):.1f}" fill="url(#halo)" fill-opacity="{.25 + .45 * e:.2f}"/>')
        noeuds.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{.9 + 1.5 * e + (.7 if brillant else 0):.2f}" fill="{"#ffffff" if brillant else "#a9c8ff"}"/>')
    cx, cy = projeter(0, 0)
    fond = (f'<ellipse cx="{cx:.1f}" cy="{cy:.1f}" rx="150" ry="82" fill="url(#coeur)" transform="rotate(-16 {cx:.1f} {cy:.1f})"/>'
            f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="22" fill="url(#halo)"/>')
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}">
<defs>
  <linearGradient id="fil" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#cfe0ff"/><stop offset="1" stop-color="#5b8fe6"/></linearGradient>
  <radialGradient id="halo"><stop offset="0" stop-color="#ffffff" stop-opacity=".9"/><stop offset=".35" stop-color="#9cc2ff" stop-opacity=".35"/><stop offset="1" stop-color="#317bff" stop-opacity="0"/></radialGradient>
  <radialGradient id="coeur"><stop offset="0" stop-color="#cfe0ff" stop-opacity=".5"/><stop offset=".45" stop-color="#5b8fe6" stop-opacity=".16"/><stop offset="1" stop-color="#317bff" stop-opacity="0"/></radialGradient>
</defs>
{fond}{"".join(poussiere)}{"".join(fils)}{"".join(noeuds)}
</svg>'''


def main():
    html = f'<!doctype html><html><head><meta charset="utf-8"><style>html,body{{margin:0;background:transparent}}svg{{display:block}}</style></head><body>{svg()}</body></html>'
    with tempfile.TemporaryDirectory() as d:
        page = os.path.join(d, "v.html")
        open(page, "w").write(html)
        subprocess.run([CHROME, "--headless=new", "--disable-gpu", "--hide-scrollbars", "--force-device-scale-factor=2",
                        "--default-background-color=00000000", f"--window-size={W},{H}", f"--screenshot={os.path.abspath(SORTIE)}",
                        "file://" + page], check=True, capture_output=True)
    print("écrit :", os.path.abspath(SORTIE))


if __name__ == "__main__":
    main()

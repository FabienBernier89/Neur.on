"""Visuel du hero LexMachina : réseau neuronal entraîné, rendu en PNG à fond transparent.

Usage : python3 outils/visuel_lexmachina.py
Produit assets/img/lexmachina-reseau.png (1040 × 660 px, affiché en 520 × 330).
Le dessin est déterministe : mêmes poids, même image à chaque exécution.
"""
import math, os, subprocess, tempfile

W, H = 520, 330
ENTREES = ["ATF / BGE", "FINMA", "Codes et lois"]
SORTIES = ["Deutsch", "Français", "Italiano", "English"]
ICI = os.path.dirname(os.path.abspath(__file__))
SORTIE = os.path.join(ICI, "..", "assets", "img", "lexmachina-reseau.png")
CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"


def poids(a, b, k):
    return ((a * 37 + b * 91 + k * 53 + a * b * 7) % 100) / 100


def colonne(n, haut, bas):
    return [haut + i * (bas - haut) / (n - 1) for i in range(n)]


def courbe(x1, y1, x2, y2):
    dx = (x2 - x1) * .5
    return f"M{x1:.1f} {y1:.1f} C{x1 + dx:.1f} {y1:.1f} {x2 - dx:.1f} {y2:.1f} {x2:.1f} {y2:.1f}"


def svg():
    xe, xs = 148, 390
    couches = [(xe, colonne(3, 72, 258))] + [(x, colonne(7, 34, 296)) for x in (208, 268, 328)] + [(xs, colonne(4, 52, 278))]
    fils, forts = [], []
    for k in range(len(couches) - 1):
        (xa, ya), (xb, yb) = couches[k], couches[k + 1]
        for i, a in enumerate(ya):
            for j, b in enumerate(yb):
                w = poids(i, j, k)
                if w < .28:
                    continue
                d = courbe(xa, a, xb, b)
                fils.append(f'<path d="{d}" stroke="url(#fil)" stroke-opacity="{.16 + w * .5:.2f}" stroke-width="{.5 + w * 1.3:.2f}" fill="none"/>')
                if (i * 3 + j + k) % 4 == 0 and w > .5:
                    forts.append(f'<path d="{d}" stroke="#bcd5ff" stroke-width="1.6" fill="none" filter="url(#lueur)" stroke-opacity=".85"/>')
    # Flux de données : segments qui entrent dans le réseau depuis chaque source
    flux = []
    for i, y in enumerate(couches[0][1]):
        for s in range(4):
            t = s / 4
            x = 2 + t * 26
            dy = math.sin(s * 1.7 + i) * 7 * (1 - t)
            flux.append(f'<rect x="{x:.1f}" y="{y + dy - 2:.1f}" width="{4 + (s % 2) * 3}" height="4" rx="2" fill="#9cc2ff" fill-opacity="{.15 + t * .5:.2f}"/>')
    noeuds = []
    for k, (x, col) in enumerate(couches[1:-1]):
        for i, y in enumerate(col):
            actif = (i * 2 + k) % 3 == 0
            noeuds.append(f'<circle cx="{x}" cy="{y:.1f}" r="{13 if actif else 9}" fill="url(#halo)" fill-opacity="{1 if actif else .55}"/>')
            noeuds.append(f'<circle cx="{x}" cy="{y:.1f}" r="{4.6 if actif else 3.6}" fill="{"#ffffff" if actif else "#7fb0ff"}"/>')
    def pastille(x, y, w, texte, align):
        return (f'<rect x="{x}" y="{y - 15}" width="{w}" height="30" rx="15" fill="#ffffff" fill-opacity=".07" stroke="#ffffff" stroke-opacity=".26"/>'
                f'<text x="{x + w / 2}" y="{y + 4.5}" text-anchor="middle" font-family="Inter, -apple-system, Helvetica, Arial, sans-serif" font-size="12.5" font-weight="600" fill="#ffffff">{texte}</text>')
    entrees = "".join(pastille(32, y, 108, t, "c") + f'<circle cx="{xe}" cy="{y:.1f}" r="12" fill="url(#halo)"/><circle cx="{xe}" cy="{y:.1f}" r="4.2" fill="#ffffff"/>'
                      for t, y in zip(ENTREES, couches[0][1]))
    sorties = "".join(f'<circle cx="{xs}" cy="{y:.1f}" r="12" fill="url(#halo)"/><circle cx="{xs}" cy="{y:.1f}" r="4.2" fill="#ffffff"/>' + pastille(xs + 16, y, 100, t, "c")
                      for t, y in zip(SORTIES, couches[-1][1]))
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}">
<defs>
  <linearGradient id="fil" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#7fb0ff"/><stop offset="1" stop-color="#317bff"/></linearGradient>
  <radialGradient id="halo"><stop offset="0" stop-color="#cfe0ff" stop-opacity=".95"/><stop offset=".45" stop-color="#7fb0ff" stop-opacity=".35"/><stop offset="1" stop-color="#317bff" stop-opacity="0"/></radialGradient>
  <filter id="lueur" x="-20%" y="-20%" width="140%" height="140%"><feGaussianBlur stdDeviation="2.2" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>
</defs>
{"".join(flux)}{"".join(fils)}{"".join(forts)}{"".join(noeuds)}{entrees}{sorties}
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

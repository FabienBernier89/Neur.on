"""Visuel du hero LexMachina : réseau de neurones épuré, en perspective, en cours d'entraînement.

SVG animé (SMIL), fond transparent, sans texte. Quelques signaux traversent les couches
(propagation avant) puis reviennent (rétropropagation) ; les connexions respirent ; l'ensemble flotte.
Les animations sont coupées si l'utilisateur limite les mouvements (prefers-reduced-motion).

Usage : python3 outils/visuel_lexmachina.py
Écrit le SVG directement dans src/pages/lexmachina/index.html, entre <!-- reseau:debut --> et
<!-- reseau:fin --> (au premier passage, remplace l'ancienne image WebP et sa couche d'influx).
Dessin déterministe (graine fixe) : même image à chaque exécution.
"""
import os, re
import random
random.seed(41)
W,H,T=520,400,10.0
X=[70,197,323,450]; N=[4,6,6,3]; CY=200; GAP=54
ys=lambda n:[CY+(i-(n-1)/2)*GAP for i in range(n)]
nodes=[[(X[l],y) for y in ys(N[l])] for l in range(4)]
f=lambda v:f"{v:.1f}"
import math
# Perspective : le plan du réseau pivote en 3D (rotation Y puis X), le fond s'éloigne
AY,AX,D,K=math.radians(-34),math.radians(14),700,1.06
def pr(x,y):
    u,v=x-260,y-200
    x1,z=u*math.cos(AY),u*math.sin(AY)
    y1,z1=v*math.cos(AX)-z*math.sin(AX),v*math.sin(AX)+z*math.cos(AX)
    sc=D/(D+z1)
    return (238+x1*sc*K,200+y1*sc*K,sc)

kt=lambda v:f"{max(0,min(1,v/T)):.4f}"
def curve(a,b):
    dx=(b[0]-a[0])*.5
    p=[pr(*a),pr(a[0]+dx,a[1]),pr(b[0]-dx,b[1]),pr(*b)]
    return f"M{f(p[0][0])} {f(p[0][1])}C{f(p[1][0])} {f(p[1][1])} {f(p[2][0])} {f(p[2][1])} {f(p[3][0])} {f(p[3][1])}"
o=[f'<svg class="nnviz" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" aria-label="Réseau de neurones en cours d’entraînement : des signaux traversent les couches puis reviennent pour ajuster les connexions" xmlns="http://www.w3.org/2000/svg">']
o.append('<defs>'
 '<radialGradient id="nnh"><stop offset="0" stop-color="#fff" stop-opacity=".9"/><stop offset=".35" stop-color="#96BCFF" stop-opacity=".45"/><stop offset="1" stop-color="#317BFF" stop-opacity="0"/></radialGradient>'
 '<radialGradient id="nnbg" cx="50%" cy="50%" r="50%"><stop offset="0" stop-color="#317BFF" stop-opacity=".22"/><stop offset="1" stop-color="#317BFF" stop-opacity="0"/></radialGradient>'
 f'<linearGradient id="nne" x1="0" y1="0" x2="{W}" y2="0" gradientUnits="userSpaceOnUse"><stop offset="0" stop-color="#7FB0FF"/><stop offset=".5" stop-color="#317BFF"/><stop offset="1" stop-color="#96BCFF"/></linearGradient>'
 '<linearGradient id="nnn" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#1f5fd6"/><stop offset="1" stop-color="#06246b"/></linearGradient>'
 '</defs>')
o.append('<g><animateTransform class="nn-anim" attributeName="transform" type="translate" values="0 0;0 -5;0 0" dur="7s" repeatCount="indefinite" calcMode="spline" keyTimes="0;.5;1" keySplines=".45 0 .55 1;.45 0 .55 1"/>')
o.append(f'<ellipse cx="{W/2}" cy="{CY}" rx="250" ry="185" fill="url(#nnbg)"/>')
# Connexions : courbes douces, poids qui respirent
o.append('<g fill="none" stroke="url(#nne)" stroke-linecap="round">')
E={}
for l in range(3):
    for i,a in enumerate(nodes[l]):
        for j,b in enumerate(nodes[l+1]):
            d=curve(a,b); E[(l,i,j)]=d
            op=.10+.22*random.random()**1.5; o2=.08+.32*random.random()
            du=random.uniform(3,7); bg=random.uniform(0,du)
            o.append(f'<path d="{d}" stroke-width=".9" stroke-opacity="{op:.2f}"><animate class="nn-anim" attributeName="stroke-opacity" values="{op:.2f};{o2:.2f};{op:.2f}" dur="{du:.1f}s" begin="-{bg:.1f}s" repeatCount="indefinite"/></path>')
o.append('</g>')
# Deux passes par cycle : propagation avant, puis retour (rétropropagation)
def route(): return [random.randrange(n) for n in N]
FW0,FG,FD=.3,.75,.7
BW0,BG,BD=2.9,.6,.55
anim=[];act={}
for t0 in (0,T/2):
    rs=[route() for _ in range(3)]
    segs=sorted({(l,r[l],r[l+1]) for r in rs for l in range(3)})
    for r in rs:
        for l in range(4): act.setdefault((l,r[l]),[]).append(t0+FW0+l*FG)
    for (l,i,j) in segs:
        d=E[(l,i,j)]
        s=t0+FW0+l*FG+.05; e=s+FD
        # trait lumineux qui suit l'influx
        anim.append(f'<path d="{d}" fill="none" stroke="#cfe0ff" stroke-width="1.6" stroke-linecap="round" stroke-opacity="0"><animate attributeName="stroke-opacity" values="0;0;.7;0;0" keyTimes="0;{kt(s)};{kt(e)};{kt(e+.6)};1" dur="{T}s" repeatCount="indefinite"/></path>')
        anim.append(f'<g opacity="0"><circle r="7" fill="url(#nnh)"/><circle r="1.8" fill="#fff"/><animateMotion path="{d}" dur="{T}s" repeatCount="indefinite" keyPoints="0;0;1;1" keyTimes="0;{kt(s)};{kt(e)};1" calcMode="spline" keySplines="0 0 1 1;.45 0 .55 1;0 0 1 1"/><animate attributeName="opacity" values="0;0;1;1;0;0" keyTimes="0;{kt(s)};{kt(s+.08)};{kt(e-.06)};{kt(e)};1" dur="{T}s" repeatCount="indefinite"/></g>')
        # retour plus discret
        s=t0+BW0+(2-l)*BG; e=s+BD
        anim.append(f'<g opacity="0"><circle r="4.5" fill="url(#nnh)" opacity=".6"/><circle r="1.2" fill="#E3ECFF"/><animateMotion path="{d}" dur="{T}s" repeatCount="indefinite" keyPoints="1;1;0;0" keyTimes="0;{kt(s)};{kt(e)};1" calcMode="spline" keySplines="0 0 1 1;.45 0 .55 1;0 0 1 1"/><animate attributeName="opacity" values="0;0;.75;.75;0;0" keyTimes="0;{kt(s)};{kt(s+.08)};{kt(e-.06)};{kt(e)};1" dur="{T}s" repeatCount="indefinite"/></g>')
o.append('<g class="nn-anim">'+"".join(anim)+'</g>')
# Neurones : disque, anneau, noyau ; halo au passage de l'influx
for l in range(4):
    for i,(x0,y0) in enumerate(nodes[l]):
        x,y,sc=pr(x0,y0); R=lambda r:f"{r*sc:.2f}"; dim=min(1,.55+.6*(sc-.8)/.4)
        o.append(f'<g opacity="{dim:.2f}">')
        o.append(f'<circle cx="{f(x)}" cy="{f(y)}" r="{R(9)}" fill="url(#nnn)" stroke="#7FB0FF" stroke-opacity=".7" stroke-width="1.2"/><circle cx="{f(x)}" cy="{f(y)}" r="{R(3)}" fill="#96BCFF" fill-opacity=".75"/>')
        ts=act.get((l,i))
        if ts:
            v=["0"];k=["0"];fin=-1
            # Instants dédoublonnés ; deux activations qui se chevauchent ne font qu'une lueur (keyTimes croissants)
            for t in sorted(set(ts)):
                if t-.03<=fin: continue
                for dt,val in ((-.03,0),(.15,1),(1.1,0)): k.append(kt(t+dt)); v.append(str(val))
                fin=t+1.1
            k.append("1"); v.append("0")
            o.append(f'<g class="nn-anim" opacity="0"><circle cx="{f(x)}" cy="{f(y)}" r="{R(24)}" fill="url(#nnh)"/><circle cx="{f(x)}" cy="{f(y)}" r="{R(9)}" fill="#317BFF" stroke="#fff" stroke-width="1.2"/><circle cx="{f(x)}" cy="{f(y)}" r="{R(3.4)}" fill="#fff"/><animate attributeName="opacity" values="{";".join(v)}" keyTimes="{";".join(k)}" dur="{T}s" repeatCount="indefinite"/></g>')
        o.append('</g>')
o.append('</g></svg>')
svg="".join(o).replace('role="img"','role="img" focusable="false"')
svg=svg.replace('<defs>','<style>@media (prefers-reduced-motion:reduce){.nnviz .nn-anim{display:none}}</style><defs>',1)

ICI=os.path.dirname(os.path.abspath(__file__))
SRC=os.path.join(ICI,"..","src","pages","lexmachina","index.html")
page=open(SRC,encoding="utf-8").read()
bloc="<!-- reseau:debut -->"+svg+"<!-- reseau:fin -->"
page,n=re.subn(r"<!-- reseau:debut -->.*?<!-- reseau:fin -->",lambda m:bloc,page,flags=re.S)
if n==0:
    # Premier passage : remplace l'image galaxie et la couche d'influx
    page,n=re.subn(r'<img src="\{\{ROOT\}\}assets/img/lexmachina-reseau\.webp"[^>]*>\s*<!-- influx:debut -->.*?<!-- influx:fin -->',lambda m:bloc,page,flags=re.S)
if n!=1:
    raise SystemExit("Emplacement du visuel introuvable dans la page LexMachina")
open(SRC,"w",encoding="utf-8").write(page)
print(f"visuel écrit dans la page LexMachina ({len(svg)//1024} Ko)")

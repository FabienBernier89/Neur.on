"""Visuel du hero LexMachina : un réseau de neurones en forme de galaxie spirale.

Chaque étoile des bras est un neurone : corps cellulaire lumineux, arbre de dendrites ramifiées,
axone courbé qui suit le sens de rotation de la galaxie et se termine par des boutons synaptiques.
Le dessin se fait sur un canvas dans Chrome sans interface (mélange additif, halo lumineux par flou),
puis Python écrit l'image et la couche animée des influx nerveux.

Usage : python3 outils/visuel_lexmachina.py
Produit :
  assets/img/lexmachina-reseau.webp (1040 × 800 px, affiché en 520 × 400, fond transparent)
  la couche des influx qui parcourent quelques axones (SVG animé en SMIL), écrite directement dans
  src/pages/lexmachina/index.html entre les marqueurs <!-- influx:debut --> et <!-- influx:fin -->
Le dessin est déterministe (graine fixe) : même image à chaque exécution.
"""
import base64, html, io, json, os, re, subprocess, tempfile

from PIL import Image

ICI = os.path.dirname(os.path.abspath(__file__))
IMG = os.path.join(ICI, "..", "assets", "img")
CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"

DESSIN = r"""
const W=520,H=400,S=2;
function toile(){const c=document.createElement('canvas');c.width=W*S;c.height=H*S;const x=c.getContext('2d');x.setTransform(S,0,0,S,0,0);return [c,x];}
let graine=230;
const R=()=>{graine|=0;graine=graine+0x6D2B79F5|0;let t=Math.imul(graine^graine>>>15,1|graine);t=t+Math.imul(t^t>>>7,61|t)^t;return((t^t>>>14)>>>0)/4294967296;};
const U=(a,b)=>a+(b-a)*R();
const G=()=>{let u=0;while(!u)u=R();return Math.sqrt(-2*Math.log(u))*Math.cos(2*Math.PI*R());};
const TAU=Math.PI*2;

// Galaxie vue de biais : disque incliné puis tourné
const CX=W/2,CY=H/2+2,K=224,INC=.56,ROT=-17*Math.PI/180,cr=Math.cos(ROT),sr=Math.sin(ROT);
const P=(u,v)=>[CX+K*(u*cr-v*INC*sr),CY+K*(u*sr+v*INC*cr)];
const PV=(du,dv)=>{const x=du*cr-dv*INC*sr,y=du*sr+dv*INC*cr,l=Math.hypot(x,y)||1;return [x/l,y/l];};
// Les arbres de dendrites sont moins aplatis que le disque, pour rester lisibles
const LINC=.74;
const L=(x,y,du,dv)=>[x+du*cr-dv*LINC*sr,y+du*sr+dv*LINC*cr];

// Bras en spirale logarithmique : deux bras majeurs, deux bras secondaires
const PAS=Math.tan(15*Math.PI/180),R0=.11;
const BRAS=[{t0:0,r1:.13,r2:.99,w:1},{t0:Math.PI,r1:.13,r2:.99,w:1},{t0:Math.PI*.5+.55,r1:.34,r2:.86,w:.5},{t0:Math.PI*1.5+.55,r1:.38,r2:.8,w:.42}];
function surBras(b,r,dec){
  const th=b.t0+Math.log(r/R0)/PAS,u=r*Math.cos(th),v=r*Math.sin(th);
  const er=[Math.cos(th),Math.sin(th)],et=[-Math.sin(th),Math.cos(th)];
  return [u+er[0]*dec,v+er[1]*dec];
}
// Sens de l'écoulement le long des bras (vers l'extérieur), en tout point du disque
function flux(u,v){const r=Math.hypot(u,v)||1,er=[u/r,v/r],et=[-v/r,u/r],sp=Math.sin(15*Math.PI/180),cp=Math.cos(15*Math.PI/180);return [er[0]*sp+et[0]*cp,er[1]*sp+et[1]*cp];}

const [cScene,scene]=toile(),[cLoin,loin]=toile();
const neurones=[];
function neurone(u,v,o){
  const [x,y]=P(u,v),r=Math.hypot(u,v),pres=Math.max(-1,Math.min(1,v));
  const n=Object.assign({u,v,x,y,r,pres,ctx:pres<-.38?loin:scene,b:(.74+.26*(pres+1)/2)*(1-.18*r)},o);
  neurones.push(n);return n;
}

// 1 · Neurones le long des bras
const parBras=BRAS.map((b,i)=>{
  const l=[];let r=b.r1*U(1,1.08);
  while(r<b.r2){
    const [u,v]=surBras(b,r,G()*.022);
    const pivot=R()<(b.w>.9?.17:.08);
    l.push(neurone(u,v,{bras:i,s:pivot?U(2.7,3.5):U(1.15,2.2)*(b.w>.9?1:.85),pivot,dl:(4+16*Math.pow(Math.min(1,r/.7),1.3))*(pivot?1.25:1)*(b.w>.9?1:.8),k:pivot?6+(R()*3|0):(r<.3?3:4)+(R()*3|0)}));
    r*=1+U(.075,.11);
  }
  return l;
});
// 2 · Bulbe central : petits neurones serrés
const coeur=[];
for(let i=0;i<20;i++){const r=Math.abs(G())*.07+.018,a=R()*TAU;coeur.push(neurone(r*Math.cos(a),r*Math.sin(a),{bras:-1,s:U(.8,1.4),pivot:false,dl:U(3,5.5),k:3+(R()*2|0)}));coeur[coeur.length-1].b*=.6;}
// 3 · Neurones isolés entre les bras, plus discrets
const isoles=[];
for(let i=0;i<18;i++){const r=U(.3,.92),a=R()*TAU;const n=neurone(r*Math.cos(a),r*Math.sin(a),{bras:-2,s:U(.9,1.4),pivot:false,dl:U(5,9),k:3+(R()*2|0)});n.b*=.62;isoles.push(n);}

// ---------- Fond : disque, nébuleuse des bras, poussière d'étoiles, bulbe ----------
scene.globalCompositeOperation='lighter';loin.globalCompositeOperation='lighter';
function ellipse(ctx,rad,stops){ctx.save();ctx.translate(CX,CY);ctx.rotate(ROT);ctx.scale(1,INC);const g=ctx.createRadialGradient(0,0,0,0,0,rad);stops.forEach(s=>g.addColorStop(s[0],s[1]));ctx.fillStyle=g;ctx.fillRect(-rad,-rad,rad*2,rad*2);ctx.restore();}
ellipse(scene,K*1.04,[[0,'rgba(120,165,255,.16)'],[.35,'rgba(49,123,255,.07)'],[1,'rgba(49,123,255,0)']]);
function tache(ctx,x,y,rad,c,a){const g=ctx.createRadialGradient(x,y,0,x,y,rad);g.addColorStop(0,`rgba(${c},${a})`);g.addColorStop(1,`rgba(${c},0)`);ctx.fillStyle=g;ctx.beginPath();ctx.arc(x,y,rad,0,TAU);ctx.fill();}
BRAS.forEach(b=>{for(let r=b.r1*.8;r<b.r2*1.04;r+=.006){const [u,v]=surBras(b,r,G()*.03);const [x,y]=P(u,v);const f=Math.min(1,(r-b.r1*.8)/.08)*Math.min(1,(b.r2*1.04-r)/.12);tache(scene,x,y,(7+17*r)*U(.7,1.25),'49,123,255',.05*b.w*f);if(R()<.35)tache(scene,x,y,(3+6*r)*U(.6,1.2),'156,194,255',.05*b.w*f);}});
// Poussière : la matière des bras, plus quelques étoiles du disque
for(let i=0;i<11000;i++){
  let u,v,r;
  if(R()<.8){const b=BRAS[R()<.82?(R()*2|0):2+(R()*2|0)];r=b.r1*.7+(b.r2*1.05-b.r1*.7)*Math.pow(R(),1.25);[u,v]=surBras(b,r,G()*(.014+.05*r));}
  else{r=-Math.log(1-R()*.98)*.28;const a=R()*TAU;u=r*Math.cos(a);v=r*Math.sin(a);}
  if(r>1.1)continue;
  const [x,y]=P(u,v),pres=Math.max(-1,Math.min(1,v)),a=U(.12,.72)*(.75+.25*(pres+1)/2)*Math.min(1,(1.1-r)/.2);
  const c=r<.3?'232,241,255':(R()<.5?'188,213,255':'140,182,255');
  scene.fillStyle=`rgba(${c},${a.toFixed(3)})`;
  const z=R()<.06?U(.55,.9):U(.22,.48);
  scene.beginPath();scene.arc(x,y,z,0,TAU);scene.fill();
}
// Bulbe : cœur lumineux et halo
ellipse(scene,K*.34,[[0,'rgba(255,255,255,.7)'],[.05,'rgba(232,241,255,.5)'],[.16,'rgba(150,190,255,.26)'],[.42,'rgba(70,135,255,.1)'],[1,'rgba(49,123,255,0)']]);
for(let i=0;i<900;i++){const r=Math.abs(G())*.09,a=R()*TAU;const [x,y]=P(r*Math.cos(a),r*Math.sin(a));scene.fillStyle=`rgba(232,241,255,${U(.1,.42).toFixed(2)})`;scene.beginPath();scene.arc(x,y,U(.2,.5),0,TAU);scene.fill();}

// ---------- Axones ----------
const axones=[];
function bez(p,t){const m=1-t;return [m*m*m*p[0][0]+3*m*m*t*p[1][0]+3*m*t*t*p[2][0]+t*t*t*p[3][0],m*m*m*p[0][1]+3*m*m*t*p[1][1]+3*m*t*t*p[2][1]+t*t*t*p[3][1]];}
function axone(A,B,genre){
  if(A===B)return;
  const p0=[A.x,A.y],p3=[B.x+G()*1.2,B.y+G()*1.2],d=Math.hypot(p3[0]-p0[0],p3[1]-p0[1]);if(d<4)return;
  let fa=flux(A.u,A.v),fb=flux(B.u,B.v);
  const ch=[p3[0]-p0[0],p3[1]-p0[1]];
  let ta=PV(fa[0],fa[1]),tb=PV(fb[0],fb[1]);
  if(ta[0]*ch[0]+ta[1]*ch[1]<0)ta=[-ta[0],-ta[1]];
  if(tb[0]*ch[0]+tb[1]*ch[1]<0)tb=[-tb[0],-tb[1]];
  const k=d*(genre==='long'?.42:.36);
  const p=[p0,[p0[0]+ta[0]*k,p0[1]+ta[1]*k],[p3[0]-tb[0]*k,p3[1]-tb[1]*k],p3];
  const ctx=(A.ctx===loin&&B.ctx===loin)?loin:scene;
  const b=Math.min(A.b,B.b)*(genre==='long'?.5:genre==='coeur'?.85:1);
  axones.push({p,d,b,genre,ctx,A,B});
}
parBras.forEach(l=>{for(let i=0;i<l.length;i++){if(i+1<l.length&&R()<.94)axone(l[i],l[i+1],'bras');if(i+2<l.length&&R()<.3)axone(l[i],l[i+2],'bras');}});
const tous=neurones.filter(n=>n.bras>=0);
tous.forEach(n=>{if(R()<.3){const c=tous.filter(m=>m.bras!==n.bras).map(m=>[m,Math.hypot(m.x-n.x,m.y-n.y)]).filter(e=>e[1]>26&&e[1]<92).sort((a,b)=>a[1]-b[1]);if(c.length)axone(n,c[R()*Math.min(2,c.length)|0][0],'travers');}});
tous.forEach(n=>{if(n.r<.48&&R()<.38)axone(n,coeur[R()*coeur.length|0],'coeur');});
parBras.forEach(l=>{if(l.length)axone(coeur[R()*coeur.length|0],l[0],'coeur');});
coeur.forEach(n=>{const c=coeur.filter(m=>m!==n).sort((a,b)=>Math.hypot(a.x-n.x,a.y-n.y)-Math.hypot(b.x-n.x,b.y-n.y));axone(n,c[R()*3|0],'coeur');});
isoles.forEach(n=>{const c=tous.map(m=>[m,Math.hypot(m.x-n.x,m.y-n.y)]).sort((a,b)=>a[1]-b[1]);axone(n,c[0][0],'bras');if(R()<.6)axone(c[1][0],n,'bras');});
for(let i=0,essais=0;i<7&&essais<400;essais++){const A=tous[R()*tous.length|0],B=tous[R()*tous.length|0];const d=Math.hypot(A.x-B.x,A.y-B.y);if(d>120&&d<230&&A.bras!==B.bras){axone(A,B,'long');i++;}}

function tracerAxone(a){
  const {p,ctx,b}=a;
  ctx.beginPath();ctx.moveTo(...p[0]);ctx.bezierCurveTo(...p[1],...p[2],...p[3]);
  ctx.lineCap='round';
  ctx.strokeStyle=`rgba(49,123,255,${(.07*b).toFixed(3)})`;ctx.lineWidth=2.8;ctx.stroke();
  ctx.strokeStyle=`rgba(160,195,255,${(.36*b).toFixed(3)})`;ctx.lineWidth=a.genre==='long'?.45:U(.55,.85);ctx.stroke();
  // Cône d'émergence : l'axone part plus épais du corps cellulaire
  ctx.beginPath();ctx.moveTo(...p[0]);const q=bez(p,.08);ctx.lineTo(...q);ctx.strokeStyle=`rgba(210,226,255,${(.4*b).toFixed(3)})`;ctx.lineWidth=1.2;ctx.stroke();
  // Arborisation terminale et boutons synaptiques
  const e=p[3],f=bez(p,.97),dir=Math.atan2(e[1]-f[1],e[0]-f[0]),nb=3+(R()*3|0);
  for(let i=0;i<nb;i++){
    const an=dir+(i/(nb-1)-.5)*U(1.6,2.4)+G()*.15,lg=U(2.5,6);
    const m=[e[0]+Math.cos(an)*lg*.5+G()*.6,e[1]+Math.sin(an)*lg*.5+G()*.6],t=[e[0]+Math.cos(an)*lg,e[1]+Math.sin(an)*lg];
    ctx.beginPath();ctx.moveTo(...e);ctx.quadraticCurveTo(...m,...t);ctx.strokeStyle=`rgba(169,200,255,${(.38*b).toFixed(3)})`;ctx.lineWidth=.4;ctx.stroke();
    tache(ctx,t[0],t[1],2.2,'156,194,255',.35*b);
    ctx.fillStyle=`rgba(236,244,255,${(.85*b).toFixed(3)})`;ctx.beginPath();ctx.arc(t[0],t[1],.55,0,TAU);ctx.fill();
  }
  // Quelques influx figés en plein trajet, avec leur traînée
  if(a.genre!=='long'&&a.d>30&&R()<.2){
    const t0=U(.3,.78);
    for(let j=0;j<14;j++){const t=t0-j*.012;if(t<0)break;const q=bez(p,t);ctx.fillStyle=`rgba(214,230,255,${(.5*(1-j/14)*b).toFixed(3)})`;ctx.beginPath();ctx.arc(q[0],q[1],1.05*(1-j/18),0,TAU);ctx.fill();}
    const q=bez(p,t0);tache(ctx,q[0],q[1],7,'120,170,255',.45*b);tache(ctx,q[0],q[1],2.6,'255,255,255',.85*b);
  }
}
axones.forEach(tracerAxone);

// ---------- Dendrites ----------
function pousser(x,y,a,lg,w,d,out){
  const pas=Math.max(3,Math.round(lg/1.7)),pts=[[x,y]];let c=G()*.05;
  for(let i=0;i<pas;i++){c+=G()*.045;a+=c+G()*.11;x+=Math.cos(a)*lg/pas;y+=Math.sin(a)*lg/pas;pts.push([x,y]);}
  const w1=Math.max(.2,w*.58);out.push({pts,w0:w,w1,d});
  if(d<3&&lg>2.2){const nb=R()<.22?3:(R()<.9?2:1),ec=U(.32,.66);
    for(let j=0;j<nb;j++){const o=nb===1?G()*.3:(j/(nb-1)-.5)*2*ec;pousser(x,y,a+o+G()*.08,lg*U(.48,.72),w1*.88,d+1,out);}}
}
const ALPHA=[.56,.42,.3,.21],TEINTE=['214,229,255','170,201,255','132,176,255','110,160,255'];
function tracerNeurone(n){
  const ctx=n.ctx,br=[];
  const a0=R()*TAU;for(let i=0;i<n.k;i++)pousser(0,0,a0+i*TAU/n.k+G()*.28,n.dl*U(.55,1.05),n.s*.95,0,br);
  br.forEach(rm=>{
    const pts=rm.pts.map(q=>L(n.x,n.y,q[0],q[1])),m=pts.length,g=[],dr=[];
    for(let i=0;i<m;i++){const A=pts[Math.max(0,i-1)],B=pts[Math.min(m-1,i+1)];let nx=-(B[1]-A[1]),ny=B[0]-A[0];const l=Math.hypot(nx,ny)||1;nx/=l;ny/=l;const w=(rm.w0+(rm.w1-rm.w0)*i/(m-1))/2;g.push([pts[i][0]+nx*w,pts[i][1]+ny*w]);dr.push([pts[i][0]-nx*w,pts[i][1]-ny*w]);}
    ctx.fillStyle=`rgba(${TEINTE[rm.d]},${(ALPHA[rm.d]*n.b).toFixed(3)})`;
    ctx.beginPath();ctx.moveTo(...g[0]);for(let i=1;i<m;i++)ctx.lineTo(...g[i]);ctx.arc(pts[m-1][0],pts[m-1][1],rm.w1/2,0,TAU);for(let i=m-1;i>=0;i--)ctx.lineTo(...dr[i]);ctx.closePath();ctx.fill();
    // Épines dendritiques
    if(rm.d>=1)for(let i=1;i<m;i++)if(R()<.16){const A=pts[i-1],B=pts[i];let nx=-(B[1]-A[1]),ny=B[0]-A[0];const l=Math.hypot(nx,ny)||1,sg=R()<.5?-1:1,o=rm.w1/2+U(.4,.9);ctx.fillStyle=`rgba(200,222,255,${(.55*n.b).toFixed(3)})`;ctx.beginPath();ctx.arc(B[0]+nx/l*o*sg,B[1]+ny/l*o*sg,.26,0,TAU);ctx.fill();}
  });
  // Corps cellulaire : halo, membrane, noyau
  const s=n.s;
  tache(ctx,n.x,n.y,s*(n.pivot?7:4.6),'49,123,255',(n.pivot?.32:.2)*n.b);
  tache(ctx,n.x,n.y,s*2.2,'156,194,255',.34*n.b);
  ctx.save();ctx.translate(n.x,n.y);ctx.rotate(ROT+R()*.6-.3);ctx.scale(1,U(.78,.95));
  const g=ctx.createRadialGradient(-s*.2,-s*.2,0,0,0,s*1.15);g.addColorStop(0,`rgba(255,255,255,${(.98*n.b).toFixed(3)})`);g.addColorStop(.5,`rgba(214,230,255,${(.85*n.b).toFixed(3)})`);g.addColorStop(1,`rgba(120,170,255,${(.25*n.b).toFixed(3)})`);
  ctx.fillStyle=g;ctx.beginPath();ctx.arc(0,0,s*1.15,0,TAU);ctx.fill();ctx.restore();
  ctx.fillStyle=`rgba(255,255,255,${(.95*n.b).toFixed(3)})`;ctx.beginPath();ctx.arc(n.x,n.y,s*.42,0,TAU);ctx.fill();
}
neurones.slice().sort((a,b)=>a.pres-b.pres).forEach(tracerNeurone);

// ---------- Composition : profondeur de champ, halo lumineux, fondu des bords ----------
const [cBase,base]=toile(),[cFin,fin]=toile();
base.setTransform(1,0,0,1,0,0);fin.setTransform(1,0,0,1,0,0);
base.globalCompositeOperation='lighter';
base.filter='blur(1.6px)';base.globalAlpha=.9;base.drawImage(cLoin,0,0);
base.filter='none';base.globalAlpha=1;base.drawImage(cScene,0,0);
fin.globalCompositeOperation='lighter';
fin.filter='blur(26px)';fin.globalAlpha=.3;fin.drawImage(cBase,0,0);
fin.filter='blur(7px)';fin.globalAlpha=.3;fin.drawImage(cBase,0,0);
fin.filter='blur(1.2px)';fin.globalAlpha=.18;fin.drawImage(cBase,0,0);
fin.filter='none';fin.globalAlpha=1;fin.drawImage(cBase,0,0);
fin.globalCompositeOperation='destination-in';
fin.save();fin.translate(W*S/2,H*S/2);fin.scale(1,H/W);
const m=fin.createRadialGradient(0,0,0,0,0,W*S/2);m.addColorStop(0,'#000');m.addColorStop(.8,'#000');m.addColorStop(1,'rgba(0,0,0,0)');
fin.fillStyle=m;fin.fillRect(-W*S,-W*S,W*S*2,W*S*2);fin.restore();

// Influx animés : quelques axones bien visibles, répartis sur toute la galaxie
const choisis=[];
axones.filter(a=>a.genre!=='long'&&a.ctx===scene&&a.d>48).sort(()=>R()-.5).forEach(a=>{const c=bez(a.p,.5);if(choisis.length<9&&choisis.every(o=>Math.hypot(o.c[0]-c[0],o.c[1]-c[1])>62))choisis.push({a,c});});
const f=v=>v.toFixed(1);
const influx=choisis.map(({a})=>({d:`M${f(a.p[0][0])} ${f(a.p[0][1])}C${f(a.p[1][0])} ${f(a.p[1][1])} ${f(a.p[2][0])} ${f(a.p[2][1])} ${f(a.p[3][0])} ${f(a.p[3][1])}`,l:Math.round(a.d)}));
document.getElementById('o').textContent=JSON.stringify({png:cFin.toDataURL('image/png'),influx,neurones:neurones.length,axones:axones.length});
"""


def svg_influx(influx):
    """Couche animée : un influx parcourt chaque axone choisi, puis s'éteint ; les départs sont décalés."""
    elems = []
    for i, a in enumerate(influx):
        trajet = round(1.6 + a["l"] / 55, 2)
        cycle = round(trajet + 2.4 + (i * 1.37) % 3.2, 2)
        k = round(trajet / cycle, 3)
        debut = round((i * 2.13) % cycle, 2)
        # La tête de l'influx, puis deux points de traînée qui la suivent avec un léger retard
        for j, (halo, point, opa) in enumerate(((8, 1.6, 1), (5, 1.1, .5), (3.5, .8, .25))):
            dep = round(debut + j * .07, 2)
            elems.append(
                f'<g opacity="0"><circle r="{halo}" fill="url(#nlinflux)" opacity="{opa}"/><circle r="{point}" fill="#fff" opacity="{opa}"/>'
                f'<animateMotion path="{a["d"]}" dur="{cycle}s" begin="{dep}s" repeatCount="indefinite" '
                f'keyPoints="0;1;1" keyTimes="0;{k};1" calcMode="spline" keySplines=".4 0 .6 1;0 0 1 1"/>'
                f'<animate attributeName="opacity" values="0;1;1;0;0" keyTimes="0;{round(k * .12, 3)};{round(k * .82, 3)};{k};1" '
                f'dur="{cycle}s" begin="{dep}s" repeatCount="indefinite"/></g>')
    return ('<svg class="nlviz-influx" viewBox="0 0 520 400" width="520" height="400" aria-hidden="true" focusable="false">'
            '<defs><radialGradient id="nlinflux"><stop offset="0" stop-color="#fff" stop-opacity=".95"/>'
            '<stop offset=".3" stop-color="#cfe0ff" stop-opacity=".55"/><stop offset="1" stop-color="#317bff" stop-opacity="0"/>'
            f'</radialGradient></defs>{"".join(elems)}</svg>')


def main():
    page = f'<!doctype html><html><head><meta charset="utf-8"></head><body><pre id="o"></pre><script>{DESSIN}</script></body></html>'
    with tempfile.TemporaryDirectory() as d:
        chemin = os.path.join(d, "v.html")
        open(chemin, "w").write(page)
        sortie = subprocess.run([CHROME, "--headless=new", "--disable-gpu", "--virtual-time-budget=30000", "--dump-dom",
                                 "file://" + chemin], check=True, capture_output=True, text=True).stdout
    brut = re.search(r'<pre id="o">(.*?)</pre>', sortie, re.S)
    if not brut or not brut.group(1).strip():
        raise SystemExit("Le dessin n'a rien renvoyé (erreur JavaScript ?)")
    data = json.loads(html.unescape(brut.group(1)))
    img = Image.open(io.BytesIO(base64.b64decode(data["png"].split(",", 1)[1]))).convert("RGBA")
    img.save(os.path.join(IMG, "lexmachina-reseau.webp"), quality=86, method=6, alpha_quality=90)
    src = os.path.join(ICI, "..", "src", "pages", "lexmachina", "index.html")
    page_src = open(src).read()
    page_src, n = re.subn(r"<!-- influx:debut -->.*?<!-- influx:fin -->",
                          lambda m: "<!-- influx:debut -->" + svg_influx(data["influx"]) + "<!-- influx:fin -->", page_src, flags=re.S)
    if n != 1:
        raise SystemExit("Marqueurs influx introuvables dans la page LexMachina")
    open(src, "w").write(page_src)
    for nom in ("lexmachina-reseau.webp",):
        print(f"écrit : assets/img/{nom} ({os.path.getsize(os.path.join(IMG, nom)) // 1024} Ko)")
    print(f"{data['neurones']} neurones, {data['axones']} axones, {len(data['influx'])} influx animés")


if __name__ == "__main__":
    main()

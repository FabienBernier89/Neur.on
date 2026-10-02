// Boucle exécutée dans l'onglet corrext.com connecté (outil javascript du navigateur intégré).
// Prérequis dans l'onglet : window.__tok() et window.__mt(textes, source, cible), définis comme dans CORREXT-MT.md.
// Elle prend un lot sur le pont local (outils/pont_corrext.py serve <lang>), le traduit avec LexMachina
// et renvoie les traductions au pont. Le jeton reste dans l'onglet.
window.__PONT = { actif: true, lots: 0, erreurs: 0, dernier: null, fin: false };
(async () => {
  const base = "http://localhost:8812";
  const pause = (ms) => new Promise((r) => setTimeout(r, ms));
  const ouvrier = async () => {
    while (window.__PONT.actif) {
      let j;
      try { j = await (await fetch(base + "/lot?n=25")).json(); }
      catch (e) { window.__PONT.erreurs++; window.__PONT.dernier = "pont injoignable"; await pause(5000); continue; }
      if (!j.lot.length) {
        const e = await (await fetch(base + "/etat")).json();
        if (e.faits >= e.total) break;
        await pause(20000); continue;   // segments encore en cours ailleurs : on attend qu'ils reviennent
      }
      let r = null;
      for (let essai = 0; essai < 3 && !r; essai++) {
        const t = await window.__mt(j.lot.map((x) => x.texte), 51, j.cible);
        if (t && t.texts && t.texts.length === j.lot.length) r = t;
        else { window.__PONT.erreurs++; window.__PONT.dernier = t && t.err; await pause(4000 * (essai + 1)); }
      }
      if (!r) continue;   // repris par le pont après 180 s
      await fetch(base + "/resultat", { method: "POST", headers: { "Content-Type": "application/json" },
        body: JSON.stringify(j.lot.map((x, i) => ({ k: x.k, traduction: r.texts[i].text }))) });
      window.__PONT.lots++;
    }
  };
  await Promise.all([ouvrier(), ouvrier()]);
  window.__PONT.fin = true;
})();

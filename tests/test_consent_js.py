"""Le bandeau de consentement s'affiche dans la langue de la page (node, DOM simulé)."""
import os, shutil, subprocess, unittest

DEPOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SIMULATION = r"""
const fs = require('fs'); const code = fs.readFileSync(process.argv[1], 'utf8');
let bandeau = null, lien = null;
const noeud = () => ({ setAttribute(){}, addEventListener(){}, remove(){}, focus(){}, appendChild(){},
  querySelector(){ return { addEventListener(){}, focus(){} }; } });
global.localStorage = { getItem(){ return null; }, setItem(){} };
global.document = {
  readyState: 'complete', documentElement: { lang: process.argv[2] },
  currentScript: { getAttribute: k => k === 'data-ga4' ? 'G-TEST' : null },
  getElementById: () => null,
  querySelector: s => s === '.footer-bottom .links' ? { appendChild: a => { lien = a; } } : null,
  createElement: () => noeud(), head: { appendChild(){} },
  body: { appendChild: b => { bandeau = b; } }, addEventListener(){} };
global.window = global;
new Function(code)();
console.log(JSON.stringify({ bandeau: bandeau && bandeau.innerHTML, lien: lien && lien.textContent }));
"""
ATTENDU = {"fr": ("Refuser", "Préférences cookies"), "de": ("Ablehnen", "Cookie-Einstellungen"),
           "it": ("Rifiutare", "Preferenze cookie"), "en": ("Decline", "Cookie preferences")}


@unittest.skipUnless(shutil.which("node"), "node absent")
class TestConsentement(unittest.TestCase):
    def test_textes_dans_chaque_langue(self):
        js = os.path.join(DEPOT, "assets", "consent.js")
        for lang, (bouton, pref) in ATTENDU.items():
            r = subprocess.run(["node", "-e", SIMULATION, js, lang], capture_output=True, text=True)
            self.assertEqual(r.returncode, 0, f"{lang} : {r.stderr[-400:]}")
            self.assertIn(bouton, r.stdout, lang)
            self.assertIn(pref, r.stdout, lang)


if __name__ == "__main__":
    unittest.main()

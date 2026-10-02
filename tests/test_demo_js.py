"""Le script des démos Corrext s'exécute sans erreur dans chaque langue (node, DOM simulé)."""
import os, shutil, subprocess, unittest

DEPOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SIMULATION = r"""
const fs = require('fs'); const code = fs.readFileSync(process.argv[1], 'utf8');
const el = () => new Proxy(function(){}, {get: (t, k) => k === 'classList' ? {add(){}, remove(){}, toggle(){}, contains(){ return false; }}
  : k === 'options' ? [] : (k === 'style' || k === 'dataset') ? {} : el(), apply: () => el(), set: () => true});
global.document = {documentElement: {lang: process.argv[2]}, getElementById: () => null, querySelector: () => null,
  querySelectorAll: () => [], addEventListener(){}, createElement: () => el()};
global.window = global; global.addEventListener = () => {};
new Function(code)();
"""


@unittest.skipUnless(shutil.which("node"), "node absent")
class TestDemo(unittest.TestCase):
    def test_execution_dans_chaque_langue(self):
        js = os.path.join(DEPOT, "assets", "corrext-demo.js")
        for lang in ("fr", "de", "it", "en"):
            r = subprocess.run(["node", "-e", SIMULATION, js, lang], capture_output=True, text=True)
            self.assertEqual(r.returncode, 0, f"{lang} : {r.stderr[-400:]}")


if __name__ == "__main__":
    unittest.main()

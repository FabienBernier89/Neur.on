"""Build multilingue sur un mini-site temporaire : une page FR, sa traduction DE, un lien entre elles."""
import json, os, shutil, subprocess, sys, tempfile, unittest

DEPOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

FR_ACCUEIL = """<!--page
title: Accueil de test · Neur.on
description: Page d'accueil de test du site Neur.on, pour vérifier la construction multilingue des pages.
short: Accueil
-->
<section><h1>Bienvenue</h1><p><a href="{{ROOT}}fr/traduction/">Traduction</a></p></section>"""
FR_TRAD = """<!--page
title: Traduction juridique · Neur.on
description: Page de test sur la traduction juridique, pour vérifier les liens localisés et les alternates hreflang.
short: Traduction
canonical: https://neur-on.ai/fr/traduction/
-->
<section><h1>Traduction</h1><p><a href="{{ROOT}}fr/">Accueil</a></p></section>"""
DE_ACCUEIL = FR_ACCUEIL.replace("Bienvenue", "Willkommen").replace("Accueil de test", "Startseite Test")
DE_TRAD = FR_TRAD.replace("<h1>Traduction</h1>", "<h1>Übersetzung</h1>").replace("Traduction juridique ·", "Juristische Übersetzung ·")


def mini_site():
    d = tempfile.mkdtemp()
    shutil.copy(os.path.join(DEPOT, "build.py"), d)
    shutil.copytree(os.path.join(DEPOT, "assets"), os.path.join(d, "assets"))
    os.makedirs(os.path.join(d, "src", "data"))
    for f in ("langues.py", "i18n.py"):
        shutil.copy(os.path.join(DEPOT, "src", f), os.path.join(d, "src", f))
    shutil.copytree(os.path.join(DEPOT, "src", "partials"), os.path.join(d, "src", "partials"))
    for f in ("organisation.json", "fedlex.json"):
        shutil.copy(os.path.join(DEPOT, "src", "data", f), os.path.join(d, "src", "data", f))
    for rel, txt in (("src/pages/index.html", FR_ACCUEIL), ("src/pages/traduction/index.html", FR_TRAD),
                     ("src/langues/de/pages/index.html", DE_ACCUEIL),
                     ("src/langues/de/pages/traduction/index.html", DE_TRAD)):
        os.makedirs(os.path.dirname(os.path.join(d, rel)), exist_ok=True)
        open(os.path.join(d, rel), "w", encoding="utf-8").write(txt)
    json.dump({"fr/": {"de": "de/"}, "fr/traduction/": {"de": "de/uebersetzung/"}},
              open(os.path.join(d, "src", "routes.json"), "w"))
    cles = json.load(open(os.path.join(DEPOT, "src", "i18n", "cles.json"), encoding="utf-8"))
    os.makedirs(os.path.join(d, "src", "i18n"))
    json.dump({k: "[de] " + k for k in cles}, open(os.path.join(d, "src", "i18n", "de.json"), "w", encoding="utf-8"),
              ensure_ascii=False)
    return d


def construire(d):
    return subprocess.run([sys.executable, os.path.join(d, "build.py")], env={**os.environ, "NEURON_BASE": d},
                          capture_output=True, text=True)


class TestBuildMultilingue(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.d = mini_site()
        cls.r = construire(cls.d)
        lire = lambda rel: open(os.path.join(cls.d, "docs", rel), encoding="utf-8").read()
        cls.lire = staticmethod(lire)

    def test_build_reussit(self):
        self.assertEqual(self.r.returncode, 0, self.r.stdout + self.r.stderr)

    def test_page_de_a_son_adresse(self):
        h = self.lire("de/uebersetzung/index.html")
        self.assertIn('<html lang="de">', h)
        self.assertIn("Übersetzung", h)
        self.assertIn('<meta property="og:locale" content="de_CH">', h)

    def test_hreflang_reciproques(self):
        de, fr = self.lire("de/uebersetzung/index.html"), self.lire("fr/traduction/index.html")
        for h in (de, fr):
            self.assertIn('hreflang="fr-CH" href="https://neur-on.ai/fr/traduction/"', h)
            self.assertIn('hreflang="de-CH" href="https://neur-on.ai/de/uebersetzung/"', h)
            self.assertIn('hreflang="x-default" href="https://neur-on.ai/"', h)

    def test_canonical_dans_la_langue(self):
        # le canonical du front-matter FR, recopié dans la traduction, ne doit pas pointer vers la page FR
        self.assertIn('<link rel="canonical" href="https://neur-on.ai/de/uebersetzung/">', self.lire("de/uebersetzung/index.html"))
        self.assertIn('<link rel="canonical" href="https://neur-on.ai/fr/traduction/">', self.lire("fr/traduction/index.html"))

    def test_lien_localise(self):
        self.assertIn('href="../../de/"', self.lire("de/uebersetzung/index.html"))
        self.assertIn('href="../de/uebersetzung/"', self.lire("de/index.html"))

    def test_selecteur_vers_la_meme_page(self):
        fr = self.lire("fr/traduction/index.html")
        self.assertIn('<a href="../../de/uebersetzung/">DE</a>', fr)
        self.assertIn('<a class="on" href="../../fr/traduction/" aria-current="true">FR</a>', fr)

    def test_sitemap_alternates(self):
        sm = self.lire("sitemap.xml")
        self.assertIn("<loc>https://neur-on.ai/de/uebersetzung/</loc>", sm)
        self.assertIn('<xhtml:link rel="alternate" hreflang="de-CH" href="https://neur-on.ai/de/uebersetzung/"/>', sm)

    def test_cle_manquante_fait_echouer(self):
        d = mini_site()
        p = os.path.join(d, "src", "i18n", "de.json")
        dico = json.load(open(p, encoding="utf-8"))
        dico.pop("Accueil")
        json.dump(dico, open(p, "w", encoding="utf-8"), ensure_ascii=False)
        r = construire(d)
        self.assertNotEqual(r.returncode, 0)
        self.assertIn("Accueil", r.stdout + r.stderr)


if __name__ == "__main__":
    unittest.main()

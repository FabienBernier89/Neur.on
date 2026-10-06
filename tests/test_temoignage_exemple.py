"""Témoignages d'exemple : signalés « Exemple de cas d'usage » à l'écran, sans attribution à une personne.

La garde de production ne bloque plus que les exemples non signalés.
"""
import sys, os, tempfile, unittest
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
import i18n, generators, build

EXEMPLE = {"exemple": True, "citation": "Quatre cents pages de pièces sont arrivées.",
           "auteur": "Associée, département contentieux", "fonction": "Cabinet d'affaires, Genève"}
REEL = {"citation": "Une vraie citation.", "auteur": "Prénom Nom", "fonction": "Associé, cabinet X"}


class TestTemoignageExemple(unittest.TestCase):
    def setUp(self):
        i18n.activer("fr", tempfile.mkdtemp())

    def test_exemple_signale_sans_attribution(self):
        html = generators.temoignage(EXEMPLE)
        self.assertIn('class="temo temo-ex"', html)
        self.assertIn('<span class="temo-lab">Exemple de cas d\'usage</span>', html)
        self.assertNotIn(EXEMPLE["auteur"], html)
        self.assertNotIn(EXEMPLE["fonction"], html)
        self.assertIn(EXEMPLE["citation"], html)

    def test_temoignage_reel_garde_son_attribution(self):
        html = generators.temoignage(REEL)
        self.assertNotIn("temo-ex", html)
        self.assertNotIn("temo-lab", html)
        self.assertIn(REEL["auteur"], html)

    def test_garde_production(self):
        self.assertFalse(build.exemple_non_signale(generators.temoignage(EXEMPLE)))
        self.assertFalse(build.exemple_non_signale(generators.temoignage(REEL)))
        sans_mention = '<section class="temo temo-ex"><figure><blockquote><p>x</p></blockquote></figure></section>'
        self.assertTrue(build.exemple_non_signale(sans_mention))


if __name__ == "__main__":
    unittest.main()

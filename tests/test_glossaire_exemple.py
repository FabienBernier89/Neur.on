"""Fiche du glossaire : la citation officielle s'affiche en allemand et dans la langue de la page."""
import sys, os, tempfile, unittest
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
import i18n, generators


class TestLangueExemple(unittest.TestCase):
    def choix(self, lang, ex):
        i18n.activer(lang, tempfile.mkdtemp())
        return generators.langue_exemple(ex)

    def test_page_fr_et_de_avec_le_francais(self):
        ex = {"de": "a", "fr": "b", "it": "c", "en": "d"}
        self.assertEqual(self.choix("fr", ex), "fr")
        self.assertEqual(self.choix("de", ex), "fr")

    def test_page_it_et_en_dans_leur_langue(self):
        ex = {"de": "a", "fr": "b", "it": "c", "en": "d"}
        self.assertEqual(self.choix("it", ex), "it")
        self.assertEqual(self.choix("en", ex), "en")

    def test_sans_version_anglaise_le_francais(self):
        self.assertEqual(self.choix("en", {"de": "a", "fr": "b", "it": "c"}), "fr")


if __name__ == "__main__":
    unittest.main()

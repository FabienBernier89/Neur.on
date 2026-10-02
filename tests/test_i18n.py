import sys, os, json, tempfile, unittest
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
import i18n


class TestT(unittest.TestCase):
    def setUp(self):
        self.d = tempfile.mkdtemp()
        json.dump({"Autres domaines": "Weitere Rechtsgebiete"}, open(os.path.join(self.d, "de.json"), "w"))

    def test_fr_identite(self):
        i18n.activer("fr", self.d)
        self.assertEqual(i18n.T("Autres domaines"), "Autres domaines")

    def test_de_traduit(self):
        i18n.activer("de", self.d)
        self.assertEqual(i18n.T("Autres domaines"), "Weitere Rechtsgebiete")

    def test_cle_absente_notee(self):
        i18n.activer("de", self.d)
        i18n.T("Par métier")
        self.assertIn("Par métier", i18n.MANQUANTS)

    def test_dates(self):
        i18n.activer("de", self.d); self.assertEqual(i18n.date_longue("2024-06-04"), "4. Juni 2024")
        i18n.activer("it", self.d); self.assertEqual(i18n.date_longue("2024-06-04"), "4 giugno 2024")
        i18n.activer("en", self.d); self.assertEqual(i18n.date_longue("2024-06-04"), "4 June 2024")
        i18n.activer("fr", self.d); self.assertEqual(i18n.date_longue("2024-06-01"), "1er juin 2024")


if __name__ == "__main__":
    unittest.main()

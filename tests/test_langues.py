import sys, os, unittest
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
from langues import Routes, localiser, alternates

TABLE = {"fr/": {"de": "de/", "it": "it/", "en": "en/"},
         "fr/traduction/contrats/": {"de": "de/uebersetzung/vertraege/", "it": "it/traduzione/contratti/",
                                     "en": "en/translation/contracts/"}}


class TestRoutes(unittest.TestCase):
    def test_fr_est_l_identite(self):
        self.assertEqual(Routes(TABLE).chemin("fr/traduction/contrats/", "fr"), "fr/traduction/contrats/")

    def test_chemin_traduit(self):
        self.assertEqual(Routes(TABLE).chemin("fr/traduction/contrats/", "de"), "de/uebersetzung/vertraege/")

    def test_chemin_absent(self):
        self.assertIsNone(Routes(TABLE).chemin("fr/inconnu/", "de"))


class TestLocaliser(unittest.TestCase):
    def test_lien_root_et_absolu(self):
        h = '<a href="{{ROOT}}fr/traduction/contrats/#faits">x</a> https://neur-on.ai/fr/traduction/contrats/'
        out, manquants = localiser(h, "de", Routes(TABLE), {"fr/traduction/contrats/"}, "https://neur-on.ai")
        self.assertIn('href="{{ROOT}}de/uebersetzung/vertraege/#faits"', out)
        self.assertIn("https://neur-on.ai/de/uebersetzung/vertraege/", out)
        self.assertEqual(manquants, set())

    def test_page_absente_garde_le_fr(self):
        out, manquants = localiser('<a href="{{ROOT}}fr/contact/">c</a>', "de", Routes(TABLE), set(), "https://neur-on.ai")
        self.assertIn("{{ROOT}}fr/contact/", out)
        self.assertEqual(manquants, {"fr/contact/"})

    def test_assets_intacts(self):
        h = '<img src="{{ROOT}}assets/img/a.webp">'
        self.assertEqual(localiser(h, "de", Routes(TABLE), set(), "https://neur-on.ai")[0], h)

    def test_fr_inchange(self):
        h = '<a href="{{ROOT}}fr/traduction/contrats/">x</a>'
        self.assertEqual(localiser(h, "fr", Routes(TABLE), set(), "https://neur-on.ai")[0], h)


class TestAlternates(unittest.TestCase):
    def test_reciproques_et_x_default(self):
        dispo = {"fr": {"fr/traduction/contrats/"}, "de": {"fr/traduction/contrats/"}, "it": set(), "en": set()}
        alt = alternates("fr/traduction/contrats/", dispo, Routes(TABLE), "https://neur-on.ai")
        self.assertEqual(alt, [("fr-CH", "https://neur-on.ai/fr/traduction/contrats/"),
                               ("de-CH", "https://neur-on.ai/de/uebersetzung/vertraege/"),
                               ("x-default", "https://neur-on.ai/")])

    def test_une_seule_langue_pas_d_alternate(self):
        dispo = {"fr": {"fr/x/"}, "de": set(), "it": set(), "en": set()}
        self.assertEqual(alternates("fr/x/", dispo, Routes(TABLE), "https://neur-on.ai"), [])


if __name__ == "__main__":
    unittest.main()

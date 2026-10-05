"""Bloc « situations » en liste éditoriale (remplace la grille de trois cartes identiques).

Chaque scénario devient une ligne : contexte (pictogramme + libellé), situation en titre, explication.
Les textes ne changent pas : seule la présentation est nouvelle.
"""
import sys, os, tempfile, unittest
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
import i18n, generators

ITEMS = [
    {"vis": "lot", "a": "Contentieux", "t": "400 pages de pièces avant l'audience", "p": "Le lot part en File translation."},
    {"vis": "pret", "a": "Transactions", "t": "Un contrat de prêt à livrer demain matin", "p": "Traduction machine le soir."},
    {"vis": "sentence", "a": "Arbitrage", "t": "Une sentence à citer au mot près", "p": "Les alternatives par moteur."},
]


class TestScenariosListe(unittest.TestCase):
    def setUp(self):
        i18n.activer("fr", tempfile.mkdtemp())

    def test_liste_sans_cartes(self):
        html = generators.who("Trois moments", ITEMS)
        self.assertIn('class="sc-list"', html)
        self.assertNotIn("ws-grid", html)
        self.assertNotIn("ws-item", html)
        self.assertEqual(html.count('class="sc-row"'), 3)

    def test_chaque_ligne_garde_ses_trois_textes(self):
        html = generators.who("Trois moments", ITEMS)
        for w in ITEMS:
            self.assertIn(f'<span class="sc-a">{w["a"]}</span>', html)
            self.assertIn(f"<h3>{w['t']}</h3>", html)
            self.assertIn(f"<p>{w['p']}</p>", html)

    def test_pictogramme_decoratif(self):
        html = generators.who("Trois moments", ITEMS)
        self.assertEqual(html.count('class="ws-ic" aria-hidden="true"'), 3)

    def test_liens_metiers_sous_la_liste(self):
        html = generators.who("Trois moments", ITEMS, ["cabinets-avocats"])
        self.assertIn('class="ws-metiers"', html)
        self.assertIn("fr/solutions/cabinets-avocats/", html)


if __name__ == "__main__":
    unittest.main()

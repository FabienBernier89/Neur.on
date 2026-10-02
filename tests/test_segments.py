import sys, os, unittest
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "outils"))
import segments as S

PAGE = """<!--page
title: Mentions légales · Neur.on
description: Les mentions légales du site.
short: Mentions
nav:
-->
<!-- commentaire interne -->
<section class="legal"><h1>Mentions <em>légales</em></h1>
<p>Consultez la <a href="{{ROOT}}fr/protection-des-donnees/">politique de protection</a> avant d'envoyer le formulaire.<br>Merci.</p>
<img src="{{ROOT}}assets/img/a.webp" alt="Logo de Neur.on">
<style>.x{color:red}</style><script>var t='Analyse en cours';</script>
<svg><text x="1">Texte du schéma</text></svg>
<div>{{ICONE:bouclier}}</div>
<p>12'000</p>
</section>"""


class TestProteger(unittest.TestCase):
    def test_aller_retour(self):
        h = 'Consultez la <a href="x">politique</a> et le <strong>formulaire</strong>.<br>Fin {{ICONE:a}}.'
        t, table = S.proteger(h)
        self.assertEqual(t, "Consultez la {1}politique{/1} et le {2}formulaire{/2}.{3}Fin {4}.")
        self.assertEqual(S.restaurer(t, table), h)

    def test_espaces_ajoutees_par_le_moteur(self):
        t, table = S.proteger('la <a href="x">politique</a> ici')
        self.assertEqual(S.restaurer("die {1} Erklärung {/1} hier", table), 'die <a href="x">Erklärung</a> hier')

    def test_marqueur_manquant(self):
        t, table = S.proteger('la <a href="x">politique</a> ici')
        with self.assertRaises(ValueError):
            S.restaurer("die Erklärung {/1} hier", table)

    def test_marqueur_double(self):
        t, table = S.proteger('la <a href="x">politique</a> ici')
        with self.assertRaises(ValueError):
            S.restaurer("{1}a{/1} {1}b{/1}", table)

    def test_emplacements_de_gabarit(self):
        t, table = S.proteger("{0} actualités depuis {1}")
        self.assertEqual(t, "{1} actualités depuis {2}")
        self.assertEqual(S.restaurer("{1} Meldungen seit {2}", table), "{0} Meldungen seit {1}")

    def test_entites(self):
        t, table = S.proteger("Tarif&nbsp;: 1 &amp; 2")
        self.assertEqual(t, "Tarif : 1 & 2")
        self.assertEqual(S.restaurer("Preis: 1 & 2", table), "Preis: 1 &amp; 2")


class TestHtml(unittest.TestCase):
    def test_extraction(self):
        unites = S.extraire_html(PAGE)
        textes = [u["texte"] for u in unites]
        self.assertIn("Mentions légales · Neur.on", textes)
        self.assertIn("Les mentions légales du site.", textes)
        self.assertIn("Mentions {1}légales{/1}", textes)
        self.assertIn("Consultez la {1}politique de protection{/1} avant d'envoyer le formulaire.{2}Merci.", textes)
        self.assertIn("Logo de Neur.on", textes)
        self.assertIn("Texte du schéma", textes)
        self.assertNotIn("Analyse en cours", " ".join(textes))
        self.assertNotIn("commentaire interne", " ".join(textes))
        self.assertNotIn("12'000", textes)
        self.assertNotIn("{1}", [u["texte"] for u in unites if u["html"].strip() == "{{ICONE:bouclier}}"])

    def test_reinjection(self):
        unites = S.extraire_html(PAGE)
        trad = {u["id"]: u["html"].upper() if u["genre"] != "bloc" else u["html"].replace("Consultez", "Konsultieren")
                for u in unites}
        out = S.reinjecter_html(PAGE, trad)
        self.assertIn("title: MENTIONS LÉGALES · NEUR.ON", out)
        self.assertIn('alt="LOGO DE NEUR.ON"', out)
        self.assertIn("<p>Konsultieren la <a href=\"{{ROOT}}fr/protection-des-donnees/\">", out)
        self.assertIn("<script>var t='Analyse en cours';</script>", out)
        self.assertIn("<!-- commentaire interne -->", out)

    def test_script_signale(self):
        self.assertTrue(S.scripts_a_traduire(PAGE))


class TestJson(unittest.TestCase):
    def test_extraction_et_reinjection(self):
        data = [{"slug": "kuendigung", "de": "Kündigung", "fr": "résiliation", "titre": "La <b>résiliation</b>",
                 "termes": [{"de": "Kündigung", "fr": "résiliation", "ref": "art. 335 CO"}],
                 "faq": [{"q": "Pourquoi ?", "r": "Parce que."}], "href": "fr/x/", "w": 12}]
        unites = S.extraire_json(data, "glossaire.json")
        textes = sorted(u["texte"] for u in unites)
        self.assertEqual(textes, sorted(["La {1}résiliation{/1}", "art. 335 CO", "Pourquoi ?", "Parce que."]))
        trad = {u["id"]: "X" for u in unites}
        out = S.reinjecter_json(data, trad)
        self.assertEqual(out[0]["slug"], "kuendigung")
        self.assertEqual(out[0]["de"], "Kündigung")
        self.assertEqual(out[0]["faq"][0]["q"], "X")
        self.assertEqual(out[0]["termes"][0]["fr"], "résiliation")


if __name__ == "__main__":
    unittest.main()

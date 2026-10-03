"""Tests du contrôle automatique des traductions (outils/controle_traductions.py).
Chaque test part d'un petit dépôt factice, conforme, créé dans un dossier temporaire, puis y introduit une faute."""
import contextlib, io, json, os, shutil, sys, tempfile, unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "outils"))
import controle_traductions as C  # noqa: E402

PAGE_FR = """<!--page
title: À propos de Neur.on · la société suisse derrière Corrext
description: Neur.on AI Solutions SA, société suisse établie à Fribourg : nos distinctions, notre certification et nos modèles juridiques.
short: À propos
nav: a-propos
-->
<!-- Commentaire interne : nous gardons ce bloc pour la page de presse et pour les annonces des partenaires -->
<section class="hero"><h1>Neur.on, une société <em>suisse</em></h1>
<p>Nous développons LexMachina et Corrext pour les juristes qui traduisent des contrats, des jugements et des extraits du registre du commerce.</p>
<p>Consultez la <a href="{{ROOT}}fr/corrext/">page Corrext</a> pour en savoir plus.</p>
<img src="{{ROOT}}assets/img/equipe.webp" alt="L'équipe de Neur.on à Fribourg">
{{ICONE:bouclier}}
<script>document.body.dataset.n = "3";</script>
</section>
"""

PAGE_DE = """<!--page
title: Über Neur.on · das Schweizer Unternehmen hinter Corrext
description: Neur.on AI Solutions SA, ein Schweizer Unternehmen mit Sitz in Freiburg: unsere Auszeichnungen, unsere Zertifizierung und unsere Rechtsmodelle.
short: Über uns
nav: a-propos
-->
<!-- Commentaire interne : nous gardons ce bloc pour la page de presse et pour les annonces des partenaires -->
<section class="hero"><h1>Neur.on, ein <em>Schweizer</em> Unternehmen</h1>
<p>Wir entwickeln LexMachina und Corrext für Juristinnen und Juristen, die Verträge, Urteile und Auszüge aus dem Handelsregister übersetzen.</p>
<p>Besuchen Sie die <a href="{{ROOT}}fr/corrext/">Seite zu Corrext</a>, um mehr zu erfahren.</p>
<img src="{{ROOT}}assets/img/equipe.webp" alt="Das Team von Neur.on in Freiburg">
{{ICONE:bouclier}}
<script>document.body.dataset.n = "3";</script>
</section>
"""

GLOSSAIRE_FR = [{
    "slug": "kuendigung", "de": "Kündigung", "fr": "résiliation",
    "exemple": "Le contrat peut être résilié pour la fin d'un mois avec un préavis de trois mois, selon les règles du code.",
    "title": "Kündigung : la résiliation du contrat en droit suisse",
    "description": "La résiliation met fin au contrat pour l'avenir : délai, forme et effets en droit suisse, avec un exemple tiré du Code des obligations.",
    "definition": "La résiliation met fin au contrat pour l'avenir. Elle est soumise à un délai et à une forme.",
    "faq": [{"q": "Quand résilier ?", "r": "Avant la fin du délai, voir <a href=\"{{ROOT}}fr/ressources/glossaire/\">le glossaire</a>."}],
}]

GLOSSAIRE_DE = [{
    "slug": "kuendigung", "de": "Kündigung", "fr": "résiliation",
    "exemple": "Le contrat peut être résilié pour la fin d'un mois avec un préavis de trois mois, selon les règles du code.",
    "title": "Kündigung: die Beendigung eines Vertrags im Schweizer Recht",
    "description": "Die Kündigung beendet einen Vertrag für die Zukunft. Frist, Form und Wirkung nach Schweizer Recht, mit Beispiel aus dem Obligationenrecht.",
    "definition": "Die Kündigung beendet den Vertrag für die Zukunft. Sie unterliegt einer Frist und einer Form.",
    "faq": [{"q": "Wann kündigen?", "r": "Vor Ablauf der Frist, siehe <a href=\"{{ROOT}}fr/ressources/glossaire/\">das Glossar</a>."}],
}]

NAV_FR = '<nav><a href="{{ROOT}}fr/">Accueil</a> <a href="{{ROOT}}fr/corrext/">Corrext</a>{{LANGUES}}</nav>\n'
NAV_DE = '<nav><a href="{{ROOT}}fr/">Startseite</a> <a href="{{ROOT}}fr/corrext/">Corrext</a>{{LANGUES}}</nav>\n'
FOOTER_FR = "<footer><p>© 2026 Neur.on AI Solutions SA · Fribourg</p></footer>\n"
FOOTER_DE = "<footer><p>© 2026 Neur.on AI Solutions SA · Freiburg</p></footer>\n"
CLES = ["Accueil", "{0} actualités", "Lire la suite"]
I18N_DE = {"Accueil": "Startseite", "{0} actualités": "{0} Meldungen", "Lire la suite": "Weiterlesen"}
TERMES_DE = [{"fr": "registre du commerce", "de": "Handelsregister"}]

PAGE = "src/langues/de/pages/a-propos/index.html"
GLOSS = "src/langues/de/data/glossaire.json"


class Base(unittest.TestCase):
    """Dépôt factice : une page, un JSON de données, les deux partiels, le dictionnaire d'interface et les termes."""

    def setUp(self):
        self.base = tempfile.mkdtemp()
        self.addCleanup(shutil.rmtree, self.base)
        fr = {"src/pages/a-propos/index.html": PAGE_FR, "src/data/glossaire.json": GLOSSAIRE_FR,
              "src/data/redirections.json": {"redirections": [{"ancien": "/x", "nouveau": "fr/"}]},
              "src/partials/nav.html": NAV_FR, "src/partials/footer.html": FOOTER_FR,
              "src/partials/404.html": "<p>Page introuvable</p>", "src/i18n/cles.json": CLES}
        de = {PAGE: PAGE_DE, GLOSS: GLOSSAIRE_DE, "src/langues/de/partials/nav.html": NAV_DE,
              "src/langues/de/partials/footer.html": FOOTER_DE, "src/i18n/de.json": I18N_DE,
              "src/i18n/termes-de.json": TERMES_DE, "src/langues/de/brut/a_traduire.json": {"a1": "Texte brut"}}
        for rel, contenu in {**fr, **de}.items():
            self.ecrire(rel, contenu)

    def ecrire(self, rel, contenu):
        p = os.path.join(self.base, rel)
        os.makedirs(os.path.dirname(p), exist_ok=True)
        with open(p, "w", encoding="utf-8") as f:
            if isinstance(contenu, str):
                f.write(contenu)
            else:
                json.dump(contenu, f, ensure_ascii=False, indent=1)

    def lire(self, rel):
        with open(os.path.join(self.base, rel), encoding="utf-8") as f:
            return f.read()

    def remplacer(self, rel, ancien, nouveau):
        t = self.lire(rel)
        self.assertIn(ancien, t, f"{ancien!r} absent de {rel}")
        self.ecrire(rel, t.replace(ancien, nouveau))

    def glossaire(self, **champs):
        g = json.loads(json.dumps(GLOSSAIRE_DE))
        g[0].update(champs)
        self.ecrire(GLOSS, g)
        return g

    def controle(self, lang="de", **kw):
        return C.controler(lang, base=self.base, **kw)

    def regle(self, regle, lang="de", **kw):
        return [p for p in self.controle(lang, **kw) if p["regle"] == regle]

    def assertBloquant(self, regle, fichier=None, contient=None):
        pbs = [p for p in self.regle(regle) if p["gravite"] == "bloquant"]
        self.assertTrue(pbs, f"aucun bloquant « {regle} » ; rapport : {self.controle()}")
        if fichier:
            self.assertTrue(any(p["fichier"] == fichier for p in pbs), pbs)
        if contient:
            self.assertTrue(any(contient in p["detail"] for p in pbs), pbs)
        return pbs


class TestConforme(Base):
    def test_champs_du_rapport(self):
        self.remplacer(PAGE, "übersetzen.", "übersetzen\u2014.")
        p = self.controle()[0]
        self.assertEqual(set(p), {"fichier", "gravite", "regle", "detail"})
        self.assertIn(p["gravite"], ("bloquant", "avertissement"))

    def test_depot_conforme_sans_probleme(self):
        self.assertEqual(self.controle(), [])

    def test_langue_non_commencee(self):
        shutil.rmtree(os.path.join(self.base, "src/langues/de/pages"))
        shutil.rmtree(os.path.join(self.base, "src/langues/de/data"))
        shutil.rmtree(os.path.join(self.base, "src/langues/de/partials"))
        os.remove(os.path.join(self.base, "src/i18n/de.json"))
        self.assertEqual(self.controle(), [])

    def test_francais_refuse(self):
        with self.assertRaises(ValueError):
            C.controler("fr", base=self.base)

    def test_statut_de_traduction_tolere(self):
        self.remplacer(PAGE, "nav: a-propos", "nav: a-propos\nstatut_traduction: brouillon")
        self.assertEqual(self.controle(), [])

    def test_donnees_non_traduites_tolerees(self):
        self.ecrire("src/langues/de/data/redirections.json", {"redirections": [{"ancien": "/x", "nouveau": "fr/"}]})
        self.assertEqual(self.controle(), [])


class TestStructure(Base):
    def test_cle_json_absente(self):
        g = json.loads(json.dumps(GLOSSAIRE_DE))
        del g[0]["faq"]
        self.ecrire(GLOSS, g)
        self.assertBloquant("structure", GLOSS, "faq")

    def test_cle_json_en_trop(self):
        self.glossaire(note="Zusatz")
        self.assertBloquant("structure", GLOSS, "note")

    def test_longueur_de_liste(self):
        self.glossaire(faq=GLOSSAIRE_DE[0]["faq"] * 2)
        self.assertBloquant("structure", GLOSS, "faq")

    def test_valeur_technique_modifiee(self):
        self.glossaire(slug="kundigung")
        self.assertBloquant("structure", GLOSS, "slug")

    def test_equivalent_du_glossaire_modifie(self):
        self.glossaire(fr="la résiliation")
        self.assertBloquant("structure", GLOSS, "fr")

    def test_code_de_symbole_modifie(self):
        fr = json.loads(json.dumps(GLOSSAIRE_FR))
        fr[0]["cellule"] = "y:En Suisse, toujours"
        self.ecrire("src/data/glossaire.json", fr)
        self.glossaire(cellule="Immer y:In der Schweiz")
        self.assertBloquant("structure", GLOSS, "cellule")

    def test_json_invalide(self):
        self.ecrire(GLOSS, '[{"slug": "kuendigung",')
        self.assertBloquant("structure", GLOSS)

    def test_fichier_manquant(self):
        os.remove(os.path.join(self.base, PAGE))
        self.assertBloquant("structure", PAGE, "manquant")

    def test_partiel_manquant(self):
        os.remove(os.path.join(self.base, "src/langues/de/partials/footer.html"))
        self.assertBloquant("structure", "src/langues/de/partials/footer.html", "manquant")

    def test_fichier_en_trop(self):
        self.ecrire("src/langues/de/pages/inexistante/index.html", PAGE_DE)
        self.assertBloquant("structure", "src/langues/de/pages/inexistante/index.html", "en trop")

    def test_front_matter_technique_modifie(self):
        self.remplacer(PAGE, "nav: a-propos", "nav: ueber-uns")
        self.assertBloquant("structure", PAGE, "nav")

    def test_cle_d_interface_absente(self):
        d = dict(I18N_DE)
        del d["Lire la suite"]
        self.ecrire("src/i18n/de.json", d)
        self.assertBloquant("structure", "src/i18n/de.json", "Lire la suite")

    def test_cle_d_interface_en_trop_avertit(self):
        self.ecrire("src/i18n/de.json", {**I18N_DE, "Ancienne clé": "Alter Schlüssel"})
        pbs = self.regle("structure")
        self.assertTrue(pbs)
        self.assertEqual({p["gravite"] for p in pbs}, {"avertissement"})


class TestBalises(Base):
    def test_balise_supprimee(self):
        self.remplacer(PAGE, "<em>Schweizer</em>", "Schweizer")
        self.assertBloquant("balises", PAGE)

    def test_retour_a_la_ligne_admis(self):
        # un <br> ne change ni la structure ni les liens : chaque langue coupe ses titres où elle veut
        self.remplacer(PAGE, "<h1>Neur.on, ein <em>Schweizer</em> Unternehmen</h1>",
                       "<h1>Neur.on,<br>ein <em>Schweizer</em> Unternehmen</h1>")
        self.assertFalse([p for p in self.regle("balises") if p["gravite"] == "bloquant"])

    def test_lien_interne_localise_refuse(self):
        self.remplacer(PAGE, 'href="{{ROOT}}fr/corrext/"', 'href="{{ROOT}}de/corrext/"')
        self.assertBloquant("balises", PAGE, "fr/corrext/")

    def test_src_modifie(self):
        self.remplacer(PAGE, "equipe.webp", "team.webp")
        self.assertBloquant("balises", PAGE, "equipe.webp")

    def test_jeton_supprime(self):
        self.remplacer(PAGE, "{{ICONE:bouclier}}", "")
        self.assertBloquant("balises", PAGE, "{{ICONE:bouclier}}")

    def test_attributs_lisibles_traduits(self):
        self.remplacer(PAGE, 'alt="Das Team von Neur.on in Freiburg"',
                       'alt="Das Team von Neur.on in Freiburg" title="Unser Team"')
        self.remplacer("src/pages/a-propos/index.html", 'alt="L\'équipe de Neur.on à Fribourg"',
                       'alt="L\'équipe de Neur.on à Fribourg" title="Notre équipe"')
        self.assertEqual(self.controle(), [])

    def test_script_modifie_avertit(self):
        self.remplacer(PAGE, 'dataset.n = "3"', 'dataset.n = "4"')
        pbs = self.regle("balises")
        self.assertTrue(pbs)
        self.assertEqual({p["gravite"] for p in pbs}, {"avertissement"})
        self.assertIn("script modifié", pbs[0]["detail"])

    def test_script_contenant_du_francais_avertit(self):
        script = "<script>var etat = 'Analyse en cours de la page';</script>"
        self.remplacer("src/pages/a-propos/index.html", '<script>document.body.dataset.n = "3";</script>', script)
        self.remplacer(PAGE, '<script>document.body.dataset.n = "3";</script>', script)
        pbs = self.regle("balises")
        self.assertTrue(pbs)
        self.assertEqual({p["gravite"] for p in pbs}, {"avertissement"})
        self.assertIn("script contenant du français", pbs[0]["detail"])

    def test_balise_supprimee_dans_un_json(self):
        g = json.loads(json.dumps(GLOSSAIRE_DE))
        g[0]["faq"][0]["r"] = "Vor Ablauf der Frist, siehe das Glossar."
        self.ecrire(GLOSS, g)
        self.assertBloquant("balises", GLOSS, "faq")

    def test_emplacement_de_gabarit_perdu(self):
        self.ecrire("src/i18n/de.json", {**I18N_DE, "{0} actualités": "Meldungen"})
        self.assertBloquant("balises", "src/i18n/de.json", "{0}")

    def test_partiel_compare(self):
        self.remplacer("src/langues/de/partials/nav.html", "{{LANGUES}}", "")
        self.assertBloquant("balises", "src/langues/de/partials/nav.html", "{{LANGUES}}")


class TestRestesFr(Base):
    PHRASE_FR = ("Nous développons LexMachina et Corrext pour les juristes qui traduisent des contrats, "
                 "des jugements et des extraits du registre du commerce.")

    def test_paragraphe_non_traduit(self):
        self.remplacer(PAGE, "Wir entwickeln LexMachina und Corrext für Juristinnen und Juristen, die Verträge, "
                             "Urteile und Auszüge aus dem Handelsregister übersetzen.", self.PHRASE_FR + " Handelsregister")
        self.assertBloquant("restes_fr", PAGE)

    def test_texte_court_tolere(self):
        self.remplacer(PAGE, "<h1>Neur.on, ein <em>Schweizer</em> Unternehmen</h1>",
                       "<h1>Neur.on, une société <em>suisse</em></h1>")
        self.assertEqual(self.regle("restes_fr"), [])

    def test_citation_marquee_lang_fr_ignoree(self):
        citation = ('<blockquote lang="fr"><p>Le débiteur en demeure doit des intérêts moratoires au taux de cinq '
                    'pour cent l\'an, selon les règles du code et pour la durée du retard.</p></blockquote>\n</section>')
        self.remplacer("src/pages/a-propos/index.html", "</section>", citation)
        self.remplacer(PAGE, "</section>", citation)
        self.assertEqual(self.controle(), [])

    def test_commentaire_et_valeur_technique_ignores(self):
        # le dépôt conforme contient un commentaire FR et un « exemple » FR (clé technique) de plus de 12 mots
        self.assertIn("Commentaire interne : nous gardons", self.lire(PAGE))
        self.assertEqual(self.regle("restes_fr"), [])

    def test_noms_propres_ignores(self):
        self.remplacer("src/pages/a-propos/index.html", "</section>",
                       "<p>Nos clients comptent La Poste, la Banque Cantonale du Valais et la rédaction "
                       "du journal Le Temps à Lausanne.</p>\n</section>")
        self.remplacer(PAGE, "</section>",
                       "<p>Zu unseren Kunden zählen La Poste, die Banque Cantonale du Valais und die Redaktion "
                       "von Le Temps in Lausanne.</p>\n</section>")
        self.assertEqual(self.regle("restes_fr"), [])

    def test_article_allemand_des_tolere(self):
        self.remplacer(PAGE, "Wir entwickeln LexMachina und Corrext für Juristinnen und Juristen, die Verträge, "
                             "Urteile und Auszüge aus dem Handelsregister übersetzen.",
                       "Wir prüfen LexMachina und Corrext anhand des Originals, anhand des Glossars und anhand "
                       "des Handelsregisters vor jeder Abgabe.")
        self.assertEqual(self.regle("restes_fr"), [])

    def test_json_non_traduit(self):
        self.glossaire(definition="La résiliation met fin au contrat pour l'avenir. Elle est soumise à un délai, "
                                  "à une forme et aux règles du code.")
        self.assertBloquant("restes_fr", GLOSS, "definition")

    def test_dictionnaire_non_traduit(self):
        cle = "Nous traduisons vos contrats pour les juristes qui travaillent avec des clients dans toute la Suisse."
        self.ecrire("src/i18n/cles.json", CLES + [cle])
        self.ecrire("src/i18n/de.json", {**I18N_DE, cle: cle})
        self.assertBloquant("restes_fr", "src/i18n/de.json")


class TestEszett(Base):
    def test_eszett_refuse(self):
        self.remplacer(PAGE, "übersetzen.", "gemäß Gesetz übersetzen.")
        self.assertBloquant("eszett", PAGE, "gemäß")

    def test_eszett_cite_par_la_source(self):
        self.remplacer("src/pages/a-propos/index.html", "</section>",
                       "<p>On écrit « Strasse » et non « Straße ».</p>\n</section>")
        self.remplacer(PAGE, "</section>", "<p>Man schreibt « Strasse » und nicht « Straße ».</p>\n</section>")
        self.assertEqual(self.regle("eszett"), [])

    def test_eszett_dans_un_json(self):
        self.glossaire(definition="Die Kündigung beendet den Vertrag gemäß Gesetz für die Zukunft.")
        self.assertBloquant("eszett", GLOSS)

    def test_eszett_hors_allemand(self):
        shutil.copytree(os.path.join(self.base, "src/langues/de"), os.path.join(self.base, "src/langues/it"))
        self.ecrire("src/i18n/it.json", I18N_DE)
        self.remplacer("src/langues/it/pages/a-propos/index.html", "übersetzen.", "gemäß übersetzen.")
        self.assertEqual(self.regle("eszett", lang="it"), [])


class TestTirets(Base):
    def test_cadratin_dans_une_page(self):
        self.remplacer(PAGE, "Juristinnen und Juristen,", "Juristinnen und Juristen \u2014")
        pbs = self.assertBloquant("tirets", PAGE)
        self.assertNotIn("\u2014", pbs[0]["detail"])

    def test_demi_cadratin_dans_un_json(self):
        self.glossaire(definition="Die Kündigung beendet den Vertrag \u2013 für die Zukunft.")
        self.assertBloquant("tirets", GLOSS, "definition")

    def test_cadratin_dans_le_dictionnaire(self):
        self.ecrire("src/i18n/de.json", {**I18N_DE, "Lire la suite": "Weiterlesen \u2014"})
        self.assertBloquant("tirets", "src/i18n/de.json")

    def test_trait_d_union_et_point_median_toleres(self):
        self.remplacer(PAGE, "Juristinnen und Juristen,", "Juristinnen und Juristen · Kanzlei-Teams,")
        self.assertEqual(self.regle("tirets"), [])


class TestProduits(Base):
    def test_casse_modifiee(self):
        self.remplacer(PAGE, "Wir entwickeln LexMachina", "Wir entwickeln Lexmachina")
        self.assertBloquant("produits", PAGE, "Lexmachina")

    def test_un_nom_en_moins_avertit(self):
        self.remplacer(PAGE, "LexMachina und Corrext für", "LexMachina für")
        pbs = self.regle("produits")
        self.assertTrue(pbs)
        self.assertEqual({p["gravite"] for p in pbs}, {"avertissement"})

    def test_deux_noms_en_moins_bloquant(self):
        self.remplacer(PAGE, "<h1>Neur.on, ein", "<h1>Ein")
        self.remplacer(PAGE, 'alt="Das Team von Neur.on in Freiburg"', 'alt="Unser Team in Freiburg"')
        self.assertBloquant("produits", PAGE, "Neur.on")

    def test_mot_compose_allemand_tolere(self):
        self.remplacer(PAGE, "Seite zu Corrext</a>, um", "Corrext-Seite</a>, um")
        self.assertEqual(self.controle(), [])

    def test_nom_dans_le_dictionnaire(self):
        self.ecrire("src/i18n/cles.json", CLES + ["Essayer Corrext et LexMachina"])
        self.ecrire("src/i18n/de.json", {**I18N_DE, "Essayer Corrext et LexMachina": "CORREXT und LEXMACHINA testen"})
        self.assertBloquant("produits", "src/i18n/de.json")


class TestSeo(Base):
    def test_title_trop_court(self):
        self.remplacer(PAGE, "title: Über Neur.on · das Schweizer Unternehmen hinter Corrext",
                       "title: Neur.on und Corrext")
        pbs = self.regle("seo")
        self.assertTrue(pbs)
        self.assertEqual({p["gravite"] for p in pbs}, {"avertissement"})
        self.assertIn("title", pbs[0]["detail"])

    def test_description_json_trop_longue(self):
        self.glossaire(description="Die Kündigung beendet einen Vertrag für die Zukunft. " * 4)
        pbs = self.regle("seo")
        self.assertTrue(pbs and pbs[0]["fichier"] == GLOSS and pbs[0]["gravite"] == "avertissement")
        self.assertIn("description", pbs[0]["detail"])


class TestTermes(Base):
    def test_equivalent_absent(self):
        self.remplacer(PAGE, "aus dem Handelsregister", "aus dem Firmenbuch")
        pbs = self.regle("termes")
        self.assertTrue(pbs)
        self.assertEqual({p["gravite"] for p in pbs}, {"avertissement"})
        self.assertIn("Handelsregister", pbs[0]["detail"])

    def test_flexion_toleree(self):
        self.remplacer(PAGE, "Auszüge aus dem Handelsregister", "Handelsregisterauszüge")
        self.assertEqual(self.controle(), [])

    def test_equivalent_dans_un_autre_segment_signale(self):
        self.remplacer(PAGE, "aus dem Handelsregister", "aus dem Firmenbuch")
        self.remplacer(PAGE, "um mehr zu erfahren", "um mehr über das Handelsregister zu erfahren")
        self.assertTrue(self.regle("termes"))

    def test_sans_base_terminologique(self):
        os.remove(os.path.join(self.base, "src/i18n/termes-de.json"))
        self.remplacer(PAGE, "aus dem Handelsregister", "aus dem Firmenbuch")
        self.assertEqual(self.regle("termes"), [])


class TestLigneDeCommande(Base):
    def lancer(self, *args):
        sortie = io.StringIO()
        with contextlib.redirect_stdout(sortie):
            code = C.main(list(args), base=self.base)
        return code, sortie.getvalue()

    def test_conforme_code_zero(self):
        code, _ = self.lancer("de")
        self.assertEqual(code, 0)

    def test_bloquant_code_un_et_resume(self):
        self.remplacer(PAGE, "Juristinnen und Juristen,", "Juristinnen und Juristen \u2014")
        self.remplacer(PAGE, "title: Über Neur.on · das Schweizer Unternehmen hinter Corrext",
                       "title: Neur.on und Corrext")
        code, texte = self.lancer("de")
        self.assertEqual(code, 1)
        self.assertIn(PAGE, texte)
        self.assertIn("Résumé", texte)
        self.assertIn("tirets", texte)
        self.assertIn("seo", texte)
        self.assertNotIn("\u2014", texte)
        self.assertNotIn("\u2013", texte)

    def test_avertissement_seul_code_zero(self):
        self.remplacer(PAGE, "title: Über Neur.on · das Schweizer Unternehmen hinter Corrext",
                       "title: Neur.on und Corrext")
        code, _ = self.lancer("de")
        self.assertEqual(code, 0)

    def test_seulement(self):
        self.remplacer(PAGE, "Juristinnen und Juristen,", "Juristinnen und Juristen \u2014")
        code, texte = self.lancer("de", "--seulement", "glossaire")
        self.assertEqual(code, 0)
        self.assertNotIn(PAGE, texte)
        self.assertEqual(self.controle(seulement="glossaire"), [])
        self.assertTrue(self.controle(seulement="pages/a-propos"))


if __name__ == "__main__":
    unittest.main()

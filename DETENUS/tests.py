from django.test import TestCase
from .models import Detenu, Agent, Prison
from datetime import date, timedelta

class DetenuModelTest(TestCase):

    def setUp(self):
        # Créez des instances nécessaires pour les tests
        self.agent = Agent.objects.create(nom="AgentTest")
        self.prison = Prison.objects.create(nom="PrisonTest")

    def test_detenu_est_libere(self):
        # Créez un détenu avec une date de sortie passée
        detenu_libere = Detenu.objects.create(
            nom="Test",
            postnom="Test",
            prenom="Test",
            profil="test.jpg",
            matricule="12345",
            sexe="M",
            date_de_naissance=date(1990, 1, 1),
            motif="Test Motif",
            peine="CAPITALE",
            condamne_par=self.agent,
            prison_incarceree=self.prison,
            date_entree=date(2020, 1, 1),
            date_sortie=date.today() - timedelta(days=1),
            cellule="A1",
            dossier="test.pdf"
        )
        self.assertTrue(detenu_libere.est_libere)

    def test_detenu_non_libere(self):
        # Créez un détenu avec une date de sortie future
        detenu_non_libere = Detenu.objects.create(
            nom="Test",
            postnom="Test",
            prenom="Test",
            profil="test.jpg",
            matricule="12346",
            sexe="M",
            date_de_naissance=date(1990, 1, 1),
            motif="Test Motif",
            peine="CAPITALE",
            condamne_par=self.agent,
            prison_incarceree=self.prison,
            date_entree=date(2020, 1, 1),
            date_sortie=date.today() + timedelta(days=1),
            cellule="A1",
            dossier="test.pdf"
        )
        self.assertFalse(detenu_non_libere.est_libere)
from django.test import TestCase
from django.contrib.auth.models import User
from comptes.models import Profil

class ProfilSignalTest(TestCase):

    def test_profil_cree_automatiquement(self):
        # Vérifie qu’un profil est créé automatiquement quand un utilisateur est ajouté.
        user = User.objects.create_user(username="Usertest", password="Azerty89")

        # Vérifie que le profil existe bien automatiquement
        profil = Profil.objects.get(user=user)
        self.assertIsNotNone(profil)
        self.assertEqual(profil.user.username, "Usertest")

    def test_profil_supprime_avec_user(self):
        # Vérifie que la suppression d’un user supprime aussi son profil.
        user = User.objects.create_user(username="Usertest", password="Azerty89")
        profil_id = user.profil.id 

        # Supprime l'utilisateur
        user.delete()

        # Supprime aussi le profil
        with self.assertRaises(Profil.DoesNotExist):
            Profil.objects.get(id=profil_id)

    def test_uuid_genere_automatiquement(self):
        user = User.objects.create_user(username="Usertest", password="Azerty89")
        profil = Profil.objects.get(user=user)
        self.assertIsNotNone(profil.uuid)

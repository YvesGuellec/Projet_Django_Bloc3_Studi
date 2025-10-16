from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse, resolve
from vitrine import views

class DeconnexionTest(TestCase):
    # Ce test prend en compte la connexion et la déconexion

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username="Testuser", password="Azerty89")
        self.url = reverse("comptes:logout")

    def test_deconnexion_redirige_vers_index(self):
        # Connexion d’un utilisateur
        self.client.login(username="Testuser", password="Azerty89")

        # Vérifie qu’il est connecté avant
        response = self.client.get(reverse("boutique:index"))
        self.assertTrue(response.wsgi_request.user.is_authenticated)

        # Appel de la vue de déconnexion
        response = self.client.get(self.url)

         # Vérifie la redirection
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("boutique:index"))

        # Vérifie que l'utilisateur est bien déconnecté
        response_suivant = self.client.get(reverse("boutique:index"))
        self.assertFalse(response_suivant.wsgi_request.user.is_authenticated)





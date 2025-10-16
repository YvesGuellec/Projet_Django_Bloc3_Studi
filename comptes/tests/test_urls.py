from django.test import SimpleTestCase
from django.urls import reverse, resolve
from comptes import views

class TestComptesUrls(SimpleTestCase):
    # Vérifie que chaque vu pointe vers la bonne vue.

    def test_register_url_resolves(self):
        url = reverse('comptes:register')
        self.assertEqual(resolve(url).func, views.inscription_view)

    def test_login_url_resolves(self):
        url = reverse('comptes:login')
        self.assertEqual(resolve(url).func, views.connexion_view)

    def test_logout_url_resolves(self):
        url = reverse('comptes:logout')
        self.assertEqual(resolve(url).func, views.deconnexion_view)

    def test_verification_url_resolve(self):
        url = reverse('comptes:verification_2fa')
        self.assertEqual(resolve(url).func, views.verification_2fa_view)

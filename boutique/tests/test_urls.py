from django.test import SimpleTestCase
from django.urls import reverse, resolve
from boutique import views

class TestBoutiqueUrls(SimpleTestCase):
    # Vérifie que chaque vu pointe vers la bonne vue.

    def test_index_url_resolves(self):
        url = reverse('boutique:index')
        self.assertEqual(resolve(url).func, views.Index)

    def test_ajouter_au_panier_url_resolves(self):
        url = reverse('boutique:ajouter_au_panier')
        self.assertEqual(resolve(url).func, views.ajouter_au_panier)

    def test_voir_panier_url_resolves(self):
        url = reverse('boutique:panier')
        self.assertEqual(resolve(url).func, views.voir_panier)

    def test_vider_panier_url_resolves(self):
        url = reverse('boutique:vider_panier')
        self.assertEqual(resolve(url).func, views.vider_panier)

    def test_commander_url_resolves(self):
        url = reverse('boutique:commander')
        self.assertEqual(resolve(url).func, views.commander)

    def test_commande_detail_url_resolves(self):
        url = reverse('boutique:commande', args=[1, 2])
        self.assertEqual(resolve(url).func, views.Qrcode)

from django.test import TestCase
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from django.http import JsonResponse
from boutique.models import Produit, Panier, LignePanier, Commande, LigneCommande
from comptes.models import Profil 

class ParcoursUtilisateurTest(TestCase):

    def setUp(self):
        # Création utilisateur et récupération de son profil
        self.user = User.objects.create_user(username='Testuser', password='Azerty89')
        self.profil, _ = Profil.objects.get_or_create(user=self.user)

        # Connexion utilisateur
        self.client = Client()
        self.client.login(username='Testuser', password='Azerty89')

        # Création du produit et du panier
        self.produit = Produit.objects.create(nom='Produit test', prix=10)
        self.panier = Panier.objects.create(utilisateur=self.user)
        self.ligne_panier = LignePanier.objects.create(
            panier=self.panier,
            produit=self.produit,
            quantite=3
        )

        # URL de la vue commander
        self.url = reverse('boutique:commander')

    def test_commande_creee_dans_panier(self):
        response = self.client.post(self.url)

        self.assertEqual(response.status_code, 201)

        # Vérifie la réponse JSON
        data = response.json()
        self.assertIn('message', data)
        self.assertIn('redirect_url', data)

        # Vérifie que la commande a bien été créée
        commande = Commande.objects.get(utilisateur=self.user)
        self.assertEqual(commande.lignes.count(), 1)

        ligne_commande = commande.lignes.first()
        self.assertEqual(ligne_commande.produit, self.produit)
        self.assertEqual(ligne_commande.quantite, 3)
        self.assertEqual(float(ligne_commande.prix_unitaire), 10.0)

        # Total commande
        self.assertEqual(float(commande.total), 30.0)

        # Suppression du panier
        self.assertFalse(LignePanier.objects.filter(panier=self.panier).exists())
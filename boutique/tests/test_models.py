from django.test import TestCase
from django.contrib.auth.models import User
from boutique.models import Panier, LignePanier, Produit, LigneCommande, Commande

class PanierModelTest(TestCase):
        # Génère un utilisateur fictif pour le test
    def setUp(self):
        self.user = User.objects.create_user(username='Testutilisateur', password='azerty89')

    def test_creation_panier(self):
        # Test que la création d’un panier s'associe bien a un utilisateur et une date
        panier = Panier.objects.create(utilisateur=self.user)
        
        self.assertEqual(panier.utilisateur.username, 'Testutilisateur')

        self.assertIsNotNone(panier.date_creation)

class LignePanierTest(TestCase):
     # Génère un utilisateur, un panier, un produit fictif pour le test
    def setUp(self):
        self.user = User.objects.create_user(username='Testutilisateur', password='Azerty88')
        self.panier = Panier.objects.create(utilisateur=self.user)
        self.produit = Produit.objects.create(nom='Produit test', prix=10.0)

    def test_relation_produit_et_panier(self):
        # test la relation entre LignePanier et Produit / LignePanier et Panier
        ligne = LignePanier.objects.create(
            panier=self.panier,
            produit=self.produit,
            quantite=3
        )
        self.assertEqual(ligne.panier, self.panier)
        self.assertEqual(ligne.produit, self.produit)
        self.assertEqual(ligne.quantite, 3)
  
class LigneCommandeTest_CommandeTest(TestCase):
    # Génère un utilisateur, un panier, un produit fictif pour le test
    def setUp(self):
        self.user = User.objects.create_user(username='Usertest')
        self.produit = Produit.objects.create(nom='Produit test', prix=15)
        self.panier = Panier.objects.create(utilisateur=self.user)
    # Génère une ligne dans le panier
        self.ligne_panier = LignePanier.objects.create(
            panier=self.panier,
            produit=self.produit,
            quantite=4
        )
    # Création d'une commande
        self.commande = Commande.objects.create(
            utilisateur=self.user,
            total=30  
        )
    # Génère une lignes dans une commande
        self.ligne_commande = LigneCommande.objects.create(
            commande=self.commande,
            produit=self.produit,
            quantite=2,
            prix_unitaire=self.produit.prix
        )

    def test_relation_LigneCom_et_Commande(self):
        self.assertEqual(self.commande.lignes.count(), 1)
        ligne = self.commande.lignes.first()
        self.assertEqual(ligne.produit.nom, 'Produit test')
        self.assertEqual(ligne.quantite, 2)
        self.assertEqual(ligne.prix_unitaire, 15)
    

from django.db import models
from django.contrib.auth.models import User
import uuid

class Produit(models.Model):
    nom = models.CharField(max_length=50)
    prix = models.FloatField(default=0.0)
    date_ajout = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'Nom du produit : {self.nom} | Prix : {self.prix}Euros'
    
class Panier(models.Model):
    utilisateur = models.ForeignKey(User, on_delete=models.CASCADE)
    date_creation = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Panier de : {self.utilisateur} | Date de création du panier : {self.date_creation.strftime('%d-%m%Y')}'

class LignePanier(models.Model):
    panier = models.ForeignKey(Panier, related_name='lignes', on_delete=models.CASCADE)
    produit = models.ForeignKey(Produit, on_delete=models.CASCADE)
    quantite = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f'Produit : {self.produit.nom} | Quantite : {self.quantite}'
    

class Commande(models.Model):
    utilisateur = models.ForeignKey(User, on_delete=models.CASCADE)
    cle2 = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    date_commande = models.DateTimeField(auto_now_add=True)
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    

    def __str__(self):
        return f"Nom d'utilisateur : {self.utilisateur}"

class LigneCommande(models.Model):
    commande = models.ForeignKey(Commande, related_name='lignes', on_delete=models.CASCADE)
    produit = models.ForeignKey(Produit, on_delete=models.CASCADE)
    quantite = models.PositiveIntegerField()
    prix_unitaire = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)

    def __str__(self):
        return f"N° commande : {self.commande.id}| Nom d'utilisateur : {self.commande.utilisateur} Produit : [{self.produit.nom}] {self.quantite}x{self.prix_unitaire}={self.commande.total}"
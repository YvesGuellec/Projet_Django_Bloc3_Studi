from django.urls import path
from . import views

app_name = 'boutique'

urlpatterns = [
    path('index', views.Index, name='index'),
    path('ajouter-au-panier/', views.ajouter_au_panier, name='ajouter_au_panier'),
    path('panier/', views.voir_panier, name='panier'),
    path('vider-panier/', views.vider_panier, name='vider_panier'),
    path('commander/', views.commander, name='commander'),
    path('commande/<int:commande_id>/<int:profil_id>/', views.Qrcode, name='commande'),
    path('panier_supprimer/', views.panier_supprimer, name='panier_supprimer'),

]



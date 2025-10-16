from django.urls import path
from . import views

app_name = 'comptes'

urlpatterns = [
    path('register/', views.inscription_view, name='register'),
    path('login/', views.connexion_view, name='login'),
    path('logout/', views.deconnexion_view, name='logout'),
    path('verification_2fa', views.verification_2fa_view, name='verification_2fa'),
]

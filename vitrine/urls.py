from django.urls import path
from . import views

app_name = 'vitrine'

urlpatterns = [
    path('', views.Accueil, name='accueil'),

]


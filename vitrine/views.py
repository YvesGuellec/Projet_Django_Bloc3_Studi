from django.shortcuts import render
from .models import Sport

def Accueil(request):
    sports = Sport.objects.all()

    context = {
        'sports':sports
    }

    return render(request, 'vitrine/accueil.html', context)
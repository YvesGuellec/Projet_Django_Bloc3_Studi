from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout, get_user_model
from .forms import FormulaireInscription, FormulaireConnexion
from django.core.mail import send_mail
import random

User = get_user_model()

def inscription_view(request):
    if request.method == 'POST':
        form = FormulaireInscription(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Connecte automatiquement
            return redirect('boutique:index')  # Redirige vers la page d’accueil
    else:
        form = FormulaireInscription()
    return render(request, 'comptes/register.html', {'form': form})


def connexion_view(request):
    if request.method == 'POST':
        form = FormulaireConnexion(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()

            code = random.randint(100000, 999999)

            request.session['2fa_user_id'] = user.id
            request.session['2fa_code'] = str(code)

            send_mail(
                subject='Votre code de vérification',
                message=f'Voici votre code de double authentification : {code}',
                from_email='no-reply@monsite.com',
                recipient_list=[user.email],
            )

            return redirect('comptes:verification_2fa')
    else:
        form = FormulaireConnexion()

    return render(request, 'comptes/login.html', {'form': form})


def verification_2fa_view(request):
    if request.method == 'POST':
        code_saisi = request.POST.get('code')
        code_session = request.session.get('2fa_code')
        user_id = request.session.get('2fa_user_id')

        if code_saisi == code_session and user_id:
            user = User.objects.get(id=user_id)
            login(request, user)

            del request.session['2fa_code']
            del request.session['2fa_user_id']

            return redirect('vitrine:accueil')

    return render(request, 'comptes/verification_2fa.html')


def deconnexion_view(request):
    logout(request)
    return redirect('boutique:index')


# def connexion_view(request):
#     if request.method == 'POST':
#         form = FormulaireConnexion(request, data=request.POST)
#         if form.is_valid():
#             user = form.get_user()
#             login(request, user)
#             return redirect('boutique:index')
#     else:
#         form = FormulaireConnexion()

#     return render(request, 'comptes/login.html', {'form': form})
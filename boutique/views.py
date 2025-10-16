from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from .models import Panier, LignePanier, Produit, Commande, LigneCommande
from comptes.models import Profil
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
import qrcode, base64, json
from io import BytesIO
from django.core.files import File
from django.urls import reverse

def Index(request):
    produits = Produit.objects.all()

    context = {
        'produits':produits
    }
    return render(request, 'boutique/index.html', context)

@require_POST
@login_required
def ajouter_au_panier(request):
    try:
        data = json.loads(request.body)
        produit_id = data.get('product_id')

        produit = Produit.objects.get(id=produit_id)
        panier, _ = Panier.objects.get_or_create(utilisateur=request.user)

        ligne, created = LignePanier.objects.get_or_create(
            panier=panier,
            produit=produit,
            defaults={'quantite': 1}
        )

        if not created:
            ligne.quantite += 1
            ligne.save()

        return JsonResponse({'success': True, 'total_items': panier.lignes.count()})

    except Produit.DoesNotExist:
        return JsonResponse({'error': 'Produit introuvable'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@login_required
def voir_panier(request):
    panier = Panier.objects.filter(utilisateur=request.user).first()
    articles = panier.lignes.select_related('produit') if panier else []

    total = sum(ligne.produit.prix * ligne.quantite for ligne in articles)

    return render(request, 'boutique/panier.html', {
        'articles': articles,
        'total': total,
    })

@login_required
def vider_panier(request):
    panier = Panier.objects.filter(utilisateur=request.user).first()
    if panier:
        panier.lignes.all().delete()
    return redirect('boutique:voir_panier')

@login_required
def commander(request):
    if request.method == "POST":
        try:
            user = request.user

            profil = Profil.objects.get(user=user)

            panier = Panier.objects.filter(utilisateur=user).first()
            if not panier:
                return JsonResponse({'error': 'Votre panier est vide'}, status=400)

            lignes = panier.lignes.select_related('produit')
            if not lignes.exists():
                return JsonResponse({'error': 'Aucun article dans le panier'}, status=400)

            total = sum(ligne.produit.prix * ligne.quantite for ligne in lignes)

            commande = Commande.objects.create(utilisateur=user, total=total)

            for ligne in lignes:
                LigneCommande.objects.create(
                    commande=commande,
                    produit=ligne.produit,
                    quantite=ligne.quantite,
                    prix_unitaire=ligne.produit.prix
                )

            lignes.delete()
                
            redirect_url = reverse('boutique:commande', args=[commande.id, profil.id])

            return JsonResponse({'message': 'Commande enregistrée avec succès !','redirect_url': redirect_url}, status=201)

        except Exception as e:
            print("Erreur commande:", e)
            return JsonResponse({'error': str(e)}, status=500)

    return JsonResponse({'error': 'Méthode non autorisée'}, status=405)

@login_required
def Qrcode(request, commande_id, profil_id):
    commande = get_object_or_404(Commande, id=commande_id)
    profil = get_object_or_404(Profil, id=profil_id)

    if commande.utilisateur != profil.user:
        return render(request, 'erreur.html', {'message': "Cette commande n'appartient pas à cet utilisateur."})

    data = f"https://tonsite.com/verifier-commande/?u={profil.uuid}&c={commande.cle2}"

    qr = qrcode.make(data)
    buffer = BytesIO()
    qr.save(buffer, format="PNG")
    buffer.seek(0)
    
    image_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')
    image_data = f"data:image/png;base64,{image_base64}"

    return render(request, 'boutique/commande.html', {
        'commande': commande,
        'profil': profil,
        'qr_image': image_data,
        })

def panier_supprimer(request):
    panier = Panier.objects.filter(utilisateur=request.user).first()
    
    if panier:
        panier.lignes.all().delete() 
    
    return redirect('boutique:panier')



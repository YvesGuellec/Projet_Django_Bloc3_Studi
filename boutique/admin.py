from django.contrib import admin
from .models import Panier, LignePanier, Commande, Produit
from django.db.models import Count, Sum, F, ExpressionWrapper, DecimalField


class LignePanierInline(admin.TabularInline):
    model = LignePanier
    extra = 0
    readonly_fields = ('produit', 'quantite')
    can_delete = True

@admin.register(Panier)
class PanierAdmin(admin.ModelAdmin):
    list_display = ('utilisateur', 'date_creation', 'nombre_articles')
    search_fields = ('utilisateur__username',)
    list_filter = ('date_creation',)
    inlines = [LignePanierInline]

    def nombre_articles(self, obj):
        return sum(ligne.quantite for ligne in obj.lignes.all())
    nombre_articles.short_description = "Articles"

@admin.register(Commande)
class CommandeAdmin(admin.ModelAdmin):
    list_display = ('id', 'utilisateur', 'cle2', 'date_commande', 'total', 'nombre_articles')
    search_fields = ('utilisateur__username', 'cle2')
    list_filter = ('date_commande',)
    ordering = ('-date_commande',)

    def nombre_articles(self, obj):
        return sum(ligne.quantite for ligne in obj.lignes.all())
    nombre_articles.short_description = "Articles"


@admin.register(Produit)
class ProduitAdmin(admin.ModelAdmin):
    list_display = ('nom', 'prix', 'qte_totale_vendue', 'prix_total_ventes')
    ordering = ('id',)

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        qs = qs.annotate(
            total_vendu=Sum('lignecommande__quantite'),
            total_prix=Sum(
                ExpressionWrapper(
                    F('lignecommande__quantite') * F('lignecommande__prix_unitaire'),
                    output_field=DecimalField(max_digits=12, decimal_places=2)
                )
            )
        )
        return qs

    def qte_totale_vendue(self, obj):
        return obj.total_vendu or 0
    qte_totale_vendue.short_description = "Quantité totale vendue"
    qte_totale_vendue.admin_order_field = 'total_vendu'

    def prix_total_ventes(self, obj):
        return f"{obj.total_prix or 0:.2f} €"
    prix_total_ventes.short_description = "Chiffre d’affaires total"
    prix_total_ventes.admin_order_field = 'total_prix'

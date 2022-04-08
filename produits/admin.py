from django.contrib import admin
from .models import Categorie, Produit, Commande

# Register your models here.
admin.site.register(Produit)
admin.site.register(Categorie)
admin.site.register(Commande)
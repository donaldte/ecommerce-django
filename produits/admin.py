from django.contrib import admin
from .models import Categorie, Produit

# Register your models here.
admin.site.register(Produit)
admin.site.register(Categorie)
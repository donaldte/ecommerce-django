from django.contrib import admin
from .models import Categorie, Produit,  Order, OrderItem

# Register your models here.
admin.site.register(Produit)
admin.site.register(Categorie)
admin.site.register(Order)
admin.site.register(OrderItem)
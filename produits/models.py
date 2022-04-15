
from tkinter import CASCADE
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _ 
from authapp.models import  UserRegistrationModel
# Create your models here.

class Categorie(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        verbose_name = _("Categorie")
        verbose_name_plural = _("Categories")

    def __str__(self):
        return self.name
class Produit(models.Model):
    user = models.ForeignKey(UserRegistrationModel, on_delete=models.CASCADE)
    name = models.CharField(_("Nom du produit"), max_length=50)
    categorie = models.ForeignKey(Categorie, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='products', null=True, blank=True)
    description = models.TextField(_("Description du produit"))
    prix = models.PositiveIntegerField(_("Prix du produit"))
    date_added = models.DateTimeField(auto_now_add=True)
    mode_payement = models.CharField(_('Mode De Payement'), max_length=100, default="Orange Money")
    
    class Meta:
        verbose_name = _("Produit")
        verbose_name_plural = _("Produits")
        ordering = ['-date_added']

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("produits:produit_detail", kwargs={"pk": self.pk})

    def get_add_to_card_url(self):
        return reverse("produits:add_to_card", kwargs={"pk": self.pk})

    def get_remove_from_card_url(self):
        return reverse("produits:remove_from_card", kwargs={"pk": self.pk})    
         
    


class OrderItem(models.Model):
    item = models.ForeignKey(Produit, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    user = models.ForeignKey(UserRegistrationModel, on_delete=models.CASCADE)
    ordered = models.BooleanField(default=False)


    def __str__(self):
        return f"{self.quantity} de {self.item}"

    def get_total_item_price(self):
        return self.quantity * self.item.prix   

       

class Order(models.Model):
    user = models.ForeignKey(UserRegistrationModel, on_delete=models.CASCADE)
    item = models.ManyToManyField(OrderItem, related_name='order')
    started_date = models.DateTimeField(auto_now_add=True)
    ordered_date = models.DateTimeField()
    ordered = models.BooleanField(default=False)
    frais_de_livraison = models.IntegerField(_('Frais De Livraison'), default=500)
   
    class Meta:
        verbose_name = _("Order")
        verbose_name_plural = _("Orders")

    def __str__(self):
        return f"{self.user}-{self.started_date}"

    def get_absolute_url(self):
        return reverse("produits:order_detail", kwargs={"pk": self.pk})

    def get_frais(self):
        return self.frais_de_livraison    

    def get_total(self):
        total = 0
        for order_item in self.item.all():
            total += order_item.get_total_item_price()
        total += self.frais_de_livraison     
        return total    
         
    



   

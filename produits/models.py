from unicodedata import category
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

    class Meta:
        verbose_name = _("Produit")
        verbose_name_plural = _("Produits")
        ordering = ['-date_added']

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("produits:produit_detail", kwargs={"pk": self.pk})


class Commande(models.Model):
    vendeur = models.ForeignKey(UserRegistrationModel, on_delete=models.CASCADE)
    items = models.CharField(max_length=300)
    prix = models.CharField(max_length=200)
    nom = models.CharField(max_length=150)
    email = models.EmailField()
    address = models.CharField(max_length=200)
    ville = models.CharField(max_length=200)
    pays = models.CharField(max_length=300)
    telephone = models.CharField(max_length=300)
    date_commande = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-date_commande']


   

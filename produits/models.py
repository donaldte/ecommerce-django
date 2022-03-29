from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _ 
# Create your models here.

class Produit(models.Model):

    name = models.CharField(_("Nom du produit"), max_length=50)
    description = models.CharField(_("Description du produit"), max_length=50)
    prix = models.PositiveIntegerField(_("Prix du produit"))

    class Meta:
        verbose_name = _("Produit")
        verbose_name_plural = _("Produits")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("produits:Produit_detail", kwargs={"pk": self.pk})


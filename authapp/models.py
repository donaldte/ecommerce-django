from django.db import models
from django.contrib.auth.models import AbstractUser , User
from django.utils.translation import gettext_lazy as _
# Create your models here.


class UserRegistrationModel(AbstractUser):
    region = models.CharField(_('region'),max_length=100)
    ville = models.CharField(_('ville'), max_length=100)
    numero_telephone = models.CharField(_("numero whatsapp"), max_length=15)
    biographie = models.TextField()
    peut_vendre = models.BooleanField(default=False)
    ne_peut_vendre = models.BooleanField(_('Je veux vendre'), default=False)
    
   
    
    

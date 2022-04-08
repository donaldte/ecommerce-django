from .models import *
from django import  forms
from authapp.models import UserRegistrationModel

class AddPrductForm(forms.ModelForm):
    class Meta:
        model = Produit
        exclude = ('user',)

class UserPrductForm(forms.ModelForm):
    class Meta:
        model = UserRegistrationModel
        exclude = ('password', 'permissions', 'groups', )

          
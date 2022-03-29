from .models import UserRegistrationModel
from django import forms
# from .models import Profile
from django.contrib.auth.forms import AuthenticationForm, UsernameField
from .models import UserRegistrationModel
from django.contrib.auth.forms import PasswordResetForm

 
class UserRegistration(forms.ModelForm):
    password = forms.CharField(label='Mot de passe', widget=forms.PasswordInput)
    password2 = forms.CharField(
        label='Repeter le Mot de password', widget=forms.PasswordInput)

    class Meta:
        model = UserRegistrationModel
        fields = ('username', 'first_name', 'last_name', 'email', 'region', 'ville', 'numero_telephone', 'biographie')

        def clean_password2(self):
            cd = self.cleaned_data
            if cd['password'] != cd['password2']:
                raise forms.ValidationError('Les deux mots de passe ne sont pas identique.')
            return cd['password2']


class UserEditForm(forms.ModelForm):
    class Meta:
        model = UserRegistrationModel
        fields = ('first_name', 'last_name', 'email', 'region', 'ville', 'numero_telephone', 'biographie')



from .models import UserRegistrationModel
from django import forms
# from .models import Profile
from .models import UserRegistrationModel
from django.contrib.auth.forms import PasswordResetForm

 
class UserRegistration(forms.ModelForm):
    password1 = forms.CharField(label='Mot de passe', widget=forms.PasswordInput)
    password2 = forms.CharField(
        label='Repeter le Mot de password', widget=forms.PasswordInput)

    class Meta:
        model = UserRegistrationModel
        fields = ('username', 'first_name', 'last_name', 'email', 'region', 'ville', 'numero_telephone', 'biographie')

        def clean_password2(self):
            password1 = self.cleaned_data.get('password1')
            password2 = self.cleaned_data.get('password2')

            if password1 and password2 and password1 != password2:
                raise forms.ValidationError('Les mots mots de passes sont different!!')
            return password2

    def save(self, commit=True):
        user = super(UserRegistration, self).save(commit=False)
        user.set_password(self.cleaned_data['password2'])
        if commit:
            user.save()
        return user


class UserEditForm(forms.ModelForm):
    class Meta:
        model = UserRegistrationModel
        fields = ('first_name', 'last_name', 'email', 'region', 'ville', 'numero_telephone', 'biographie')



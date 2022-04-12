from .models import UserRegistrationModel
from django import forms
# from .models import Profile
from .models import UserRegistrationModel
from django.contrib.auth.forms import PasswordResetForm

 
class UserRegistration(forms.ModelForm):
    password1 = forms.CharField(label='Mot de passe', widget=forms.PasswordInput)
    password2 = forms.CharField(
        label='Repeter le Mot de password', widget=forms.PasswordInput)
    ne_peut_vendre = forms.BooleanField(label='JE VEUX VENDRE' ,required=True)
    class Meta:
        model = UserRegistrationModel
        fields = ('username', 'first_name', 'last_name', 'email', 'region', 'ville', 'numero_telephone', 'ne_peut_vendre', 'biographie')

        def clean_password2(self):
            password1 = self.cleaned_data.get('password1')
            password2 = self.cleaned_data.get('password2')

            if password1 and password2 and password1 != password2:
                raise forms.ValidationError('Les mots mots de passes sont different!!')
            return password2
        def clean_ne_peut_vendre(self):
            ne_peut_vendre = self.clean_data.get('ne_peux_vendre')
            if ne_peut_vendre:
                return ne_peut_vendre
            else:
                forms.ValidationError("vous devez cocher la case * JE VEUX VENDRE* ")                

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


class UserCustomerForm(forms.ModelForm):
    password1 = forms.CharField(label='Mot de passe', widget=forms.PasswordInput)
    password2 = forms.CharField(
        label='Repeter le Mot de password', widget=forms.PasswordInput)

    class Meta:
        model = UserRegistrationModel
        fields = ('username', 'first_name', 'last_name', 'email', 'region', 'ville', 'numero_telephone')

        def clean_password2(self):
            password1 = self.cleaned_data.get('password1')
            password2 = self.cleaned_data.get('password2')

            if password1 and password2 and password1 != password2:
                raise forms.ValidationError('Les mots mots de passes sont different!!')
            return password2

    def save(self, commit=True):
        user = super(UserCustomerForm, self).save(commit=False)
        user.set_password(self.cleaned_data['password2'])
        if commit:
            user.save()
        return user


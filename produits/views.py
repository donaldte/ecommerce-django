from django.shortcuts import redirect, render
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, DetailView, UpdateView, ListView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin

from produits.models import Produit
from authapp.models import UserRegistrationModel
from .form import AddPrductForm, UserPrductForm
from django.contrib import messages

# Create your views here.

#home page 
def home(request):
    return render(request, 'produits/index.html')



#statistique des achats
@staff_member_required
def statistique(request):
    return render(request, 'statistique/index.html')

@staff_member_required
def product_sellers_list(request):
    userproduits = Produit.objects.all()
    return render(request, 'statistique/table-export.html', {'userproduit':userproduits})    


@staff_member_required
def profile(request):
    userprofiles = UserRegistrationModel.objects.all()
    return render(request, 'statistique/app-profile.html', {'userprofiles':userprofiles})    

class UserEditView(LoginRequiredMixin,UpdateView):
	model = UserRegistrationModel
	form_class = UserPrductForm
	template_name = 'statistique/profile_modification.html'
	success_url = reverse_lazy('produits:profile')


# seller
@login_required 
def product_seller_list(request):
    userproduit = Produit.objects.filter(user=request.user)
    return render(request, 'seller/tables.html', {'userproduit':userproduit})        

@login_required
def addProduct(request):
    if request.method == 'POST':
        form = AddPrductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False)
            product.user = request.user
            product.save()
            messages.success(request, "The book was added successfully.")
            return redirect('/list')
        else:
            form = AddPrductForm(request.POST, request.FILES)
    else:
        form = AddPrductForm()
    return render(request, 'produits/add.html', {'form': form})

class EditViewProduct(LoginRequiredMixin,UpdateView):
	model = Produit
	form_class = AddPrductForm
	template_name = 'produits/edit_product.html'
	success_url = reverse_lazy('produits:produtListSeller')
	success_message = 'Le produit a ete bien modifie'


class DeleteViewProduct(LoginRequiredMixin,DeleteView):
	model = Produit
	template_name = 'produits/delete_product.html'
	success_url = reverse_lazy('produits:produtListSeller')
	success_message = 'le produit a été supprimé avec succès'    
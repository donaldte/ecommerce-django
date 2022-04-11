from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, DetailView, UpdateView, ListView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin

from produits.models import Commande, Order, OrderItem, Produit
from authapp.models import UserRegistrationModel
from .form import AddPrductForm, UserPrductForm
from django.contrib import messages
from django.core.paginator import Paginator

# Create your views here.
#home
def index(request):
    product_object = Produit.objects.all()
    item_name = request.GET.get('item')
    if item_name !='' and item_name is not None:
        product_object = Produit.objects.filter(name__icontains=item_name)
    paginator = Paginator(product_object, 6)
    page = request.GET.get('page')
    product_object = paginator.get_page(page)
    return render(request, 'produits/index.html', {'produits': product_object})

#detail
def detail(request, myid):
    product_object = Produit.objects.get(id=myid)
    return render(request, 'produits/detail.html', {'product': product_object})    

def checkout(request):
    return render(request, 'produits/checkout.html')

def checkout(request, id):
    produit = Produit.objects.get(id=id)
    items = produit.name
    prix = produit.prix
    user=produit.user
    if request.method == "POST":
        nom = request.POST.get('nom')
        email = request.POST.get('email')
        address = request.POST.get('address')
        ville = request.POST.get('ville')
        pays = request.POST.get('pays')
        telephone= request.POST.get('zipcode')
        com = Commande(vendeur=user, items=items, prix=prix, nom=nom, email=email, address=address, ville=ville, pays=pays, telephone=telephone)
        com.save()
        return redirect('/confirmation')
    return render(request, 'produits/checkout.html', {'item':items, 'price':prix}) 

def confimation(request):
    info = Commande.objects.all()[:1]
    for item in info:
        nom = item.nom
    return render(request, 'produits/confirmation.html', {'name': nom})            

#statistique des achats
@staff_member_required
def statistique(request):
    command = Commande.objects.all()
    valide = Commande.objects.filter(regler=True).count()
    count = Commande.objects.all().count()
    return render(request, 'statistique/index.html', {'commande':command, 'valid': valide, 'count':count})

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


def add_to_card(request, pk):
    item = get_object_or_404(Produit, id=pk)
    order_item = OrderItem.objects.create(item=item)
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        if order.item.filter(item__slug=item.slug).exists():
            order_item.quantity +=1
            order_item.save()
    else:
        order = OrderItem.objects.create(user=request.user)
        order.item.add(order_item)        
        




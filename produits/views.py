
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, DetailView, UpdateView, ListView, View
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin

from produits.models import  Categorie, Order, OrderItem, Produit
from authapp.models import UserRegistrationModel
from .form import AddPrductForm, UserPrductForm
from django.contrib import messages
from django.core.paginator import Paginator
from django.utils import timezone


# Create your views here.
#home
def index(request):
    product_object = Produit.objects.all()
    categories = Categorie.objects.all()
    item_name = request.GET.get('item')
    if item_name !='' and item_name is not None:
        product_object = Produit.objects.filter(name__icontains=item_name)
    paginator = Paginator(product_object, 6)
    page = request.GET.get('page')
    product_object = paginator.get_page(page)
    return render(request, 'produits/index.html', {'produits': product_object, 'categories':categories})

#detail
def detail(request, myid):
    product_object = Produit.objects.get(id=myid)
    return render(request, 'produits/detail.html', {'product': product_object})    

def checkout(request):
    return render(request, 'produits/checkout.html')

login_required
def confimation(request):
    has_order=False
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        order.ordered=True
        order.save()
        has_order = True

    return render(request, 'produits/confirmation.html', {'has_order': has_order})            

#statistique des achats
@staff_member_required
def statistique(request):
    commande = Order.objects.all().order_by('-ordered_date')
    valide = Order.objects.all().count()
    order_item = OrderItem.objects.all().count()
    total = UserRegistrationModel.objects.all().count()
    return render(request, 'statistique/index.html', {'commande':commande, 'valid': valide, 'order_item':order_item, 'total': total})

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
            messages.success(request, "The product has been added successfully.")
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

class OrderSummary(LoginRequiredMixin ,View):
    def get(self, *args, **kwargs):
        try:
            order = Order.objects.get(user=self.request.user, ordered=False)
            context = {
                'object':order
            }
        except ObjectDoesNotExist:
            messages.error(self.request, "Vous n'avez mis aucun produit dans le panier")    
        return render(self.request, 'produits/checkout.html', context)


def all_categories(request, pk):
    categories = Categorie.objects.get(id=pk)
    produits = Produit.objects.filter(categorie=categories)
    context = {
        'produits':produits
    }
    return render(request, 'produits/index.html', context)
    
@login_required
def add_to_card(request, pk):
    item = get_object_or_404(Produit, id=pk)
    order_item, created = OrderItem.objects.get_or_create(item=item, user=request.user, ordered=False)
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        if order.item.filter(item__id=item.id).exists():
            order_item.quantity +=1
            order_item.save()
            messages.info(request, f"{item}-quantité augmenté")    
        else:
            order.item.add(order_item)
            messages.success(request, f"produit {item} ajouté")    
    else:
        ordered_date  = timezone.now()
        order = Order.objects.create(user=request.user, ordered_date=ordered_date)
        order.item.add(order_item)
        messages.info(request, f"produit {item} ajouté")
    return redirect('produits:product_detail', myid=pk)            

@login_required
def add_single_to_card(request, pk):
    item = get_object_or_404(Produit, id=pk)
    order_item, created = OrderItem.objects.get_or_create(item=item, user=request.user, ordered=False)
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        if order.item.filter(item__id=item.id).exists():
            order_item.quantity +=1
            order_item.save()
            messages.info(request, f"{item}-quantité augmenté")  
            return redirect("produits:order-summary")  
        else:
            order.item.add(order_item)
            messages.success(request, f"produit {item} ajouté")    
    else:
        ordered_date  = timezone.now()
        order = Order.objects.create(user=request.user, ordered_date=ordered_date)
        order.item.add(order_item)
        messages.info(request, f"produit {item} ajouté")
    return redirect("produits:product", id=pk)      

@login_required
def remove_single_item_from_cart(request, pk):
    item = get_object_or_404(Produit, id=pk)
    order_qs = Order.objects.filter(
        user=request.user,
        ordered=False
    )
    if order_qs.exists():
        order = order_qs[0]
        # check if the order item is in the order
        if order.item.filter(item__id=item.pk).exists():
            order_item = OrderItem.objects.filter(
                item=item,
                user=request.user,
                ordered=False
            )[0]
            if order_item.quantity > 1:
                order_item.quantity -= 1
                order_item.save()
            else:
                order.item.remove(order_item)
            messages.info(request, "La quantité de cet article a été mise à jour.")
            return redirect("produits:order-summary")
        else:
            messages.info(request, "Cet article n'était pas dans votre panier")
            return redirect("produit:product", id=pk)
    else:
        messages.info(request, "Vous n'avez pas de commande active")
        return redirect("produits:product", id=pk)


def remove_from_card(request, pk):
    item = get_object_or_404(Produit, id=pk)
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        if order.item.filter(item__id=item.id).exists():
            order_item = OrderItem.objects.filter(item=item, user=request.user, ordered=False)[0]
            if order_item:
                order.item.remove(order_item)
                messages.info(request, f"produit {item} retiré")
                return redirect('produits:product_detail', myid=pk)
        else:
            messages.warning(request, f"Vous n'avez pas le produit {item} dans le parnier")
            return redirect('produits:product_detail', myid=pk)         
    else:
        messages.warning(request, f"Vous n'avez pas le produit {item} dans le parnier")
        return redirect('produits:product_detail', myid=pk) 


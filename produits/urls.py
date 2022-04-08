from django.urls import path
from produits.views import *

app_name = 'produits'
urlpatterns = [
    path('', index, name='home'),
    path('statistique', statistique, name='statistique'),

    #Seller
    path('list', product_seller_list, name='produtListSeller'),
    path('addproduct',  addProduct, name=' addproduct'),
    path('modifier/<int:pk>', EditViewProduct.as_view(), name='produit_detail'),
    path('supprimer/<int:pk>', DeleteViewProduct.as_view(), name='supprimmer_produit'),
    path('detail/<int:myid>/', detail, name="product_detail"),
    path('checkout/<int:id>', checkout, name='checkout'),
    path('confirmation', confimation, name='confirmation'),
    #Admin
    path('allproduct', product_sellers_list, name='allproducts'),
    path('profile', profile, name='profile'),
    path('modif/<int:pk>', UserEditView.as_view(), name='user_detail'),

    

]
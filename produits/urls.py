from django.urls import path
from produits.views import *

app_name = 'produits'
urlpatterns = [
    path('', home, name='home'),
    path('statistique', statistique, name='statistique'),

    #Seller
    path('list', product_seller_list, name='produtListSeller'),
    path('addproduct',  addProduct, name=' addproduct'),
    path('modifier/<int:pk>', EditViewProduct.as_view(), name='produit_detail'),
    path('supprimer/<int:pk>', DeleteViewProduct.as_view(), name='supprimmer_produit'),

    #Admin
    path('allproduct', product_sellers_list, name='allproducts'),
    path('profile', profile, name='profile'),
    path('modif/<int:pk>', UserEditView.as_view(), name='user_detail'),

    

]
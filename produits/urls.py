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

    # Clients
    path('detail/<int:myid>/', detail, name="product_detail"),
    path('add_single_to_card/<int:pk>/', add_single_to_card, name='add_single_to_card'),
    path('categories/<int:pk>/',  all_categories, name='categories'),
    path('add_to_card/<int:pk>/', add_to_card, name='add_to_card'),
    path('remove_single_item_from_cart/<int:pk>', remove_single_item_from_cart, name="remove_single_item_from_cart"),
    path('remove_from_card/<int:pk>/', remove_from_card, name='remove_from_card'),
    path('checkout/<int:id>', checkout, name='checkout'),
    path('confirmation', confimation, name='confirmation'),
    path('order-summary', OrderSummary.as_view(), name="order-summary"),

    #Admin
    path('allproduct', product_sellers_list, name='allproducts'),
    path('profile', profile, name='profile'),
    path('modif/<int:pk>', UserEditView.as_view(), name='user_detail'),

    

]
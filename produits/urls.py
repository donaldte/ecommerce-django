from django.urls import path
from produits.views import *

app_name = 'produits'
urlpatterns = [
    path('', home, name='home'),
    path('statistique', statistique, name='statistique'),
]

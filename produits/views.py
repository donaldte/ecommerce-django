from django.shortcuts import render

# Create your views here.

#home page 
def home(request):
    return render(request, 'produits/index.html')



#statistique des achats
def statistique(request):
    return render(request, 'statistique/index.html')    

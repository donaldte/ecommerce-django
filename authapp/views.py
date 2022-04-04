from django.http import request
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from .forms import UserRegistration, UserEditForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required


# Create your views here.

@login_required(login_url='/login')
def dashboard(request):
    context = {
        "welcome": "Welcome to your dashboard"
    }
    return render(request, 'seller/index.html', context=context)


def register(request):
    if request.method == 'POST':
        form = UserRegistration(request.POST or None)
        if form.is_valid():
            form.save()
            return render(request, 'authapp/register_done.html')
    else:
        form = UserRegistration()

    context = {
        "form": form
    }

    return render(request, 'authapp/register.html', context=context)

def signIn(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        print(username, password)
        user = authenticate(request, username=username, password=password)
        if user is not None and user.is_active:
            login(request, user)
            if user.peut_vendre:
                if 'next' in request.POST:
                    return redirect(request.POST.get('next'))    
                return render(request, 'seller/index.html')
            else:
                return render(request, 'authapp/peux_pas_vendre.html')   
        
    return render(request, 'registration/log.html')

@login_required
def logoutuser(request):
    logout(request)
    return redirect('/auth')    

@login_required(login_url='/login')
def edit(request):
    if request.method == 'POST':
        user_form = UserEditForm(instance=request.user,
                                 data=request.POST)
        if user_form.is_valid():
            user_form.save()
    else:
        user_form = UserEditForm(instance=request.user)
    context = {
        'form': user_form,
    }
    return render(request, 'authapp/edit.html', context=context)

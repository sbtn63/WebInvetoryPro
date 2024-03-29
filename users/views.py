from django.shortcuts import render, redirect
from django.db import IntegrityError
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages

from .forms import RegisterUserForm, LoginUserForm

def login_view(request):
    if request.method == 'GET':
        return render(request, 'pages/users/login.html', context={'form' : LoginUserForm})
    
    else:
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        
        if user is None:
            messages.warning(request, 'El usuario o la cotraseña no son validos!')
            return render(request, 'pages/users/login.html', context={'form' : LoginUserForm})
        else:
            login(request, user)
            return redirect('products:sale_products')

def register_view(request):
    if request.method == 'GET':
        return render(request, 'pages/users/register.html', context={'form' : RegisterUserForm})
        
    else:
        if request.POST['password1'] == request.POST['password2']:
            
            try:
                new_user = User.objects.create_user(username=request.POST['username'], password=request.POST['password1'])
                new_user.save()
                login(request, new_user)
                messages.success(request, 'Usuario registrado correctamente!')
                return redirect('products:sale_products')
            
            except IntegrityError:
                messages.warning(request, 'El usuario ya existe!')
                return render(request, 'pages/users/register.html', context={'form' : RegisterUserForm})
          
        messages.warning(request, 'Las Contraseñas no coinciden!')      
        return render(request, 'pages/users/register.html', context={'form' : RegisterUserForm})

def logout_view(request):
    logout(request)
    return redirect('home')
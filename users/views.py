from django.shortcuts import render, redirect
from django.db import IntegrityError
from django.views import View
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages

from .forms import RegisterUserForm, LoginUserForm


class LoginView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'pages/users/login.html', context={'form' : LoginUserForm})
    
    def post(self, request, *args, **kwargs):
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        
        if user is None:
            messages.warning(request, 'El usuario o la cotraseña no son validos!')
            return render(request, 'pages/users/login.html', context={'form' : LoginUserForm})
        else:
            login(request, user)
            return redirect('products:sale_products')

class RegisterView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'pages/users/register.html', context={'form' : RegisterUserForm})
    
    def post(self, request, *args, **kwargs):
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

class LogoutView(View):
    def get(self, request, *args, **kwargs):
        logout(request)
        return redirect('home')
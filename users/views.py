""" Importaciones necesarias para la vista de inicio de sesión """

# Importa funciones para renderizar plantillas y redirigir a otras vistas
from django.shortcuts import render, redirect

# Importa la clase base para vistas basadas en clases
from django.views import View

# Importa funciones para manejar la autenticación de usuarios
from django.contrib.auth import login, logout

# Importa el módulo para mostrar mensajes de usuario
from django.contrib import messages

# Importa los formularios personalizados para el registro y el inicio de sesión de usuarios
from .forms import RegisterUserForm, LoginUserForm


class LoginView(View):
    """
    Vista para gestionar el inicio de sesión de los usuarios.
    """

    def get(self, request):
        """
        Muestra el formulario de inicio de sesión.

        Parámetros:
        - request: Objeto HttpRequest que contiene datos de la solicitud.

        Retorna:
        - Renderiza la plantilla de inicio de sesión con un formulario vacío.
        """
        return render(request, 'pages/users/login.html', context={'form': LoginUserForm})

    def post(self, request):
        """
        Procesa el formulario de inicio de sesión y autentica al usuario.

        Parámetros:
        - request: Objeto HttpRequest que contiene los datos del formulario.

        Retorna:
        - Redirige a la página de productos si el inicio de sesión es exitoso.
        - Renderiza nuevamente el formulario de inicio de sesión con mensajes de 
        advertencia si los datos son inválidos.
        """
        form = LoginUserForm(request, request.POST)

        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('products:sale_products')

        messages.warning(request, 'El usuario o la contraseña no son válidos!')
        return render(request, 'pages/users/login.html', context={'form': form})


class RegisterView(View):
    """
    Vista para gestionar el registro de nuevos usuarios.
    """

    def get(self, request):
        """
        Muestra el formulario de registro de usuario.

        Parámetros:
        - request: Objeto HttpRequest que contiene datos de la solicitud.

        Retorna:
        - Renderiza la plantilla de registro con un formulario vacío.
        """
        return render(request, 'pages/users/register.html', context={'form': RegisterUserForm})

    def post(self, request):
        """
        Procesa el formulario de registro y crea un nuevo usuario.

        Parámetros:
        - request: Objeto HttpRequest que contiene los datos del formulario.

        Retorna:
        - Redirige a la página de productos si el registro es exitoso y 
        el usuario inicia sesión automáticamente.
        - Renderiza nuevamente el formulario de registro con los errores si los datos son inválidos.
        """
        form = RegisterUserForm(request.POST)

        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Usuario registrado correctamente!')
            return redirect('products:sale_products')

        return render(request, 'pages/users/register.html', context={'form': form})


class LogoutView(View):
    """
    Vista para gestionar el cierre de sesión de los usuarios.
    """

    def get(self, request):
        """
        Cierra la sesión del usuario y redirige a la página de inicio.

        Parámetros:
        - request: Objeto HttpRequest que contiene datos de la solicitud.

        Retorna:
        - Redirige al usuario a la página de inicio después de cerrar la sesión.
        """
        logout(request)
        return redirect('home')

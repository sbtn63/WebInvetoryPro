""" Importaciones necesarias para la vista de inicio de sesión """

# Importa funciones para renderizar plantillas y redirigir a otras vistas
from django.shortcuts import render, redirect

# Importa la clase base para vistas basadas en clases
from django.views import View

# Importa funciones para manejar la autenticación de usuarios
from django.contrib.auth import login, logout

# Importa el módulo para mostrar mensajes de usuario
from django.contrib import messages

# Importa `authenticate` y `update_session_auth_hash` para gestionar la autenticación del usuario.
from django.contrib.auth import authenticate, update_session_auth_hash

# Importa los formularios personalizados para el registro y el inicio de sesión de usuarios
from .forms import RegisterUserForm, LoginUserForm, UserChangeInfoForm


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


class UserChangeInfoView(View):
    """
    Vista para gestionar la actualización de la información del usuario.

    Esta vista permite a los usuarios cambiar su nombre de usuario, dirección 
    de correo electrónico y contraseña.
    """
    def get(self, request):
        """
        Muestra el formulario de actualización de usuario.

        Este método maneja las solicitudes GET y renderiza el formulario para que 
        el usuario pueda ingresar los datos que desea actualizar.

        Parámetros:
        - request: Objeto HttpRequest que contiene datos de la solicitud.

        Retorna:
        - Renderiza la plantilla de actualización de usuario con un formulario vacío o 
        prellenado con los datos actuales.
        """
        form = UserChangeInfoForm(instance=request.user, current_user=request.user)
        return render(request, 'pages/users/change.html', context={'form': form})

    def post(self, request):
        """
        Procesa el formulario de actualización de usuario.

        Este método maneja las solicitudes POST, valida el formulario y actualiza 
        la información del usuario si los datos son válidos. También maneja la autenticación 
        de la contraseña actual antes de realizar cambios en la cuenta del usuario.

        Parámetros:
        - request: Objeto HttpRequest que contiene datos de la solicitud, incluyendo los 
        datos del formulario.

        Retorna:
        - Si el formulario es válido y la contraseña actual es correcta:
          Redirige al usuario con un mensaje de éxito.
        - Si la contraseña actual no es correcta:
          Redirige al usuario con un mensaje de error.
        - Si el formulario no es válido:
          Renderiza la plantilla de actualización con el formulario y los errores.
        """
        current_username = request.user.username
        form = UserChangeInfoForm(request.POST, instance=request.user, current_user=request.user)
        if form.is_valid():
            current_password = form.cleaned_data.get('current_password')
            new_username = form.cleaned_data.get('username')
            new_email = form.cleaned_data.get('email')
            new_password = form.cleaned_data.get('password_new')
            user = authenticate(username=current_username, password=current_password)
            if user is not None:
                if new_username and new_username != request.user.username:
                    request.user.username = new_username
                if new_email and new_email != request.user.email:
                    request.user.email = new_email
                if new_password:
                    request.user.set_password(new_password)
                    update_session_auth_hash(request, request.user)
                request.user.save()
                messages.success(request, 'Usuario actualizado correctamente!')
                return redirect('users:change')
            else:
                messages.error(request, 'La contraseña actual no es correcta!')
                return redirect('users:change')
        return render(request, 'pages/users/change.html', context={'form': form})


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

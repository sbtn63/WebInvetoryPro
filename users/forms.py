"""Importaciones necesarias para los formularios"""

# Importa el módulo forms de Django para la creación de formularios
from django import forms

# Importa formularios específicos para la creación y autenticación de usuarios, así como el modelo de usuario
from django.contrib.auth.forms import (
    UserCreationForm,   # Formulario para el registro de nuevos usuarios
    AuthenticationForm, # Formulario para la autenticación de usuarios
    User                # Modelo de usuario de Django
)


class RegisterUserForm(UserCreationForm):
    """
    Formulario para el registro de nuevos usuarios.

    Hereda de UserCreationForm e incluye los campos para el nombre de usuario 
    y las contraseñas (password1 y password2). Los mensajes de ayuda para los 
    campos están vacíos.
    """

    class Meta:
        """
        Clase interna que proporciona metainformación sobre el formulario.

        Define el modelo asociado al formulario y los campos que deben 
        incluirse en el formulario. Los mensajes de ayuda para los campos 
        están configurados para no mostrar ningún texto adicional.
        """
        model = User
        fields = ['username', 'password1', 'password2']
        help_texts = {k: "" for k in fields}


class LoginUserForm(AuthenticationForm):
    """
    Formulario para la autenticación de usuarios existentes.

    Hereda de AuthenticationForm e incluye los campos para el nombre de usuario 
    y la contraseña.
    """

    class Meta:
        """
        Clase interna que proporciona metainformación sobre el formulario.

        Define el modelo asociado al formulario y los campos que deben 
        incluirse en el formulario. No se configuran mensajes de ayuda para los 
        campos en este formulario.
        """
        model = User
        fields = ['username', 'password']

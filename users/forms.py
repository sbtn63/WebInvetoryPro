"""Importaciones necesarias para los formularios"""

# Importa el módulo forms de Django para la creación de formularios
from django import forms

# Importa formularios específicos para la creación y autenticación de usuarios, 
# así como el modelo de usuario
from django.contrib.auth.forms import (
    UserCreationForm,   # Formulario para el registro de nuevos usuarios
    AuthenticationForm, # Formulario para la autenticación de usuarios
    User,                # Modelo de usuario de Django
)

# Importa ValidationError que se utiliza para lanzar excepciones de Validación.
from django.core.exceptions import ValidationError

# Importa validate_password verificar politicas de seguridad contraseñas.
from django.contrib.auth.password_validation import validate_password


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

class UserChangeInfoForm(forms.ModelForm):
    """
    Un formulario para cambiar la información del usuario y actualizar la contraseña.
        
    Campos del formulario:
    - username: Nombre de usuario (opcional, mínimo 3 caracteres).
    - email: Dirección de correo electrónico (requerido).
    - current_password: Contraseña actual (requerida, mínimo 8 caracteres).
    - password_new: Nueva contraseña (opcional, mínimo 8 caracteres).
    - password_new_confirm: Confirmación de la nueva contraseña (opcional, mínimo 8 caracteres).
    """
    username = forms.CharField(
        min_length=3,
        required=False
    )
    email = forms.EmailField()
    current_password = forms.CharField(
        widget=forms.PasswordInput(),
        min_length=8
    )
    password_new = forms.CharField(
        widget=forms.PasswordInput(),
        required=False,
        min_length=8
    )
    password_new_confirm = forms.CharField(
        widget=forms.PasswordInput(),
        required=False,
        min_length=8
    )

    class Meta:
        """
        Metadatos para el formulario UserChangeInfoForm.
        
        Atributos:
        - model: El modelo asociado con este formulario. En este caso, el modelo User.
        - fields: Lista de campos del modelo que se incluyen en el formulario. 
                Incluye 'username', 'email', 'password_new', 
                'current_password', y 'password_new_confirm'.
        - help_texts: Diccionario para proporcionar textos de ayuda adicionales para los campos 
                    del formulario. En este caso, todos los textos de ayuda se establecen 
                    como cadenas vacías.
        """
        model = User
        fields = ['username', 'email', 'password_new', 'current_password', 'password_new_confirm']
        help_texts = {k: "" for k in fields}

    def __init__(self, *args, **kwargs):
        """
        Inicializa el formulario y extrae el usuario actual de los argumentos.
        
        :param args: Argumentos posicionales.
        :param kwargs: Argumentos de palabra clave, se espera que 
                    'current_user' sea uno de ellos.
        """
        self.current_user = kwargs.pop('current_user', None)
        super().__init__(*args, **kwargs)

    def clean_username(self):
        """
        Valida el campo de nombre de usuario para asegurarse de que no 
        esté en uso por otro usuario.
        
        :raises ValidationError: Si el nombre de usuario ya está en uso.
        :return: El nombre de usuario limpio.
        """
        username = self.cleaned_data.get('username')
        if username and username != self.current_user.username:
            if User.objects.exclude(pk=self.current_user.pk).filter(username=username).exists():
                raise ValidationError("El nombre de usuario ya está en uso.")
        return username

    def clean(self):
        """
        Valida los campos del formulario, incluyendo la coincidencia de las contraseñas
        y la validez de la nueva contraseña.
        
        :return: Los datos limpios del formulario.
        """
        cleaned_data = super().clean()
        password_new = cleaned_data.get('password_new')
        password_new_confirm = cleaned_data.get('password_new_confirm')
        if password_new or password_new_confirm:
            if not password_new:
                self.add_error('password_new', 'Debes proporcionar la nueva contraseña.')
            if not password_new_confirm:
                self.add_error('password_new_confirm', 'Debes confirmar la nueva contraseña.')
            if password_new and password_new_confirm and password_new != password_new_confirm:
                self.add_error('password_new_confirm', 'Las contraseñas no coinciden.')
            if password_new:
                try:
                    validate_password(password_new)
                except ValidationError as e:
                    self.add_error('password_new', e)
        return cleaned_data

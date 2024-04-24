from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, User

class RegisterUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']
        help_texts = {k:"" for k in fields}

class LoginUserForm(AuthenticationForm):    
    class Meta:
        model = User
        fields = ['username', 'password']
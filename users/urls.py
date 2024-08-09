""" Importaciones necesarias para las URLs """

# Importa la función path para definir rutas en la aplicación
from django.urls import path

# Importa las vistas necesarias para las rutas de autenticación
from .views import (
    LoginView,      # Vista para el inicio de sesión
    RegisterView,   # Vista para el registro de nuevos usuarios
    LogoutView,     # Vista para el cierre de sesión
)

# Define las rutas URL para las vistas de autenticación
urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('register/', RegisterView.as_view(), name='register'),
    path('logout/', LogoutView.as_view(), name='logout'),
]

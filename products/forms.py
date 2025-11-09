"""Importaciones necesarias para los formularios"""

# Importa el módulo de formularios de Django
from django import forms

# Importa el modelo Product para usarlo en los formularios
from .models import Product


class CalendarForm(forms.Form):
    """
    Formulario para seleccionar una fecha usando un widget de selección de fecha.

    Campos:
    - date: Campo de fecha con un widget para seleccionar año, mes y día.
    """

    date = forms.DateField(
        # Widget para seleccionar la fecha con opciones para el año
        widget=forms.SelectDateWidget(years=range(2023, 2034)),
        # Formatos de entrada aceptados para la fecha
        input_formats=["%Y-%m-%d", "%d/%m/%Y"],
    )


class ProductForm(forms.ModelForm):
    """
    Formulario para crear y actualizar productos.

    Campos:
    - name: Nombre del producto.
    - price: Precio del producto.
    - stock: Cantidad del producto en stock.
    """

    class Meta:
        """
        Configuración de la clase Meta para el formulario ProductForm.

        Model:
        - Product: El modelo al que se refiere este formulario.

        Fields:
        - name: Nombre del producto.
        - price: Precio del producto.
        - stock: Cantidad del producto en stock.
        """

        model = Product
        fields = ["name", "price", "stock"]


class UpdateProductForm(forms.ModelForm):
    """
    Formulario para actualizar productos existentes.

    Campos:
    - name: Nombre del producto.
    - price: Precio del producto.
    - stock: Cantidad del producto en stock.
    """

    class Meta:
        """
        Configuración de la clase Meta para el formulario UpdateProductForm.

        Model:
        - Product: El modelo al que se refiere este formulario.

        Fields:
        - name: Nombre del producto.
        - price: Precio del producto.
        - stock: Cantidad del producto en stock.
        """

        model = Product
        fields = ["name", "price", "stock"]

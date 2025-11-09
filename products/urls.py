"""Importaciones necesarias para las URLs"""

# Importa la función path para definir rutas en la aplicación
from django.urls import path

# Importaciones locales desde el archivo de vistas
from .views import (
    SaleProductsView,  # Vista para mostrar productos en venta
    SaleProductsHistoryView,  # Vista para mostrar el historial de productos en venta
    SaleProductUpdateView,  # Vista para actualizar un producto específico
    SaleProductDeleteView,  # Vista para eliminar un producto específico
)


# Define las rutas URL para las vistas de productos
urlpatterns = [
    path("", SaleProductsView.as_view(), name="sale_products"),
    path("history/", SaleProductsHistoryView.as_view(), name="sale_products_history"),
    path(
        "update/<int:pk>", SaleProductUpdateView.as_view(), name="update_sale_product"
    ),
    path(
        "delete/<int:pk>", SaleProductDeleteView.as_view(), name="delete_sale_product"
    ),
]

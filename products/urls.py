from django.urls import path

from .views import (
    SaleProductsView,
    SaleProductsHistoryView,
    SaleProductUpdateView,
    SaleProductDeleteView,
)


urlpatterns = [
    path('', SaleProductsView.as_view(), name='sale_products'),
    path('history/', SaleProductsHistoryView.as_view(), name="sale_products_history"),
    path('update/<int:pk>', SaleProductUpdateView.as_view(), name='update_sale_product'),
    path('delete/<int:pk>', SaleProductDeleteView.as_view(), name='delete_sale_product'),
]

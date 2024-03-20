from django.urls import path

from .views import (
    sale_products_view,
    sale_products_history_view,
    sale_product_update_view,
    sale_product_delete_view,
)


urlpatterns = [
    path('', sale_products_view, name='sale_products'),
    path('history/', sale_products_history_view, name="sale_products_history"),
    path('update/<int:pk>', sale_product_update_view, name='update_sale_product'),
    path('delete/<int:pk>', sale_product_delete_view, name='delete_sale_product'),
]

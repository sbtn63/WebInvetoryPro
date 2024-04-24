from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('home/', TemplateView.as_view(template_name='pages/core/home.html'), name='home'),
    path('', include(('products.urls', 'products'))),
    path('users/', include(('users.urls', 'users'))),
]

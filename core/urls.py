from django.contrib import admin
from django.urls import path, include

from .views import home_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('home/', home_view, name='home'),
    path('', include(('products.urls', 'products'))),
    path('users/', include(('users.urls', 'users'))),
]

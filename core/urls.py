"""  Importaciones de módulos de Django """
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from django.views.generic import TemplateView

# Definición de las URLs del proyecto
urlpatterns = [
    path('admin/', admin.site.urls),
    path('home/', TemplateView.as_view(template_name='pages/core/home.html'), name='home'),
    path('', include(('products.urls', 'products'))),
    path('users/', include(('users.urls', 'users'))),
]


# Configuración para servir archivos estáticos durante el desarrollo
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    
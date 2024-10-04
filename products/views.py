"""Importaciones necesarias para las vistas"""

# Importa funciones para la renderización de plantillas y redirección
from django.shortcuts import render, redirect, get_object_or_404

# Importa utilidades para manejar la zona horaria
from django.utils import timezone
#from datetime import datetime

# Importa la clase base para vistas basadas en clases
from django.views import View

# Importa mixins para requerir autenticación de usuarios
from django.contrib.auth.mixins import LoginRequiredMixin

# Importa el módulo para mostrar mensajes de usuario
from django.contrib import messages

# Importa el paginador para manejar la paginación de resultados
from django.core.paginator import Paginator

# Importa el módulo para manejar errores HTTP
from django.http import Http404

# Importa los modelos y formularios específicos de la aplicación
from .models import Product
from .forms import ProductForm, UpdateProductForm, CalendarForm


def pagination_products(products, page, amount):
    """
    Paginación de productos para la vista.

    Parámetros:
    - products: QuerySet de productos a paginar.
    - page: Número de página actual.
    - amount: Cantidad de productos por página.

    Retorna:
    - products: Productos de la página actual.
    - paginator: Objeto Paginator utilizado para la paginación.

    Lanza:
    - Http404: Si ocurre un error en la paginación.
    """
    try:
        paginator = Paginator(products, amount)
        products = paginator.page(page)
        return products, paginator
    except:
        # Lanza una excepción Http404 si ocurre un error
        raise Http404

def total_sale(products):
    """
    Calcula el total de ventas de una lista de productos.

    Esta función toma un QuerySet de productos y calcula el total 
    de ventas multiplicando el precio de cada producto por su cantidad 
    en stock y sumando estos valores.

    Parámetros:
    - products (QuerySet): Un conjunto de productos, donde cada producto 
    tiene atributos de precio (price) y cantidad en stock (stock).

    Retorna:
    - float: La suma total del valor en ventas de todos los productos en el QuerySet.
    """
    return sum(product.price * product.stock for product in products)


class SaleProductsView(LoginRequiredMixin, View):
    """
    Vista para gestionar la venta de productos.
    """

    def get_queryset(self, request):
        """
        Obtiene los productos de venta del usuario para la fecha actual.

        Parámetros:
        - request: Objeto HttpRequest que contiene los datos de la solicitud.

        Retorna:
        - Queryset de productos filtrados por usuario y fecha actual.
        """
        current_date = timezone.now()
        products = Product.objects.filter(
            user=request.user,
            sale_date__date=current_date
        )
        return products

    def get(self, request):
        """
        Muestra la lista de productos con el formulario para agregar nuevos productos.

        Parámetros:
        - request: Objeto HttpRequest que contiene los datos de la solicitud.

        Retorna:
        - Renderiza la plantilla de productos con los datos necesarios.
        """
        form = ProductForm(initial={'stock': 1})
        products = self.get_queryset(request)
        consult = request.GET.get('search', '')
        page = request.GET.get('page', 1)
        sale = total_sale(products)

        if consult and len(consult) >= 3:
            products = products.filter(name__icontains=consult)
            paginator = None
        else:
            products, paginator = pagination_products(products, page, 4)

        context = {
            "products": products,
            "paginator": paginator,
            "form": form,
            "sale": sale,
            "current_date": timezone.now(),
        }
        return render(request, 'pages/products/sale_products.html', context)

    def post(self, request):
        """
        Procesa el formulario para agregar un nuevo producto.

        Parámetros:
        - request: Objeto HttpRequest que contiene los datos del formulario.

        Retorna:
        - Redirige a la vista de productos con un mensaje de éxito o advertencia.
        """
        form = ProductForm(request.POST, initial={'stock': 1})
        products = self.get_queryset(request)

        if form.is_valid():
            form.instance.user = request.user
            existing_product = products.filter(
                name__iexact=form.instance.name
            ).first()
            if existing_product:
                messages.info(
                    request,
                    f"El producto {existing_product.name} ya existe"
                )
                return redirect("products:update_sale_product", pk=existing_product.id)
            form.save()
            messages.success(
                request,
                f"El producto {form.instance.name} ha sido creado!"
            )
            return redirect("products:sale_products")

        messages.warning(request, "Los datos son inválidos")
        return redirect("products:sale_products")


class SaleProductsHistoryView(LoginRequiredMixin, View):
    """
    Vista para mostrar el historial de productos vendidos basado en una fecha seleccionada.

    Métodos:
    - get: Renderiza la vista con el historial de productos vendidos en la fecha seleccionada.
    - post: Actualiza la fecha del historial en la sesión y redirige a la vista actualizada.
    """

    def get(self, request):
        """
        Muestra el historial de productos vendidos en una fecha específica.

        Parámetros:
        - request: Objeto HttpRequest que contiene los datos de la solicitud.

        Retorna:
        - Renderiza la plantilla con la lista de productos vendidos, 
        el formulario de selección de fecha,
          y el total de ventas para la fecha seleccionada.
        """
        session = request.session
        date = session.get('date_history', timezone.localtime(timezone.now()).date())
        form = CalendarForm(initial={'date': date})
        consult = request.GET.get('search', '')
        products = Product.objects.filter(user=request.user, sale_date__date=date)
        page = request.GET.get('page', 1)
        sale = total_sale(products)

        if consult and len(consult) >= 3:
            products = products.filter(name__icontains=consult)
            paginator = None
        else:
            products, paginator = pagination_products(products, page, 4)

        context = {
            "products": products,
            "paginator": paginator,
            "sale": sale,
            "form": form,
            #"date": datetime.strptime(date, '%Y-%m-%d').date() 
            "date" : date
        }
        return render(request, 'pages/products/sale_products_history.html', context)

    def post(self, request):
        """
        Actualiza la fecha del historial de productos en la sesión y 
        redirige a la vista actualizada.

        Parámetros:
        - request: Objeto HttpRequest que contiene los datos del formulario.

        Retorna:
        - Redirige a la vista de historial de productos si el formulario es válido.
        - Muestra un mensaje de advertencia y redirige a la vista si el formulario es inválido.
        """
        form = CalendarForm(request.POST)

        if form.is_valid():
            date = form.cleaned_data['date']
            request.session['date_history'] = date.isoformat()
            return redirect('products:sale_products_history')

        messages.warning(request, "Los datos son inválidos")
        return redirect('products:sale_products_history')


class SaleProductUpdateView(LoginRequiredMixin, View):
    """
    Vista para actualizar un producto en las ventas.

    Métodos:
    - get_product: Recupera un producto específico para el usuario.
    - get: Renderiza la vista para actualizar un producto existente.
    - post: Procesa la actualización del producto y maneja la respuesta.
    """

    def get_product(self, request, pk):
        """
        Recupera un producto específico basado en el identificador proporcionado 
        y el usuario actual.

        Parámetros:
        - request: Objeto HttpRequest que contiene los datos de la solicitud.
        - pk: Identificador del producto a recuperar.

        Retorna:
        - Un objeto Product si se encuentra el producto; de lo contrario, devuelve un error 404.
        """
        return get_object_or_404(Product, user=request.user, pk=pk)

    def get(self, request, pk):
        """
        Muestra el formulario para actualizar un producto existente.

        Parámetros:
        - request: Objeto HttpRequest que contiene los datos de la solicitud.
        - pk: Identificador del producto a actualizar.

        Retorna:
        - Renderiza la plantilla con el formulario prellenado para actualizar el producto.
        """
        product = self.get_product(request, pk)
        form = UpdateProductForm(instance=product)
        context = {'form': form, 'product': product}
        return render(request, 'pages/products/update_sale_product.html', context)

    def post(self, request, pk):
        """
        Procesa la actualización del producto con los datos del formulario.

        Parámetros:
        - request: Objeto HttpRequest que contiene los datos del formulario.
        - pk: Identificador del producto a actualizar.

        Retorna:
        - Redirige a la lista de productos si el formulario es válido.
        - Renderiza la plantilla de actualización del producto con mensajes 
        de advertencia si el formulario es inválido.
        """
        product = self.get_product(request, pk)
        form = UpdateProductForm(request.POST, instance=product)

        if form.is_valid():
            form.instance.user = request.user
            form.save()
            messages.success(request, f"El producto {form.instance.name} ha sido actualizado!")
            return redirect("products:sale_products")

        messages.warning(request, "Los datos son inválidos!")
        context = {'form': form, 'product': product}
        return render(request, 'pages/products/update_sale_product.html', context)

class SaleProductDeleteView(LoginRequiredMixin, View):
    """
    Vista para eliminar un producto de las ventas.

    Métodos:
    - get: Elimina un producto específico basado en el identificador proporcionado.
    """

    def get(self, request, pk):
        """
        Elimina el producto especificado por el identificador proporcionado.

        Parámetros:
        - request: Objeto HttpRequest que contiene los datos de la solicitud.
        - pk: Identificador del producto a eliminar.

        Retorna:
        - Redirige a la lista de productos con un mensaje de confirmación de eliminación.
        """
        product = get_object_or_404(Product, user=request.user, pk=pk)
        messages.info(request, f"El producto {product.name} ha sido eliminado!")
        product.delete()
        return redirect("products:sale_products")

from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.core.paginator import Paginator
from django.http import Http404

from .models import Product
from .forms import ProductForm, UpdateProductForm, CalendarForm

class SaleProductsView(LoginRequiredMixin, View):
    def get_queryset(self, request):
        current_date = timezone.now()
        products = Product.objects.filter(user=request.user, sale_date__date=current_date)
        return products
    
    def get(self, request, *args, **kwargs):
        form = ProductForm(initial={'stock': 1})
        products = self.get_queryset(request)
        consult = request.GET.get('search')
        page = request.GET.get('page', 1)
        
        if consult: products = products.filter(name__icontains=consult)
        
        sale = sum(product.price * product.stock for product in products)
        
        if not consult: products, paginator = pagination_products(products, page, 4)   
        else: paginator = None
        
        context = {
            "products": products,
            "paginator" : paginator,
            "form": form,
            "sale": sale,
            "current_date": timezone.now(),
        }
        
        return render(request, 'pages/products/sale_products.html', context)
    
    def post(self, request, *args, **kwargs):
        form = ProductForm(request.POST, initial={'stock': 1})
        products = self.get_queryset(request)
        
        if form.is_valid():
            form.instance.user = request.user
            existing_product = products.filter(name__iexact=form.instance.name).first()
            
            if existing_product:
                messages.info(request, f"El producto {existing_product.name} ya existe")
                return redirect("products:update_sale_product", pk=existing_product.id)
            
            form.save()
            messages.success(request, f"El producto {form.instance.name} ha sido creado!")
            return redirect("products:sale_products")
        else:
            messages.warning(request, "Los datos son inválidos")
            return redirect("products:sale_products")

class SaleProductsHistoryView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        session = request.session
        date = session.get('date_history', timezone.localtime(timezone.now()).date())
        form = CalendarForm(initial={'date': date})
        consult = request.GET.get('search')
        products = Product.objects.filter(user=request.user, sale_date__date=date)
        page = request.GET.get('page', 1)
        
        if consult: products = products.filter(name__icontains=consult)

        sale = sum([product.price * product.stock for product in products])
        
        if not consult: products, paginator = pagination_products(products, page, 4)   
        else: paginator = None
        
        context = {
            "products": products,
            "paginator" : paginator,
            "sale": sale,
            "form": form,
            "date": date
        }
        
        return render(request, 'pages/products/sale_products_history.html', context)
    
    def post(self, request, *args, **kwargs):
        form = CalendarForm(request.POST)
        
        if form.is_valid():
            date = form.cleaned_data['date']
            request.session['date_history'] = date.isoformat()
            return redirect('products:sale_products_history')
        
        messages.warning(request, "Los datos son inválidos")
        return redirect('products:sale_products_history')
    
class SaleProductUpdateView(LoginRequiredMixin, View):
    def get_product(self, request, pk):
        return get_object_or_404(Product, user=request.user, pk=pk)
    
    def get(self, request, pk, *args, **kwargs):
        product = self.get_product(request, pk)
        form = UpdateProductForm(instance=product)
        context = {'form': form, 'product': product}
        return render(request, 'pages/products/update_sale_product.html', context)
    
    def post(self, request, pk, *args, **kwargs):
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
    def get(self, request, pk, *args, **kwargs):
       product = get_object_or_404(Product, user=request.user, pk=pk) 
       messages.info(request, f"El producto {product.name} ha sido eliminado!")
       product.delete()
       return redirect("products:sale_products")
   
def pagination_products(products, page, amount):
    try:
        paginator = Paginator(products, amount)
        products = paginator.page(page)
        return products, paginator
    except:
        raise Http404
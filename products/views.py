from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from django.db.models import Q
from django.contrib.sessions.models import Session
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from .models import Product
from .forms import ProductForm, UpdateProductForm, CalendarForm

# Create your views here.

@login_required
def sale_products_view(request):
    current_date = timezone.now()
    form = ProductForm(request.POST or None, initial={'stock': 1})
    products = Product.objects.filter(user=request.user, sale_date__date=current_date)
    consult = request.GET.get('search')
    
    sale = 0
    
    for product in products:
        sale += product.price * product.stock
          
    if request.method == 'POST':
        
        if form.is_valid():
            new_product = form.save(commit=False)
            new_product.user = request.user
            
            if new_product.price < 50 and new_product.stock < 1:
                messages.warning(request, "Error, Los datos precio y cantidad son incorrectos!")
                
            elif new_product.price < 50:
                 messages.warning(request, "Error, El precio debe ser mayor a 50!")
                 
            elif new_product.stock < 1:
                 messages.warning(request, "Error, La cantidad debe ser mayor a 1!")
            
            else:
                
                for product in products:
                    if new_product.name.replace(" ", "").lower() == product.name.replace(" ", "").lower():
                        messages.info(request, f"El producto {product.name} ya existe")
                        return redirect("products:update_sale_product", pk=product.id)
                
                messages.success(request, f"El producto {new_product.name} ha sido creado!")
                new_product.save()
                return redirect("products:sale_products")
        
        else:
            messages.warning(request, "Los datos son invalidos")
    
    if consult:
        products = Product.objects.filter(Q(name__icontains=consult), user=request.user, sale_date__date=current_date)
        
    context = {
        "products" : products,
        "form" : form,
        "sale" : sale,
        "current_date": current_date,
    }
    
    return render(request, 'pages/products/sale_products.html', context)

@login_required
def sale_products_history_view(request):
    date = timezone.localtime(timezone.now())
    date = date.strftime('%Y-%m-%d')
    form = CalendarForm(request.POST or None, initial={'date': date})
    products = Product.objects.filter(user=request.user, sale_date__date=date)
    consult = request.GET.get('search')
    session = request.session

    sale = 0
    
    if request.method == 'POST':
        if form.is_valid():
            date = form.cleaned_data['date']
            session['date_history'] = date.isoformat()
            products = Product.objects.filter(user=request.user, sale_date__date=date)
    
    if session.get('date_history'):
        date = session.get('date_history')
        products = Product.objects.filter(user=request.user, sale_date__date=date)
        form = CalendarForm(request.POST or None, initial={'date': date})
    
    for product in products:
        sale += product.price * product.stock
            
    
    if consult:
        products = Product.objects.filter(Q(name__icontains=consult), user=request.user, sale_date__date=date)
        
    context = {
        "products" : products,
        "sale" : sale,
        "form" : form,
        "date" : date
    }
    
    return render(request, 'pages/products/sale_products_history.html', context)
    

@login_required
def sale_product_update_view(request, pk):
    product = get_object_or_404(Product, user=request.user, pk=pk)
    form = UpdateProductForm(request.POST or None, instance=product)
    
    if request.method == 'POST':
        
        if form.is_valid():
            update_product = form.save(commit=False)
            
            if update_product.price < 50 and update_product.stock < 1:
                messages.warning(request, "Error, Los datos precio y cantidad son incorrectos!")
                
            elif update_product.price < 50:
                 messages.warning(request, "Error, El precio debe ser mayor a 50!")
                 
            elif update_product.stock < 1:
                 messages.warning(request, "Error, La cantidad debe ser mayor a 1!")
                 
            else:
                
                messages.success(request, f"El producto {update_product.name} ha sido actualizado!")
                update_product.save()
                return redirect("products:sale_products")
            
        else:
            messages.warning(request, "Los datos son invalidos!")
    
    context = {
        "form" : form,
        "product" : product,
    }

    return render(request, 'pages/products/update_sale_product.html', context)
  
@login_required  
def sale_product_delete_view(request, pk):
    product = get_object_or_404(Product, user=request.user, pk=pk)
    messages.info(request, f"El producto {product.name} ha sido eliminado!")
    product.delete()
    return redirect("products:sale_products")
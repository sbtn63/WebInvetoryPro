from django import forms

from .models import Product

class CalendarForm(forms.Form):
    date = forms.DateField(
        widget = forms.SelectDateWidget(
            years=range(2023, 2034)
        ),
        
        input_formats=['%Y-%m-%d', '%d/%m/%Y'],
    )
    
class ProductForm(forms.ModelForm):    
    class Meta:
        model = Product
        fields = ["name", "price", "stock"]

class UpdateProductForm(forms.ModelForm):        
    class Meta:
        model = Product
        fields = ["name", "price", "stock"]
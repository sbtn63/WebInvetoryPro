from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Product(models.Model):
    name = models.CharField(max_length=255) 
    price = models.PositiveIntegerField()
    stock = models.PositiveIntegerField(default=1)
    sale_date = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    
    class Meta:
        ordering = ['-sale_date']
    
    def __str__(self):
        return f'{self.name}'
    
    def total_sale(self):
        return f"{self.price * self.stock}"

"""Importa los módulos necesarios para definir el modelo Product"""

# Importa la clase base para los modelos de Django
from django.db import models

# Importa el modelo User para establecer una relación de clave foránea con el modelo Product
from django.contrib.auth.models import User

# Define el modelo Product para gestionar productos en la aplicación


class Product(models.Model):
    """
    Modelo para representar un producto en el sistema de ventas.

    Atributos:
    - name: Nombre del producto (maximo 255 caracteres).
    - price: Precio del producto (valor entero positivo).
    - stock: Cantidad disponible del producto (valor entero positivo, por defecto 1).
    - sale_date: Fecha y hora en que se añadió el producto (se establece automáticamente).
    - user: Usuario asociado al producto (clave foránea que hace referencia al modelo User).

    Métodos:
    - __str__: Devuelve una representación en cadena del nombre del producto.
    - total_sale: Calcula el total de la venta (precio * stock).
    """

    name = models.CharField(max_length=255)
    price = models.PositiveIntegerField()
    stock = models.PositiveIntegerField(default=1)
    sale_date = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        """
        Configuración adicional del modelo.

        Ordering:
        - Ordena los productos por fecha de venta en orden descendente.
        """

        ordering = ["-sale_date"]

    def __str__(self):
        """
        Retorna una representación en cadena del producto, que es su nombre.

        Retorna:
        - Nombre del producto.
        """
        return f"{self.name}"

    def total_sale(self):
        """
        Calcula el total de la venta del producto basado en el precio y la cantidad en stock.

        Retorna:
        - El total de la venta como una cadena formateada (precio * stock).
        """
        return f"{self.price * self.stock}"

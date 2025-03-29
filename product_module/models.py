from django.db import models
from engine.models import Module

class Product(models.Model):
    module = models.ForeignKey(Module, on_delete=models.CASCADE, related_name='products')
    name = models.CharField(max_length=100)
    barcode = models.CharField(max_length=50)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField()

    class Meta:
        unique_together = ('module', 'barcode')  # Barcode unik per modul

    def __str__(self):
        return self.name

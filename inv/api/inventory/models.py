from django.db import models

# Create your models here.
# inventory/models.py
from django.db import models
from api.product.models import Product
from api.warehouse.models import Warehouse

class Inventory(models.Model):
    warehouse = models.ForeignKey(
        Warehouse,
        on_delete=models.CASCADE,
        related_name='inventory_items'
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='inventory_entries'
    )
    quantity = models.PositiveIntegerField(default=0)
    reorder_level = models.PositiveIntegerField(default=10)
    last_updated = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('warehouse', 'product')  # One entry per product per warehouse
        verbose_name = "Inventory Item"
        verbose_name_plural = "Inventory"
        ordering = ['warehouse', 'product']

    def __str__(self):
        return f"{self.product.name} - {self.warehouse.name}"

    @property
    def is_below_reorder(self):
        return self.quantity <= self.reorder_level
    def restock(self, amount):
        if amount > 0:
            self.quantity += amount
            self.save()
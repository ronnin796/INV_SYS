from django.db import models
from django.utils import timezone
from api.suppliers.models import Supplier
from api.product.models import Product
from api.warehouse.models import Warehouse

class PurchaseOrder(models.Model):
    STATUS_CHOICES = [
        ("Pending", "Pending"),
        ("Received", "Received"),
        ("Cancelled", "Cancelled"),
    ]

    supplier = models.ForeignKey(Supplier, on_delete=models.PROTECT, related_name="purchase_orders")
    warehouse = models.ForeignKey(Warehouse, on_delete=models.PROTECT, related_name="purchase_orders")
    reference_number = models.CharField(max_length=100, blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="Pending")
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"PO-{self.id} ({self.reference_number or 'no-ref'})"

    @property
    def total(self):
        return sum(item.total for item in self.items.all())


class PurchaseItem(models.Model):
    purchase = models.ForeignKey(PurchaseOrder, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(Product, on_delete=models.PROTECT, related_name="+")
    quantity = models.DecimalField(max_digits=12, decimal_places=2)
    price = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["id"]

    def __str__(self):
        return f"{self.product} x {self.quantity}"

    @property
    def total(self):
        return (self.price or 0) * (self.quantity or 0)

    def save(self, *args, **kwargs):
        # If no price is explicitly given, pull from product
        if not self.price and self.product:
            self.price = self.product.price
        super().save(*args, **kwargs)


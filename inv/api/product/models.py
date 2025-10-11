from django.db import models
from api.subcategory.models import SubCategory
from api.category.models import Category
from api.suppliers.models import Supplier

class Product(models.Model):
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    subcategory = models.ForeignKey(SubCategory, on_delete=models.CASCADE, related_name='products', blank=True, null=True)
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE, related_name='products')

    def __str__(self):
        return self.name

    class Meta:
        indexes = [
            models.Index(fields=['name']),
            models.Index(fields=['category']),
            models.Index(fields=['subcategory']),
            models.Index(fields=['supplier']),
        ]
        verbose_name = 'Product'
        verbose_name_plural = 'Products'
        unique_together = ('name', 'supplier')
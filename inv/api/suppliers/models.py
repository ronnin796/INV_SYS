from django.db import models

# Create your models here.
class Supplier(models.Model):
    name = models.CharField(max_length=100)
    contact_email = models.EmailField()
    phone_number = models.CharField(max_length=15)
    address = models.TextField()

    def __str__(self):
        return self.name
    

# class SupplierProduct(models.Model):
#     supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE)
#     product = models.ForeignKey(Product, on_delete=models.CASCADE)
#     warehouse = models.ForeignKey(Warehouse, on_delete=models.CASCADE)
#     quantity_supplied = models.PositiveIntegerField()
#     supply_date = models.DateField(auto_now_add=True)

#     class Meta:
#         indexes = [
#             models.Index(fields=['warehouse']),
#             models.Index(fields=['supplier', 'product']),
#         ]
#         unique_together = ('supplier', 'product', 'warehouse')
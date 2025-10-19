from django.db import models

# Create your models here.
# api/sales/models.py
from django.db import models
from django.contrib.auth import get_user_model
CustomUser = get_user_model()

class Customer(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    created_by = models.ForeignKey(
        CustomUser,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="added_customers",
        help_text="The staff/user who added this customer."
    )

    def __str__(self):
        return self.name
    class Meta:
        verbose_name = "Customer"
        verbose_name_plural = "Customers"
        ordering = ["name"]
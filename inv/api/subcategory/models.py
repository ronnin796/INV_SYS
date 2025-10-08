from django.db import models
from api.category.models import Category
# Create your models here.
class SubCategory(models.Model):
    name = models.CharField(max_length=100)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='subcategories')

    class Meta:
        unique_together = ('name', 'category')
        verbose_name_plural = "Subcategories"

    def __str__(self):
        return f"{self.name} ({self.category.name})"
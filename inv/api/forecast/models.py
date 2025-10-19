# forecast/models.py
from django.db import models
from api.product.models import Product
from api.warehouse.models import Warehouse

class ForecastResult(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    warehouse = models.ForeignKey(Warehouse, on_delete=models.CASCADE)
    forecast_date = models.DateField(auto_now_add=True)
    days_ahead = models.PositiveIntegerField(default=30)
    predicted_sales = models.FloatField()
    projected_stock = models.FloatField()
    will_be_low = models.BooleanField(default=False)
    forecast_series = models.JSONField(blank=True, null=True)

    class Meta:
        unique_together = ('product', 'warehouse', 'forecast_date')
        ordering = ['-forecast_date']

    def __str__(self):
        return f"{self.product.name} @ {self.warehouse.name} ({self.forecast_date})"
    def to_dict(self):
        return {
            "product": self.product.name,
            "warehouse": self.warehouse.name,
            "forecast_date": self.forecast_date,
            "days_ahead": self.days_ahead,
            "predicted_sales": self.predicted_sales,
            "projected_stock": self.projected_stock,
            "will_be_low": self.will_be_low,
            "forecast_series": self.forecast_series,
        }
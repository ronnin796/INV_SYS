# forecast/services.py
from datetime import date, timedelta
from django.utils import timezone
from api.sales.models import SalesItem
from api.inventory.models import Inventory
from .models import ForecastResult
from .utils import forecast_sales_for_product

def evaluate_forecast(inventory_obj, days_ahead=30):
    """
    Evaluates ARIMA forecast without saving anything.
    """
    product = inventory_obj.product
    warehouse = inventory_obj.warehouse

    # Get last 60 days of sales
    sales = SalesItem.objects.filter(
        product=product,
        order__warehouse=warehouse,
        order__status="Completed",
        order__created_at__gte=timezone.now().date() - timedelta(days=60)
    )

    result = forecast_sales_for_product(product, warehouse, sales, days_ahead)
    if not result:
        return None

    predicted_sales = result["predicted_total_sales"]
    projected_stock = inventory_obj.quantity - predicted_sales

    return {
        "product": product,
        "warehouse": warehouse,
        "predicted_sales": predicted_sales,
        "projected_stock": projected_stock,
        "will_be_low": projected_stock <= inventory_obj.reorder_level,
        "forecast_series": result["forecast_series"]
    }


def get_or_create_forecast(inventory_obj, days_ahead=30):
    """
    Fetches cached forecast if exists, else evaluates and saves a new one.
    """
    product = inventory_obj.product
    warehouse = inventory_obj.warehouse
    today = date.today()

    # Check for cached forecast
    cached = ForecastResult.objects.filter(
        product=product, warehouse=warehouse, forecast_date=today
    ).first()
    if cached:
        return cached

    # Evaluate
    evaluated = evaluate_forecast(inventory_obj, days_ahead)
    if not evaluated:
        return None

    # Save forecast
    result = ForecastResult.objects.create(
        product=product,
        warehouse=warehouse,
        predicted_sales=evaluated["predicted_sales"],
        projected_stock=evaluated["projected_stock"],
        will_be_low=evaluated["will_be_low"],
        forecast_series=evaluated["forecast_series"],
        days_ahead=days_ahead,
    )
    return result

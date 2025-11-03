# forecast/views.py
from django.shortcuts import render
from api.inventory.models import Inventory
from api.product.models import Product
from api.warehouse.models import Warehouse
from .services import get_or_create_forecast
from django.shortcuts import render, get_object_or_404
from api.sales.models import SalesItem
from .utils import forecast_sales_for_product
import json
from django.utils import timezone
from django.http import JsonResponse
from api.sales.models import SalesItem  # adjust if different
from datetime import timedelta
from django.utils import timezone
import pandas as pd

def forecast_alerts_view(request):
    from .models import ForecastResult
    today = timezone.now().date()
    alerts = ForecastResult.objects.filter(forecast_date=today, will_be_low=True)
    return render(request, "forecast/alerts.html", {"alerts": alerts})


def forecast_dashboard(request):
    product_id = request.GET.get("product_id")
    warehouse_id = request.GET.get("warehouse_id")

    inventories = Inventory.objects.select_related("product", "warehouse")

    if product_id:
        inventories = inventories.filter(product_id=product_id)
    if warehouse_id:
        inventories = inventories.filter(warehouse_id=warehouse_id)

    forecasts = []
    for inv in inventories:
        forecast = get_or_create_forecast(inv)
        if forecast:
            # Add extra info for the table
            forecast.current_stock = inv.quantity
            forecast.reorder_level = inv.reorder_level
            forecasts.append(forecast)

    context = {
        "forecast_data": forecasts,
        "products": Product.objects.all(),
        "warehouses": Warehouse.objects.all(),
    }

    return render(request, "forecast/forecast.html", context)

def ajax_forecast_chart(request):
    product_id = request.GET.get("product_id")
    warehouse_id = request.GET.get("warehouse_id")

    # Example: fetch last 60 days of sales
    qs = SalesItem.objects.filter(
        product_id=product_id,
        warehouse_id=warehouse_id
    ).order_by("order__date")

    if not qs.exists():
        return JsonResponse({"dates": [], "actual_sales": [], "predicted_sales": []})

    df = pd.DataFrame.from_records(qs.values("order__date", "quantity"))
    df = df.groupby("order__date")["quantity"].sum().reset_index()

    # Example simple prediction (extend with your ARIMA logic)
    df["predicted"] = df["quantity"].rolling(7, min_periods=1).mean()

    return JsonResponse({
        "dates": list(df["order__date"].astype(str)),
        "actual_sales": list(df["quantity"]),
        "predicted_sales": list(df["predicted"]),
    })




# def forecast_chart_view(request, product_id, warehouse_id):
#     product = get_object_or_404(Product, id=product_id)
#     warehouse = get_object_or_404(Warehouse, id=warehouse_id)

#     sales = SalesItem.objects.filter(
#         product=product,
#         order__warehouse=warehouse,
#         order__status="Completed"
#     ).order_by("created_at")

#     result = forecast_sales_for_product(product, warehouse, sales, days_ahead=30)
#     if not result:
#         return render(request, "forecast/no_data.html", {"product": product, "warehouse": warehouse})

#     context = {
#         "product": product,
#         "warehouse": warehouse,
#         "historical": result["historical"],
#         "forecast": result["forecast"],
#     }
#     return render(request, "forecast/forecast_chart.html", context)


def forecast_chart_view(request, product_id, warehouse_id):
    product = get_object_or_404(Product, id=product_id)
    warehouse = get_object_or_404(Warehouse, id=warehouse_id)

    inventory = Inventory.objects.filter(product=product, warehouse=warehouse).first()

    sales = SalesItem.objects.filter(
        product=product,
        order__warehouse=warehouse,
        order__status="Completed"
    ).order_by("created_at")

    result = forecast_sales_for_product(product, warehouse, sales, days_ahead=30)

    if not result or not inventory:
        return render(request, "forecast/no_data.html", {"product": product, "warehouse": warehouse})

    forecast_data = {
        "historical": result["historical"],
        "forecast": result["forecast"],
        "predicted_sales": result.get("predicted_total_sales", 0),
        "projected_stock": inventory.quantity - result.get("predicted_total_sales", 0),
        "will_be_low": inventory.reorder_level is not None and
                       (inventory.quantity - result.get("predicted_total_sales", 0)) <= inventory.reorder_level,
    }

    context = {
        "inventory": inventory,
        "forecast_data": forecast_data,
        "forecast_data_json": json.dumps(forecast_data),  # 🔑 pass for JS
    }

    return render(request, "forecast/forecast_chart.html", context)
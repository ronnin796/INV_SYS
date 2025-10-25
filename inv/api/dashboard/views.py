# dashboard/views.py
import json
from datetime import timedelta, date
from decimal import Decimal

from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from django.shortcuts import render
from django.utils import timezone

from api.product.models import Product
from api.warehouse.models import Warehouse
from api.sales.models import SalesItem, SalesOrder
from api.inventory.models import Inventory
from api.forecast.models import ForecastResult
from api.purchase.models import PurchaseOrder  # adjust import if different
from django.db import models

def _to_float(x):
    if isinstance(x, Decimal):
        return float(x)
    try:
        return float(x)
    except Exception:
        return 0.0

@login_required
def dashboard(request):
    # Basic stats
    total_products = Product.objects.count()
    total_warehouses = Warehouse.objects.count()
    total_sales = SalesItem.objects.aggregate(total=Sum("quantity"))["total"] or 0
    total_stock = Inventory.objects.aggregate(total=Sum("quantity"))["total"] or 0

    total_sales = _to_float(total_sales)
    total_stock = _to_float(total_stock)

    avg_sales_per_product = round(total_sales / total_products, 2) if total_products else 0
    low_stock_products = Inventory.objects.filter(quantity__lte=models.F('reorder_level')).count()

    # Top 5 selling products (most recent)
    top_products_qs = (
        SalesItem.objects.values("product__name")
        .annotate(total_sold=Sum("quantity"))
        .order_by("-total_sold")[:5]
    )
    top_products = [
        {"product__name": tp["product__name"], "total_sold": _to_float(tp["total_sold"])}
        for tp in top_products_qs
    ]

    # Stock by warehouse
    stock_by_warehouse_qs = (
        Inventory.objects.values("warehouse__name")
        .annotate(total_stock=Sum("quantity"))
        .order_by("warehouse__name")
    )
    stock_labels = [s["warehouse__name"] for s in stock_by_warehouse_qs]
    stock_values = [_to_float(s["total_stock"]) for s in stock_by_warehouse_qs]
    print("DEBUG - stock_labels:", stock_labels)
    print("DEBUG - stock_values:", stock_values)
    # Last 7 days (or date range if requested)
    today = date.today()
    # allow optional query params ?from=YYYY-MM-DD&to=YYYY-MM-DD
    q_from = request.GET.get("from")
    q_to = request.GET.get("to")
    if q_from and q_to:
        try:
            start = date.fromisoformat(q_from)
            end = date.fromisoformat(q_to)
        except Exception:
            start = today - timedelta(days=6)
            end = today
    else:
        start = today - timedelta(days=6)
        end = today

    days = (end - start).days + 1
    last_days = [start + timedelta(days=i) for i in range(days)]

    sales_trend = []
    for d in last_days:
        s = SalesItem.objects.filter(created_at__date=d).aggregate(total=Sum("quantity"))["total"] or 0
        sales_trend.append(_to_float(s))

    stock_trend = []
    for d in last_days:
        s = Inventory.objects.filter(last_updated__date=d).aggregate(total=Sum("quantity"))["total"] or 0
        stock_trend.append(_to_float(s))

    # low stock detail (limit to 10)
    low_stock_items = Inventory.objects.filter(quantity__lte=models.F('reorder_level')).select_related('product','warehouse')[:10]
    low_stock_list = [
        {
            "product": li.product.name,
            "warehouse": li.warehouse.name,
            "quantity": _to_float(li.quantity),
            "reorder_level": li.reorder_level,
            "below_by": _to_float(li.reorder_level - li.quantity) if (li.reorder_level - li.quantity) > 0 else 0
        } for li in low_stock_items
    ]

    # forecasts summary
    forecasts_today = ForecastResult.objects.filter(forecast_date=timezone.now().date())
    will_be_low_count = forecasts_today.filter(will_be_low=True).count()
    avg_predicted_sales = _to_float(
        forecasts_today.aggregate(avg_pred=Sum("predicted_sales"))["avg_pred"] or 0
    ) if forecasts_today.exists() else 0

    # recent orders
    recent_sales_orders = SalesOrder.objects.order_by('-created_at')[:5]
    recent_pos = PurchaseOrder.objects.order_by('-created_at')[:5]

    context = {
        "total_products": total_products,
        "total_warehouses": total_warehouses,
        "total_sales": total_sales,
        "total_stock": total_stock,
        "avg_sales_per_product": avg_sales_per_product,
        "low_stock_products": low_stock_products,
        "top_products": top_products,
        "top_product_labels": json.dumps([p["product__name"] for p in top_products]),
        "top_product_values": json.dumps([p["total_sold"] for p in top_products]),
        "stock_labels": json.dumps(stock_labels),
        "stock_values": json.dumps(stock_values),
        "trend_labels": json.dumps([d.strftime("%b %d") for d in last_days]),
        "sales_trend": json.dumps(sales_trend),
        "stock_trend": json.dumps(stock_trend),
        "low_stock_list": low_stock_list,
        "will_be_low_count": will_be_low_count,
        "avg_predicted_sales": avg_predicted_sales,
        "recent_sales_orders": recent_sales_orders,
        "recent_pos": recent_pos,
        # also pass raw python objects for template loops
        "top_products_raw": top_products,
    }
    return render(request, "dashboard/dashboard.html", context)

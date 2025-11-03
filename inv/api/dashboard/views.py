import json
from datetime import timedelta, date, datetime

from django.contrib.auth.decorators import login_required
from django.db.models import Sum, F
from django.shortcuts import render

from api.product.models import Product
from api.warehouse.models import Warehouse
from api.sales.models import SalesItem, SalesOrder
from api.inventory.models import Inventory
from api.forecast.models import ForecastResult
from api.purchase.models import PurchaseOrder


def _to_float(x):
    if x is None:
        return 0.0
    try:
        return float(x)
    except Exception:
        return 0.0


@login_required
def dashboard(request):
    today = date.today()

    # ------------------------
    # Date filter
    # ------------------------
    q_from = request.GET.get("from")
    q_to = request.GET.get("to")
    try:
        start = datetime.fromisoformat(q_from).date() if q_from else today - timedelta(days=6)
        end = datetime.fromisoformat(q_to).date() if q_to else today
    except Exception:
        start = today - timedelta(days=6)
        end = today

    last_days = [start + timedelta(days=i) for i in range((end - start).days + 1)]

    # ------------------------
    # Total KPIs
    # ------------------------
    total_products = Product.objects.count()
    total_warehouses = Warehouse.objects.count()

    total_sales = SalesItem.objects.filter(created_at__date__range=(start, end)).aggregate(total=Sum("quantity"))["total"] or 0
    total_stock = Inventory.objects.aggregate(total=Sum("quantity"))["total"] or 0

    total_sales = _to_float(total_sales)
    total_stock = _to_float(total_stock)
    avg_sales_per_product = round(total_sales / total_products, 2) if total_products else 0
    low_stock_products = Inventory.objects.filter(quantity__lte=F('reorder_level')).count()

    # ------------------------
    # Top 5 Products (with warehouse)
    # ------------------------
    top_products_qs = (
        SalesItem.objects.filter(created_at__date__range=(start, end))
        .values("product__name", "order__warehouse__name")
        .annotate(total_sold=Sum("quantity"))
        .order_by("-total_sold")[:5]
    )
    top_products = [
        {
            "product__name": tp["product__name"],
            "warehouse": tp["order__warehouse__name"],
            "total_sold": _to_float(tp["total_sold"]),
        }
        for tp in top_products_qs
    ]

    # ------------------------
    # Stock by warehouse (uses same logic as debug view)
    # ------------------------
    selected_warehouse = request.GET.get("warehouse")
    warehouses = Warehouse.objects.all()

    if selected_warehouse and selected_warehouse != "all":
        inventories = Inventory.objects.filter(warehouse__id=selected_warehouse)
        stock_labels = [inv.product.name for inv in inventories]
        stock_values = [_to_float(inv.quantity) for inv in inventories]
    else:
        inventories = Inventory.objects.values("warehouse__name").annotate(total_stock=Sum("quantity"))
        stock_labels = [i["warehouse__name"] for i in inventories]
        stock_values = [_to_float(i["total_stock"]) for i in inventories]

    # ------------------------
    # Trends
    # ------------------------
    sales_trend_list = []
    for d in last_days:
        s = SalesItem.objects.filter(created_at__date=d).aggregate(total=Sum("quantity"))["total"] or 0
        sales_trend_list.append(_to_float(s))

    stock_trend_list = []
    for d in last_days:
        s = Inventory.objects.filter(last_updated__date=d).aggregate(total=Sum("quantity"))["total"] or 0
        stock_trend_list.append(_to_float(s))

    # ------------------------
    # Low stock items
    # ------------------------
    low_stock_items = Inventory.objects.filter(quantity__lte=F('reorder_level')).select_related('product', 'warehouse')[:10]
    low_stock_list = [
        {
            "product": li.product.name,
            "warehouse": li.warehouse.name,
            "quantity": _to_float(li.quantity),
            "reorder_level": li.reorder_level,
            "below_by": _to_float(li.reorder_level - li.quantity) if (li.reorder_level - li.quantity) > 0 else 0,
        }
        for li in low_stock_items
    ]

    # ------------------------
    # Forecast KPIs
    # ------------------------
    forecasts_today = ForecastResult.objects.filter(forecast_date=today)
    will_be_low_count = forecasts_today.filter(will_be_low=True).count()
    avg_predicted_sales = _to_float(
        forecasts_today.aggregate(total=Sum("predicted_sales"))["total"] or 0
    )

    predicted_low_stock = [
        {
            "product": f.product.name,
            "warehouse": f.warehouse.name,
            "predicted_sales": _to_float(f.predicted_sales),
            "projected_stock": _to_float(f.projected_stock),
        }
        for f in forecasts_today.filter(will_be_low=True)
    ]

    # ------------------------
    # Recent Orders
    # ------------------------
    recent_sales_orders = SalesOrder.objects.order_by("-created_at")[:5]
    recent_pos = PurchaseOrder.objects.order_by("-created_at")[:5]

    # ------------------------
    # Context
    # ------------------------
    context = {
        "total_products": total_products,
        "total_warehouses": total_warehouses,
        "total_sales": total_sales,
        "total_stock": total_stock,
        "avg_sales_per_product": avg_sales_per_product,
        "low_stock_products": low_stock_products,
        "top_products_raw": top_products,
        "top_product_labels": json.dumps([p["product__name"] for p in top_products]),
        "top_product_values": json.dumps([p["total_sold"] for p in top_products]),
        "stock_labels": json.dumps(stock_labels),
        "stock_values": json.dumps(stock_values),
        "trend_labels": json.dumps([d.strftime("%b %d") for d in last_days]),
        "sales_trend": json.dumps(sales_trend_list),
        "stock_trend": json.dumps(stock_trend_list),
        "low_stock_list": low_stock_list,
        "predicted_low_stock": predicted_low_stock,
        "will_be_low_count": will_be_low_count,
        "avg_predicted_sales": avg_predicted_sales,
        "recent_sales_orders": recent_sales_orders,
        "recent_pos": recent_pos,
        "warehouses": warehouses,
        "selected_warehouse": selected_warehouse or "all",
    }

    return render(request, "dashboard/dashboard.html", context)



def stock_debug_view(request):
    selected_warehouse = request.GET.get('warehouse')

    # Get all warehouses for dropdown
    warehouses = Warehouse.objects.all()

    if selected_warehouse and selected_warehouse != 'all':
        inventories = Inventory.objects.filter(warehouse__id=selected_warehouse)
        labels = [inv.product.name for inv in inventories]
        values = [inv.quantity for inv in inventories]
    else:
        # total stock across warehouses
        inventories = Inventory.objects.values('warehouse__name').annotate(total_stock=Sum('quantity'))
        labels = [i['warehouse__name'] for i in inventories]
        values = [i['total_stock'] for i in inventories]
    from django.conf import settings
    print("=== DEBUG STOCK VIEW ===")
    print("Settings DB:", settings.DATABASES)
    print("Warehouses in DB:", list(Warehouse.objects.values_list('id', 'name')))
    print("Inventory count:", Inventory.objects.count())
    print("Selected warehouse:", selected_warehouse)


    context = {
        'warehouses': warehouses,
        'selected_warehouse': selected_warehouse or 'all',
        'stock_labels': json.dumps(labels),
        'stock_values': json.dumps(values),
    }
    return render(request, 'dashboard/debug.html', context)

from datetime import timedelta, date
from django.db.models import Sum
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from api.product.models import Product
from api.warehouse.models import Warehouse
from api.sales.models import SalesItem
from api.inventory.models import Inventory

@login_required
def dashboard(request):
    # Basic stats
    total_products = Product.objects.count()
    total_warehouses = Warehouse.objects.count()
    total_sales = SalesItem.objects.aggregate(total=Sum("quantity"))["total"] or 0
    total_stock = Inventory.objects.aggregate(total=Sum("quantity"))["total"] or 0

    avg_sales_per_product = round(total_sales / total_products, 2) if total_products else 0
    low_stock_products = Inventory.objects.filter(quantity__lte=10).count()

    # Top 5 selling products
    top_products_qs = (
        SalesItem.objects.values("product__name")
        .annotate(total_sold=Sum("quantity"))
        .order_by("-total_sold")[:5]
    )
    top_products = list(top_products_qs)

    # Pie chart fallback
    top_product_labels = [p["product__name"] for p in top_products] if top_products else ["No sales"]
    top_product_values = [p["total_sold"] for p in top_products] if top_products else [0]

    # Stock by warehouse
    stock_by_warehouse = (
        Inventory.objects.values("warehouse__name")
        .annotate(total_stock=Sum("quantity"))
        .order_by("warehouse__name")
    )
    stock_labels = [s["warehouse__name"] for s in stock_by_warehouse]
    stock_values = [s["total_stock"] for s in stock_by_warehouse]

    # Last 7 days trends
    today = date.today()
    last_7_days = [today - timedelta(days=i) for i in range(6, -1, -1)]
    sales_trend = [
        SalesItem.objects.filter(created_at__date=d).aggregate(total=Sum("quantity"))["total"] or 0
        if hasattr(SalesItem, 'created_at') else 0
        for d in last_7_days
    ]
    stock_trend = [
        Inventory.objects.filter(last_updated__date=d).aggregate(total=Sum("quantity"))["total"] or 0
        if hasattr(Inventory, 'last_updated') else 0
        for d in last_7_days
    ]

    context = {
        "total_products": total_products,
        "total_warehouses": total_warehouses,
        "total_sales": total_sales,
        "total_stock": total_stock,
        "avg_sales_per_product": avg_sales_per_product,
        "low_stock_products": low_stock_products,
        "top_products": top_products,
        "top_product_labels": top_product_labels,
        "top_product_values": top_product_values,
        "stock_labels": stock_labels,
        "stock_values": stock_values,
        "trend_labels": [d.strftime("%b %d") for d in last_7_days],
        "sales_trend": sales_trend,
        "stock_trend": stock_trend,
    }
    return render(request, "dashboard/dashboard.html", context)

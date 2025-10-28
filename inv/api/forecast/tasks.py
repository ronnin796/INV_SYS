# forecast/tasks.py
from celery import shared_task
from django.core.mail import send_mail
from django.utils import timezone
from collections import defaultdict
from api.inventory.models import Inventory
from .services import get_or_create_forecast
from django.conf import settings
import time



@shared_task
def test_task():
    print("Starting background task...")
    time.sleep(5)
    print("Task completed!")
    return "Done"




@shared_task
def auto_forecast_and_notify():
    today = timezone.now().date()
    warehouse_alerts = defaultdict(list)

    inventories = Inventory.objects.select_related("product", "warehouse").all()

    for inv in inventories:
        forecast = get_or_create_forecast(inv)
        if not forecast:
            continue

        if forecast.will_be_low:
            warehouse_alerts[inv.warehouse].append({
                "product": inv.product.name,
                "current_stock": inv.quantity,
                "reorder_level": inv.reorder_level,
                "projected_stock": forecast.projected_stock,
            })

    # Send one email per warehouse
    for warehouse, alerts in warehouse_alerts.items():
        if not warehouse.manager or not warehouse.manager.email:
            print(f"[INFO] Skipping {warehouse.name}: no manager email set.")
            continue

        body_lines = [
            f"{a['product']}: Current={a['current_stock']}, Reorder={a['reorder_level']}, Projected={a['projected_stock']:.2f}"
            for a in alerts
        ]
        body = "\n".join(body_lines)

        send_mail(
            subject=f"⚠️ Low Stock Forecast — {warehouse.name} ({today})",
            message=f"Dear {warehouse.manager.get_full_name() or warehouse.manager.username},\n\n"
                    f"The following items may soon reach low stock levels:\n\n{body}\n\n"
                    f"— Forecast System",
            from_email=settings.DEFAULT_FROM_EMAIL, 
            recipient_list=[warehouse.manager.email],
            fail_silently=False,
        )

    return f"Processed {len(inventories)} inventories, sent {len(warehouse_alerts)} emails."


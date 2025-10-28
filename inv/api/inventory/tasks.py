# inventory/tasks.py
from celery import shared_task
from django.core.mail import send_mail
from django.utils import timezone
from django.conf import settings
from collections import defaultdict
from api.inventory.models import Inventory

@shared_task
def check_and_notify_low_stock():
    """
    Task that checks all inventory items and sends an email alert
    to the respective warehouse manager if any item is below reorder level.
    """
    today = timezone.now().date()
    warehouse_alerts = defaultdict(list)

    inventories = Inventory.objects.select_related("warehouse", "product").all()

    for inv in inventories:
        if inv.is_below_reorder:
            warehouse_alerts[inv.warehouse].append({
                "product": inv.product.name,
                "current_stock": inv.quantity,
                "reorder_level": inv.reorder_level,
            })

    for warehouse, alerts in warehouse_alerts.items():
        manager = getattr(warehouse, "manager", None)
        if not manager or not manager.email:
            print(f"[INFO] Skipping {warehouse.name}: No manager email set.")
            continue

        # Format the email body
        body_lines = [
            f"{a['product']}: Current={a['current_stock']}, Reorder={a['reorder_level']}"
            for a in alerts
        ]
        body = "\n".join(body_lines)

        send_mail(
            subject=f"🚨 Low Stock Alert — {warehouse.name} ({today})",
            message=(
                f"Dear {manager.get_full_name() or manager.username},\n\n"
                f"The following products in {warehouse.name} are below the reorder level:\n\n"
                f"{body}\n\n"
                f"Please restock them soon to avoid shortages.\n\n"
                f"— Automated Inventory System"
            ),
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[manager.email],
            fail_silently=False,
        )

    return f"Checked {len(inventories)} items, sent {len(warehouse_alerts)} alert emails."

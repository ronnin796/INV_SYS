# api/inventory/utils.py
from django.db import transaction
from django.db.models import F
from .models import Inventory
from api.purchase.models import PurchaseOrder
from api.sales.models import SalesOrder

def update_inventory_after_status_change(instance, direction: str):
    """
    Adjust inventory safely for PurchaseOrder or SalesOrder.
    direction: "increase" or "decrease"
    """
    if direction not in ["increase", "decrease"]:
        raise ValueError("direction must be 'increase' or 'decrease'")

    if isinstance(instance, (PurchaseOrder, SalesOrder)):
        items = instance.items.select_related("product")
        warehouse = instance.warehouse
    else:
        raise TypeError("instance must be a PurchaseOrder or SalesOrder")

    with transaction.atomic():
        for item in items:
            # Use filter + first() instead of get() to prevent MultipleObjectsReturned
            inventory = Inventory.objects.filter(
                warehouse=warehouse, product=item.product
            ).first()

            if not inventory:
                inventory = Inventory.objects.create(
                    warehouse=warehouse, product=item.product, quantity=0
                )

            if direction == "increase":
                inventory.quantity = F('quantity') + item.quantity
            else:  # decrease
                inventory.quantity = F('quantity') - item.quantity

            inventory.save()
            inventory.refresh_from_db()

from api.inventory.models import Inventory

def update_inventory_after_status_change(purchase_order, action):
    """
    Update inventory quantities when a purchase order changes state.

    Args:
        purchase_order: PurchaseOrder instance
        action: "increase" or "decrease"
    """
    for item in purchase_order.items.select_related("product"):
        inventory, _ = Inventory.objects.get_or_create(
            product=item.product,
            warehouse=purchase_order.warehouse,
            defaults={"quantity": 0},
        )

        if action == "increase":
            inventory.quantity += item.quantity
        elif action == "decrease":
            inventory.quantity -= item.quantity

        inventory.save(update_fields=["quantity"])

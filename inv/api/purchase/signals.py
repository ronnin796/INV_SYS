from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from .models import PurchaseOrder
from api.inventory.utils import update_inventory_after_status_change


@receiver(pre_save, sender=PurchaseOrder)
def detect_status_change(sender, instance, **kwargs):
    """
    Store previous status before saving to detect change later.
    """
    if instance.pk:
        try:
            old = PurchaseOrder.objects.get(pk=instance.pk)
            instance._previous_status = old.status
        except PurchaseOrder.DoesNotExist:
            instance._previous_status = None
    else:
        instance._previous_status = None


@receiver(post_save, sender=PurchaseOrder)
def handle_status_change(sender, instance, created, **kwargs):
    """
    Automatically update inventory when purchase status changes.
    """
    prev_status = getattr(instance, "_previous_status", None)
    new_status = instance.status

    # 1️⃣ When a new Purchase Order is created with "Received"
    if created and new_status == "Received":
        update_inventory_after_status_change(instance, "increase")

    # 2️⃣ When status changes from Pending → Received
    elif not created and prev_status != new_status:
        if prev_status != "Received" and new_status == "Received":
            update_inventory_after_status_change(instance, "increase")

        # 3️⃣ When status changes from Received → Pending or Cancelled
        elif prev_status == "Received" and new_status in ["Pending", "Cancelled"]:
            update_inventory_after_status_change(instance, "decrease")

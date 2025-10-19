from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from .models import SalesOrder
from api.inventory.utils import update_inventory_after_status_change  # reuse same util

@receiver(pre_save, sender=SalesOrder)
def detect_sales_status_change(sender, instance, **kwargs):
    if instance.pk:
        try:
            old = SalesOrder.objects.get(pk=instance.pk)
            instance._previous_status = old.status
        except SalesOrder.DoesNotExist:
            instance._previous_status = None
    else:
        instance._previous_status = None


@receiver(post_save, sender=SalesOrder)
def handle_sales_status_change(sender, instance, created, **kwargs):
    prev_status = getattr(instance, "_previous_status", None)
    new_status = instance.status

    if created and new_status == "Completed":
        update_inventory_after_status_change(instance, "decrease")
    elif not created and prev_status != new_status:
        if prev_status != "Completed" and new_status == "Completed":
            update_inventory_after_status_change(instance, "decrease")
        elif prev_status == "Completed" and new_status in ["Pending", "Cancelled"]:
            update_inventory_after_status_change(instance, "increase")

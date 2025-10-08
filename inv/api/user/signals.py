# signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from .models import CustomUser

@receiver(post_save, sender=CustomUser)
def send_approval_email(sender, instance, created, **kwargs):
    if not created and instance.is_approved:
        send_mail(
            "Account Approved",
            "Your account has been approved by the admin. You can now log in.",
            "admin@example.com",
            [instance.email],
        )

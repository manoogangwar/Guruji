from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.conf import settings
from .models import ContactRequest
from .models import ContactInformation

@receiver(post_save, sender=ContactRequest)
def send_contact_request_email(sender, instance, created, **kwargs):
    if created:
        receiver_name = (
            instance.receiver.get_full_name()
            if hasattr(instance.receiver, "get_full_name")
            else instance.receiver.username
        )

        sender_name = (
            instance.sender.get_full_name()
            if hasattr(instance.sender, "get_full_name")
            else instance.sender.username
        )

        subject = "New Contact Request"
        message = f"""
Hello {receiver_name},

You have received a contact request from:

Name: {sender_name}
Email: {instance.sender.email}

Please login to your account to respond.
"""

        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [instance.receiver.email],
            fail_silently=False,
        )
        
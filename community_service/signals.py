from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import NeedRequest
from .utils import get_nearest_users, send_need_email


@receiver(post_save, sender=NeedRequest)
def notify_nearby_users(sender, instance, created, **kwargs):

    if not created:
        return

    users = get_nearest_users(instance, max_distance_km=10)
    send_need_email(users, instance)

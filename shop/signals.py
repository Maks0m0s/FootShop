from django.db.models.signals import post_delete
from django.dispatch import receiver
from .models import Order

@receiver(post_delete, sender=Order)
def delete_destination(sender, instance, **kwargs):
    if instance.destination:
        if not Order.objects.filter(destination=instance.destination).exists():
            instance.destination.delete()
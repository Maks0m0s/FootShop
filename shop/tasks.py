from celery import shared_task
from django.utils import timezone
from datetime import timedelta
from .models import Jersey, Size, ItemInCard, Shorts

@shared_task
def update_sizes():
    updated_items = 0

    # Update Items
    for model in [Jersey, Shorts]:
        for item in model.objects.all():
            if item.sizes.count() == 0:
                for size in Size.objects.all():
                    item.sizes.add(size)
                item.sold = False
                item.save()
                updated_items += 1

    if updated_items != 1:
        return f"{updated_items} Items were updated."
    else:
        return f"{updated_items} Item was updated."

@shared_task
def remove_from_cart():
    """
    Deletes cart items older than 5 minutes.
    """
    one_week_ago = timezone.now() - timedelta(weeks=1)
    expired_items = ItemInCard.objects.filter(adding_time__lte=one_week_ago)
    count = expired_items.count()
    expired_items.delete()
    return f"Deleted {count} expired cart items"
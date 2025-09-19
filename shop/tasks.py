from celery import shared_task
from django.utils import timezone
from datetime import timedelta
from .models import Jersey, Size, ItemInCard, Card, Ball

@shared_task
def update_sizes():
    """
    Re-adds all sizes to jerseys that have no sizes (restocks them)
    and marks sold Cards and Balls as unsold.
    """
    updated_items = 0

    # Update Jerseys
    for jersey in Jersey.objects.all():
        if jersey.sizes.count() == 0:
            for size in Size.objects.all():
                jersey.sizes.add(size)
            jersey.sold = False
            jersey.save()
            updated_items += 1

    # Update Cards
    for card in Card.objects.filter(sold=True):
        card.sold = False
        card.save()
        updated_items += 1

    # Update Balls
    for ball in Ball.objects.filter(sold=True):
        ball.sold = False
        ball.save()
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
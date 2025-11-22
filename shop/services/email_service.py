from django.core.mail import send_mail
from django.conf import settings
from myproject.settings import EMAIL_HOST_USER

from shop.models import OrderItem



def send_registration_email(user):
    subject = "Welcome to FootShop!"
    message = f"""
    Hi {user.first_name or user.username},

    Your account has been successfully created!

    Username: {user.username}
    Email: {user.email}

    Thank you for registering.
    """
    recipient = [user.email]

    send_mail(
        subject=subject,
        message=message,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=recipient,
        fail_silently=False,
    )

def send_order_email(order):
    items = OrderItem.objects.filter(order=order)

    #--- For Client ---


    subject = f"Your Order was placed!"
    message = f"""
    Hi {order.user.first_name or order.user.username},
    
    Your order has been successfully placed !
    
    -- Order Details --
    Creating Date : {order.created_at.date()}
    Aprox. Arriving Date : {order.arriving_date.date()}
    Total Items : {items.count()}
    Total Price : {order.total_price}€
    
    -- Delivery Details --
    Country : {order.destination.country}
    Address : {order.destination.address}
    Postal Code : {order.destination.postal_code}
    
    Thank you for your order ! Soon you will receive another email about your order.
    """
    recipient = [order.user.email]

    send_mail(
        subject=subject,
        message=message,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=recipient,
        fail_silently=False,
    )

    #--- For Admin ---

    subject2 = f"NEW ORDER ({len(items)} item/s)"
    items_list = ""
    for item in items:
        items_list+=f'- {item.product_name} | {item.chosen_size} | {item.player} - {item.number} | {item.product_price}€\n'
    message2 = f"""
    New order was placed by :
    {order.user.first_name or order.user.username}
    
    -- Client Contact --
    Email : {order.user.email}
    
    -- Order --
    {items_list}
    
    -- Order Details --
    Creating Date : {order.created_at.date()}
    Aprox. Arriving Date : {order.arriving_date.date()}
    Total Items : {items.count()}
    Total Price : {order.total_price}€
    
    -- Delivery Details --
    Country : {order.destination.country}
    Address : {order.destination.address}
    Postal Code : {order.destination.postal_code}
    """
    recipient2 = [EMAIL_HOST_USER]

    send_mail(
        subject=subject2,
        message=message2,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=recipient2,
        fail_silently=True,
    )
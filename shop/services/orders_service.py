from shop.models import Order
from shop.services.cart_service import get_items
from datetime import datetime
from shop.models import OrderItem, ItemInCard

def save_order(request):
    user = request.user
    cart_items = ItemInCard.objects.filter(user=user)
    order = Order.objects.create(user=user)

    for item in cart_items:
        OrderItem.objects.create(
            order=order,
            product_name=str(item.product),
            product_price=item.product.price,
            quantity=item.quantity,
            chosen_size=item.chosen_size.name if item.chosen_size else None,
            product_category=item.product.category
        )

    # Optionally clear cart after order
    cart_items.delete()

    return order

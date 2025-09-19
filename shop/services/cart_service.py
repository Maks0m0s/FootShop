from django.contrib.contenttypes.models import ContentType
from django.shortcuts import get_object_or_404

from shop.models import Jersey, Card, Ball, Size, ItemInCard, Product


def add_to_cart(request, pk, category_id, MODEL_MAP):
    if not request.user.is_authenticated:
        # redirect to login with "next" so user can return to product page after login
        return {
            'status_ok': False,
            'redirect_to': '/auth/login/'
        }

    model = MODEL_MAP.get(category_id)

    product = get_object_or_404(model, pk=pk)

    if not product:
        return {'status_ok': False}

    size_id = request.data.get("size")
    chosen_size = None
    if size_id:
        chosen_size = get_object_or_404(Size, id=size_id)

        if isinstance(product, Jersey):
            product.sizes.remove(chosen_size)
            if product.sizes.count() == 0:
                product.sold = True
            else:
                product.sold = False
            product.save()  # ✅ Save the change

    if not product.category.id == 1:
        product.sold = True
        product.save()

    ItemInCard.objects.create(
        content_type=ContentType.objects.get_for_model(model),
        object_id=product.id,
        user=request.user,  # ✅ now safe because we checked authentication
        quantity=1,
        chosen_size=chosen_size
    )

    return {
        'status_ok': True,
        'product': product
    }

def get_items(request):
    user = request.user
    items = ItemInCard.objects.filter(user=user)

    total = sum(item.product.price * item.quantity for item in items)

    return {
        'items': items,
        'cart': {'total': total},
        'user': user
    }

def remove_product(request, product_id):
    item = get_object_or_404(ItemInCard, id=product_id)

    product = item.product
    size = item.chosen_size

    item.delete()

    product.sold = False
    if product.category.id == 1:
        product.sizes.add(size)
    product.save()

    data = get_items(request)

    return data
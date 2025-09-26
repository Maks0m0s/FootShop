from django.contrib.contenttypes.models import ContentType
from django.shortcuts import get_object_or_404

from shop.models import Jersey, Shorts, Size, ItemInCard, Product


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

        product.sizes.remove(chosen_size)
        if product.sizes.count() == 0:
            product.sold = True
        else:
            product.sold = False
        product.save()  # ✅ Save the change


    jersey_name = request.POST.get("name-id")
    jersey_number = request.POST.get("number-id")

    # Only validate if inputs exist
    if category_id != 3:
        if jersey_name != '' and jersey_number != '':
            # Check that name is not digits
            if jersey_name.isdigit():
                return {'status_ok': False, 'error': 'Name cannot be numeric'}

            try:
                jersey_number = int(jersey_number)
            except ValueError:
                return {'status_ok': False, 'error': 'Number must be an integer'}

            if jersey_number < 1 or jersey_number > 99:
                return {'status_ok': False, 'error': 'Number must be between 1 and 99'}
        elif jersey_name != '' or jersey_number != '':
            return {'status_ok': False, 'error': 'If you fill inputs, fill both of them.'}
        else:
            jersey_name = None
            jersey_number = None
    else:
        jersey_name = None
        jersey_number = None


    item = ItemInCard.objects.create(
        content_type=ContentType.objects.get_for_model(model),
        object_id=product.id,
        user=request.user,  # ✅ now safe because we checked authentication
        quantity=1,
        chosen_size=chosen_size,
        player=jersey_name,
        number=jersey_number
    )

    return {
        'status_ok': True,
        'product': product,
        'item' : item
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
    product.sizes.add(size)
    product.save()

    data = get_items(request)

    return data
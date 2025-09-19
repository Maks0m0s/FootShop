import stripe
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from shop.services.cart_service import get_items

stripe.api_key = settings.STRIPE_SECRET_KEY


class CheckoutView(APIView):
    def post(self, request):
        # Get user's cart
        cart_data = get_items(request)
        items = cart_data['items']

        if not items:
            return Response({"error": "Cart is empty"}, status=400)

        # Prepare line items for Stripe
        line_items = []
        for item in items:
            line_items.append({
                "price_data": {
                    "currency": "eur",
                    "product_data": {"name": str(item.product)},
                    "unit_amount": int(item.product.price * 100),
                },
                "quantity": item.quantity,
            })

        # Create Checkout Session
        session = stripe.checkout.Session.create(
            payment_method_types=["card"],
            line_items=line_items,
            mode="payment",
            success_url=request.build_absolute_uri("/order/success_payment/"),
            cancel_url=request.build_absolute_uri("/cart/?canceled=true"),
        )

        return Response({"checkout_url": session.url})
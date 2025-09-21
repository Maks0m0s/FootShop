import stripe
import json
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.renderers import TemplateHTMLRenderer, JSONRenderer

from shop.services.cart_service import get_items

stripe.api_key = settings.STRIPE_SECRET_KEY

class CheckoutView(APIView):
    def get(self, request):
        return Response({}, template_name='shop/checkout.html')

    def post(self, request):
        cart_data = get_items(request)
        items = cart_data['items']

        if not items:
            return Response({"error": "Cart is empty"}, status=400)

        line_items = [
            {
                "price_data": {
                    "currency": "eur",
                    "product_data": {"name": str(item.product)},
                    "unit_amount": int(item.product.price * 100),
                },
                "quantity": item.quantity
            }
            for item in items
        ]

        # Save destination info in session
        data = request.data
        country = data.get('country')
        address = data.get('address')
        postal_code = data.get('postal_code')

        if country and address and postal_code:
            request.session['destination'] = {
                'country': data.get('country'),
                'address': data.get('address'),
                'postal_code': data.get('postal_code')
            }
        else:
            return Response({"error": "Destination is empty."}, status=400)

        session = stripe.checkout.Session.create(
            payment_method_types=["card"],
            line_items=line_items,
            mode="payment",
            success_url=request.build_absolute_uri("/order/success_payment/"),
            cancel_url=request.build_absolute_uri("/cart/?canceled=true"),
        )

        return Response({"checkout_url": session.url})
from django.shortcuts import redirect
from rest_framework.views import APIView
from rest_framework.response import Response
from shop.serializers.checkout_serializer import CheckoutSerializer
from shop.services.cart_service import get_items
import stripe
from django.conf import settings

stripe.api_key = settings.STRIPE_SECRET_KEY


class CheckoutView(APIView):
    def get(self, request):
        """
        Render the empty checkout form without triggering errors.
        We call is_valid() on an empty serializer to safely expose `.errors`.
        """
        serializer = CheckoutSerializer(data={})
        serializer.is_valid()  # makes .errors safe to access in template
        return Response({'serializer': serializer}, template_name='shop/checkout.html')

    def post(self, request):
        serializer = CheckoutSerializer(data=request.data)
        if not serializer.is_valid():
            # Validation failed — re-render with field errors
            return Response({'serializer': serializer}, template_name='shop/checkout.html', status=400)

        # Cart data
        cart_data = get_items(request)
        items = cart_data['items']
        if not items:
            # Example of non-field error
            serializer._errors = {"non_field_errors": ["Cart is empty."]}
            return Response({'serializer': serializer}, template_name='shop/checkout.html', status=400)

        # Save validated info in session
        data = serializer.validated_data
        request.session['destination'] = data

        # Stripe checkout
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

        session = stripe.checkout.Session.create(
            payment_method_types=["card"],
            line_items=line_items,
            mode="payment",
            success_url=request.build_absolute_uri("/orders/success_payment/"),
            cancel_url=request.build_absolute_uri("/cart/?canceled=true"),
        )

        return redirect(session.url)
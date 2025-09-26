
from django.shortcuts import redirect
from rest_framework import viewsets, permissions
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.parsers import FormParser, MultiPartParser
from django.shortcuts import get_object_or_404

from shop.models import Jersey, Shorts, Size, Product
from shop.services import cart_service

MODEL_MAP = {
    1: Jersey,
    2: Jersey,
    3: Shorts,
}

class ProductsViewSet(viewsets.ViewSet):
    """
    Handles showing a single product (jersey, card, or ball)
    """
    renderer_classes = [TemplateHTMLRenderer]
    template_name = "shop/product_details.html"
    permission_classes = [permissions.AllowAny]
    parser_classes = [FormParser, MultiPartParser]

    def retrieve(self, request, category_id=None, pk=None):
        model = MODEL_MAP.get(category_id)

        product = get_object_or_404(model, pk=pk)

        # **Make sure to set template_name here!**
        return Response(
            {
                "product": product,
                "all_sizes": Size.objects.all(),
            },
        )

    @action(detail=True, methods=['post'], url_path='add-to-cart')
    def add_to_cart(self, request, category_id=None, pk=None):
        response = cart_service.add_to_cart(request, pk, category_id, MODEL_MAP)

        if response.get('redirect_to'):
            return redirect(response['redirect_to'])

        if response.get('status_ok', False):
            return Response({'product': response['product'], 'item':response['item']}, template_name="shop/successful_adding_to_cart.html")
        else:
            return redirect('product-details', category_id=category_id, pk=pk)
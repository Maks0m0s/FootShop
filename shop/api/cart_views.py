from rest_framework import viewsets, permissions
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.parsers import FormParser, MultiPartParser

from shop.models import ItemInCard
from shop.services.cart_service import get_items, remove_product


class CartViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    renderer_classes = [TemplateHTMLRenderer]
    parser_classes = [FormParser, MultiPartParser]

    def list(self, request):
        data = get_items(request)
        return Response(data, template_name='shop/cart.html')

    @action(detail=True, methods=['post'], url_path='remove')
    def remove(self, request, pk=None):
        data = remove_product(request, pk)
        return Response(data, template_name='shop/cart.html')
from rest_framework import viewsets, permissions
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response
from rest_framework.decorators import action
from shop.services.orders_service import save_order


class OrdersViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    renderer_classes = [TemplateHTMLRenderer]

    @action(detail=False, methods=['get'], url_path='success_payment')
    def success_payment(self, request):
        order = save_order(request)
        return Response({'order':order}, template_name="shop/success_payment.html")
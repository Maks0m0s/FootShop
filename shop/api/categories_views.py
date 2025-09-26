from rest_framework import viewsets, permissions
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

from shop.models import Category, Jersey, Shorts


class CategoriesViewSet(viewsets.ModelViewSet):
    renderer_classes = [TemplateHTMLRenderer]
    permission_classes = [permissions.AllowAny]

    def list(self, request):
        categories = Category.objects.all()
        return Response({"categories": categories}, template_name="shop/categories.html")

    def retrieve(self, request, pk=None):
        category = get_object_or_404(Category, id=pk)
        # Collect all products (jerseys, cards, balls) in this category
        jerseys = Jersey.objects.filter(category=category)
        shorts = Shorts.objects.filter(category=category)
        products = list(jerseys) + list(shorts)

        return Response(
            {"category": category, "products": products},
            template_name="shop/products_list.html"
        )
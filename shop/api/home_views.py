from rest_framework import viewsets
from django.shortcuts import render

class HomeViewSet(viewsets.ViewSet):
    def list(self, request):
        return render(request, 'shop/home.html', {})
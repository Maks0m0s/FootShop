from rest_framework import viewsets
from django.shortcuts import render

class AboutViewSet(viewsets.ViewSet):
    def list(self, request):
        return render(request, 'shop/about.html', {})
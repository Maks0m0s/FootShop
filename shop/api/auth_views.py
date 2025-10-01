from rest_framework import viewsets, permissions
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.parsers import FormParser, MultiPartParser
from django.contrib.auth import login, logout, authenticate
from django.shortcuts import redirect
from rest_framework.response import Response
from shop.forms import LoginForm, RegisterForm
from shop.services.auth_service import register as register_service
from rest_framework.decorators import action

class AuthViewSet(viewsets.ViewSet):
    renderer_classes = [TemplateHTMLRenderer]
    parser_classes = [FormParser, MultiPartParser]
    permission_classes = [permissions.AllowAny]

    @action(detail=False, methods=['get', 'post'], url_path='login')
    def login(self, request):
        if request.method == 'POST':
            form = LoginForm(request.POST)
            if form.is_valid():
                user = authenticate(
                    request,
                    username=form.cleaned_data['username'],
                    password=form.cleaned_data['password']
                )
                if user:
                    login(request, user)
                    return redirect('home')
                else:
                    form.add_error(None, 'Invalid credentials')
        else:
            form = LoginForm()
        return Response({'form': form}, template_name='shop/login.html')

    @action(detail=False, methods=['get', 'post'], url_path='register')
    def register(self, request):
        if request.method == 'POST':
            form = RegisterForm(request.POST)
            if form.is_valid():
                user = register_service(form.cleaned_data)
                login(request, user)
                return redirect('home')
        else:
            form = RegisterForm()
        return Response({'form': form}, template_name='shop/register.html')

    @action(detail=False, methods=['get'], url_path='logout')
    def logout(self, request):
        logout(request)
        return redirect('home')

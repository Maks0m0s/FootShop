from rest_framework import viewsets, permissions
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.parsers import FormParser, MultiPartParser
from django.contrib.auth import login, logout, authenticate
from django.shortcuts import redirect
from rest_framework.response import Response
from shop.forms import LoginForm, RegisterForm
from shop.services.auth_service import register as register_service
from rest_framework.decorators import action
from rest_framework_simplejwt.tokens import RefreshToken
from django.conf import settings


class AuthViewSet(viewsets.ViewSet):
    renderer_classes = [TemplateHTMLRenderer]
    parser_classes = [FormParser, MultiPartParser]
    permission_classes = [permissions.AllowAny]

    @action(detail=False, methods=['get', 'post'], url_path='login')
    def login(self, request):
        form_not_valid = False
        form = LoginForm(request.POST or None)

        if request.method == 'POST':
            if form.is_valid():
                user = authenticate(
                    request,
                    username=form.cleaned_data['username'],
                    password=form.cleaned_data['password']
                )
                if user:
                    login(request, user)
                    refresh = RefreshToken.for_user(user)

                    response = redirect('home')
                    response.set_cookie(
                        key='access_token',
                        value=str(refresh.access_token),
                        httponly=True,
                        secure=not settings.DEBUG,
                        samesite='Lax'
                    )
                    response.set_cookie(
                        key='refresh_token',
                        value=str(refresh),
                        httponly=True,
                        secure=not settings.DEBUG,
                        samesite='Lax'
                    )
                    return response
                else:
                    form.add_error(None, 'Invalid credentials')
            form_not_valid = True

        return Response({'form': form, 'form_not_valid': form_not_valid}, template_name='shop/login.html')


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
        response = redirect('home')
        response.delete_cookie('access_token')
        response.delete_cookie('refresh_token')
        logout(request)
        return response

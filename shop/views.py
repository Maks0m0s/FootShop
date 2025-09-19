from django.views.generic import TemplateView

class HomeView(TemplateView):
    template_name = 'shop/home.html'

class CategoriesView(TemplateView):
    template_name = 'shop/categories.html'

class AboutView(TemplateView):
    template_name = 'shop/about.html'
from django.contrib import admin
from .models import Category, Detail, Jersey, Ball, Card, ItemInCard, Order, Size, OrderItem

admin.site.register(Category)
admin.site.register(Detail)
admin.site.register(Jersey)
admin.site.register(Ball)
admin.site.register(Card)
admin.site.register(ItemInCard)
admin.site.register(Order)
admin.site.register(Size)
admin.site.register(OrderItem)


from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from datetime import datetime, timedelta
from django.utils import timezone
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.auth.models import User

current_year = datetime.now().year


class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return self.name


class Detail(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Size(models.Model):
    name = models.CharField(max_length=3)

    def __str__(self):
        return self.name

class Destination(models.Model):
    country = models.CharField(max_length=50)
    address = models.CharField(max_length=200)
    postal_code = models.CharField(max_length=10)

    def __str__(self):
        return f"{self.address} - {self.country}"

class Product(models.Model):
    category = models.ForeignKey("Category", on_delete=models.CASCADE)
    details = models.ManyToManyField("Detail", blank=True)
    description = models.TextField(blank=True, null=True)
    photo = models.ImageField(upload_to="product_photos", blank=True, null=True)
    price = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    sold = models.BooleanField(default=False)

    class Meta:
        abstract = True


class Jersey(Product):
    club = models.CharField(max_length=100)
    brand = models.CharField(max_length=100, blank=True, null=True)
    year = models.IntegerField(validators=[MinValueValidator(1900), MaxValueValidator(current_year)])
    sizes = models.ManyToManyField(Size)

    def __str__(self):
        return f"Jersey: {self.club}"


class Shorts(Product):
    club = models.CharField(max_length=100)
    year = models.IntegerField(validators=[MinValueValidator(1900), MaxValueValidator(current_year)])
    brand = models.CharField(max_length=100, blank=True, null=True)
    sizes = models.ManyToManyField(Size)

    def __str__(self):
        return f"Shorts: {self.club}"


class ItemInCard(models.Model):
    # Generic relation: can point to Jersey, Card, or Ball
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    product = GenericForeignKey('content_type', 'object_id')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='item_in_cart')

    quantity = models.PositiveIntegerField(default=1)
    player = models.CharField(max_length=20, blank=True, null=True)
    number = models.IntegerField(blank=True, null=True)
    chosen_size = models.ForeignKey(Size, on_delete=models.CASCADE, blank=True, null=True)
    adding_time = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.product} (x{self.quantity})"

class OrderItem(models.Model):
    order = models.ForeignKey('Order', on_delete=models.CASCADE, related_name='order_items')
    product_name = models.CharField(max_length=200)
    product_price = models.PositiveIntegerField()
    quantity = models.PositiveIntegerField()
    chosen_size = models.CharField(max_length=10, blank=True, null=True)
    player = models.CharField(max_length=20, blank=True, null=True)
    number = models.IntegerField(blank=True, null=True)
    product_category = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.product_name} (x{self.quantity})"

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    created_at = models.DateTimeField(auto_now_add=True)
    destination = models.ForeignKey(Destination, on_delete=models.CASCADE, related_name='orders', blank=True, null=True)
    arriving_date = models.DateTimeField(default=timezone.now()+timedelta(days=15))

    @property
    def total_price(self):
        return sum(item.product_price * item.quantity for item in self.order_items.all())
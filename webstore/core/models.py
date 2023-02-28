import uuid
from django.contrib.sessions.models import Session
from django.db import models
from django.urls import reverse
from django.utils import timezone
from django_extensions.db.fields import AutoSlugField
from django.contrib.auth.models import User
from phonenumber_field.modelfields import PhoneNumberField
from .utilis import validate_postcode


class Customer(models.Model):

    def __str__(self):
        return self.user.username

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    firstname = models.CharField(max_length=30)
    lastname = models.CharField(max_length=30)
    phone_number = PhoneNumberField()


class CustomerAddress(models.Model):
    def __str__(self):
        return self.customer

    customer = models.OneToOneField(Customer, on_delete=models.CASCADE)
    city = models.CharField(max_length=50)
    postcode = models.CharField(max_length=50, validators=[validate_postcode])
    street = models.CharField(max_length=100)
    house_number = models.CharField(max_length=20)


class Category(models.Model):
    name = models.TextField()

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("category", self.name)


class Brand(models.Model):
    name = models.TextField()

    def __str__(self):
        return self.name


class Product(models.Model):

    def upload_to(self, filename):
        return f'static/media/{self.brand}/{self.slug}/{filename}'

    def get_absolute_url(self):
        return reverse("product", kwargs={'slug': self.slug})

    def __str__(self):
        return f"{self.name} {self.brand}"

    slug = AutoSlugField(populate_from=['brand__name', 'name', 'category__name'])
    name = models.TextField()
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    description = models.TextField()
    image = models.ImageField(upload_to=upload_to, default='static/media/blank.png')
    base_price = models.DecimalField(max_digits=10, decimal_places=2)
    current_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    no_of_items_in_stock = models.IntegerField(default=0)
    no_of_items_sold = models.IntegerField(default=0)


class Cart(models.Model):
    def __str__(self):
        return f"{self.session} {self.item} {self.quantity} {self.total()}"

    def total(self):
        return self.item.current_price * self.quantity

    session = models.ForeignKey(Session, on_delete=models.CASCADE)
    item = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)


class Order(models.Model):
    def __str__(self):
        return

    STATUS_CHOICES = [
        ('WP', 'Waiting for payment'),
        ('PR', 'Preparing order'),
        ('ID', 'In delivery'),
        ('DE', 'Delivered'),
        ('CS', 'Claim opened'),
        ('CC', 'Claim closed'),
        ('RE', 'Rerturned'),
    ]
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    owner = models.ForeignKey(Customer, on_delete=models.CASCADE)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    paid = models.BooleanField(default=False)
    status = models.CharField(max_length=2, choices=STATUS_CHOICES, default='WP')
    date = models.DateTimeField(default=timezone.now)


class OrderItem(models.Model):
    def __str__(self):
        return f"{self.order.owner} {self.item} {self.total}"

    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    item = models.ForeignKey(Product, on_delete=models.CASCADE)
    amount = models.IntegerField(default=1)
    total = models.DecimalField(max_digits=10, decimal_places=2)

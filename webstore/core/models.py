from django.db import models
from django.urls import reverse
from django_extensions.db.fields import AutoSlugField


class Category(models.Model):
    name = models.TextField()

    def __str__(self):
        return self.name


class Brand(models.Model):
    name = models.TextField()

    def __str__(self):
        return self.name


class Product(models.Model):

    def upload_to(self, filename):
        return f'/products/{self.brand}/{self.slug}/{filename}'

    def get_absolute_url(self):
        return reverse("product", kwargs={'slug': self.slug})

    def __str__(self):
        return f"{self.name} {self.brand}"

    slug = AutoSlugField(populate_from=['brand__name', 'name', 'category__name'])
    name = models.TextField()
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    description = models.TextField()
    image = models.ImageField(upload_to=upload_to, default='blank.png')
    base_price = models.DecimalField(max_digits=10, decimal_places=2)
    current_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    no_of_items_in_stock = models.IntegerField(default=0)
    no_of_items_sold = models.IntegerField(default=0)

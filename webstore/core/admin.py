from django.contrib import admin
from .models import *


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('user',)


@admin.register(CustomerAddress)
class CustomerAddressAdmin(admin.ModelAdmin):
    list_display = ('customer',)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)


@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ('name',)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('slug',)


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('session',)


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('pk',)


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('order',)

@admin.register(Discount)
class DiscountAdmin(admin.ModelAdmin):
    list_display = ('amount',)

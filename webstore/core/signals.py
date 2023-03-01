from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import User, Customer, CustomerAddress, Product, OrderItem


def create_customer(sender, instance, created, **kwargs):
    if created:
        customer = Customer.objects.create(user=instance)
        CustomerAddress.objects.create(customer=customer)


post_save.connect(create_customer, sender=User)


def order_item(sender, instance, created, **kwargs):
    if created:
        item = instance.item
        item.no_of_items_in_stock -= instance.amount
        item.no_of_items_in_stock += instance.amount
        item.save()


post_save.connect(order_item, sender=OrderItem)

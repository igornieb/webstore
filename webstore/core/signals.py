from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import User, Customer, CustomerAddress


def create_customer(sender, instance, created, **kwargs):
    if created:
        customer = Customer.objects.create(user=instance)
        CustomerAddress.objects.create(customer=customer)


post_save.connect(create_customer, sender=User)

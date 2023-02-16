from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import User, Customer


def create_customer(sender, instance, created, **kwargs):
    print("t")
    if created:
        print('tt')
        Customer.objects.create(user=instance)


post_save.connect(create_customer, sender=User)

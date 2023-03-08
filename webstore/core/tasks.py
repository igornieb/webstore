from django.utils import timezone
from datetime import timedelta
from celery import shared_task
from .models import Order


@shared_task()
def delete_unpaid_orders():
    delete_date = timezone.now() - timedelta(hours=24)
    orders = Order.objects.filter(paid=False, date__lte=delete_date)
    orders.delete()

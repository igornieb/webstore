import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'webstore.settings')

app = Celery('app')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

app.conf.beat_schedule = {
    'delete-unpaid-orders-every-1-hour': {
        'task': 'core.tasks.delete_unpaid_orders',
        'schedule': 60*60,
    }
}

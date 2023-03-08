#!/bin/sh
python manage.py makemigrations --no-input
python manage.py migrate --no-input
celery -A webstore beat -l INFO --scheduler django_celery_beat.schedulers:DatabaseScheduler --detach
exec "$@"

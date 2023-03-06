#!/bin/sh
python webstore/manage.py makemigrations --no-input
python webstore/manage.py migrate --no-input
cd webstore
exec "$@"

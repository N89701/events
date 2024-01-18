#!/bin/bash

python manage.py makemigrations

python manage.py migrate

python manage.py collectstatic --no-input

exec gunicorn events.wsgi:application --bind 0:8000
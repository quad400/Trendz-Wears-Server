#!/bin/bash

SUPERUSER_EMAIL=${DJANGO_SUPERUSER_EMAIL}

pip install pip --upgrade && \
pip install -r requirements.txt && \

python manage.py makemigrations --noinput && \
python manage.py migrate --noinput && \
python manage.py createsuperuser --email $SUPERUSER_EMAIL --noinput || true && \

python manage.py collectstatic --noinput

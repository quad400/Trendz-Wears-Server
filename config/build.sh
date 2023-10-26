#!/bin/bash

SUPERUSER_EMAIL=${DJANGO_SUPERUSER_EMAIL}

/opt/venv/bin/pip install pip --upgrade && \
/opt/venv/bin/pip install -r requirements.txt && \

/opt/venv/bin/python manage.py migrate --noinput && \
/opt/venv/bin/python manage.py createsuperuser --email $SUPERUSER_EMAIL --noinput || true && \

/opt/venv/bin/python manage.py collectstatic --noinput


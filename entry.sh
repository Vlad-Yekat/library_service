#!/bin/sh

python3 manage.py migrate && \
# exec gunicorn -c=gunicorn_config.py library_service.wsgi:application

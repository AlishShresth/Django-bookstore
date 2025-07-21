#!/bin/bash
python manage.py migrate
python manage.py collectstatic --noinput
gunicorn --bind 0.0.0.0:10000 your_project.wsgi:application
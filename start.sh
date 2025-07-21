#!/bin/bash
python manage.py migrate
python manage.py collectstatic --noinput
echo "from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.filter(is_superuser=True).exists() or User.objects.create_superuser('admin', 'admin@example.com', os.getenv('SUPERUSER_PASSWORD'))" | python manage.py shell
gunicorn --bind 0.0.0.0:10000 django_project.wsgi:application
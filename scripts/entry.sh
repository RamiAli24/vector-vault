#!/bin/bash

set -o errexit
set -o pipefail
set -o nounset
 
echo "Apply migrations"
python manage.py migrate

 
echo "Creating Superuser..."
echo "from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.create_superuser('$ADMIN_USER', 'test@test-email.com', '$ADMIN_PASSWORD')" | python manage.py shell

echo "Collecting static files"
python manage.py collectstatic --noinput

 
echo "Starting prod server"
gunicorn --worker-class gthread --workers 2 vector_vault.wsgi:application  --bind 0.0.0.0:8000


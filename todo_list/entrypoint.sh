#!/bin/sh

python manage.py makemigrations
python manage.py migrate
python manage.py loaddata db.json
python manage.py collectstatic --no-input
cp -r /app/collected_static/. /backend_static/
cp -r /app/templates/. /backend_static/

gunicorn todo_list.wsgi:application --bind 0.0.0.0:8000
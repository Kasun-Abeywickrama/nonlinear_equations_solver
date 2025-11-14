#!/usr/bin/env bash
# Render startup script

set -o errexit  # exit on error

echo "Running database migrations..."
python manage.py migrate --no-input

echo "Starting Gunicorn server..."
exec gunicorn project_settings.wsgi:application --host 0.0.0.0 --port $PORT --workers 3 --timeout 120
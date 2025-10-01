release: python manage.py migrate && python manage.py collectstatic --noinput --clear

web: gunicorn core.wsgi:application --bind 0.0.0.0:$PORT

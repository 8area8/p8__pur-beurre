release: python manage.py migrate

web: gunicorn app.wsgi
worker: celery worker -A app -E -l debug

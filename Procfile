release: python manage.py migrate && python manage.py collectstatic --noinput

web: gunicorn app.wsgi
worker: celery worker -A app -E -l debug

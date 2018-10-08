release: python manage.py migrate

web: gunicorn pure_beurre.wsgi
worker: celery worker -A pure_beurre -E -l debug

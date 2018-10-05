release: python manage.py migrate

web: gunicorn pure_beurre.wsgi
worker: celery worker -A heroku_blog -E -l debug

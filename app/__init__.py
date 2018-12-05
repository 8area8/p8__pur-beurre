"""Django main init."""

from __future__ import absolute_import, unicode_literals

# This will make sure the app is always imported when
# Django starts so that shared_task will use this app.
from .celery_settings import app as celery_app
from django.conf import settings


__all__ = ('celery_app')

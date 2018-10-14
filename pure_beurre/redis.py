"""Redis object."""

import redis

from django.conf import settings


app = redis.Redis(settings.REDIS_URL)
app.config_get('maxmemory')["maxmemory"] = 16000000

"""Celery tasks.

redis.delete(key) -> delete a key
redis.sadd(key, value) -> add a value in a set key
redis.scard(key) --> len of a set key
redis.smembers("key") --> values of a set key
redis.info()["used_memory"] --> actual used memory
"""

from __future__ import absolute_import, unicode_literals

from celery import shared_task
from django.core.cache import cache

from apps.products.models import Product


# @shared_task
def get_product_names(research):
    """Get product names."""
    products = Product.objects.filter(name__icontains=research)
    if len(products) > 15:
        products = products[:15]
    products = [product.name for product in products]

    return products

"""Celery tasks.

redis.delete(key) -> delete a key
redis.sadd(key, value) -> add a value in a set key
redis.scard(key) --> len of a set key
redis.smembers("key") --> values of a set key
redis.info()["used_memory"] --> actual used memory
"""

from __future__ import absolute_import, unicode_literals

from celery import shared_task
import requests

from pure_beurre import redis_app as redis


@shared_task
def get_product_names():
    """Get product names."""
    redis.delete("product_names")

    for index in range(100):
        get_page_and_put_names_in_redis.delay(index)


@shared_task
def get_page_and_put_names_in_redis(index):
    """Blabla."""
    base_url = "https://fr.openfoodfacts.org/cgi/search.pl"
    print(f"page {index}")

    params = {"action": "process", "page_size": "1000",
              "json": "1", "page": index}
    response = requests.get(base_url, params=params).json()
    products = response["products"]

    for product in products:
        try:
            name = product.get("generic_name", "")
            if not name:
                name = product["generic_name_fr"]
            if not name:
                continue
        except KeyError:
            pass
        else:
            lowered = name.lower()
            redis.sadd("product_names", lowered)

        if int(redis.info()["used_memory"]) >= 16000000:
            break

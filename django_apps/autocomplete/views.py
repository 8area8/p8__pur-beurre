from django.http import HttpResponse, JsonResponse
from django.shortcuts import render

from pure_beurre import redis_app as redis
from . import requests

# Create your views here.


def redis_names(request):
    """Redis event."""
    requests.get_product_names.delay()
    return HttpResponse("good")


def ajax_product_names(request):
    """Return the product names."""
    products = redis.smembers("product_names")
    products_list = [product.decode("utf-8") for product in products]
    return JsonResponse({"resp": products_list})

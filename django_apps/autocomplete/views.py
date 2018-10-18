from django.http import HttpResponse, JsonResponse
# from django.shortcuts import render

from pure_beurre import redis_app as redis
from . import requests

# Create your views here.


def redis_names(request):
    """Redis event."""
    requests.get_product_names.delay()
    return HttpResponse("good")


def ajax_product_names(request):
    """Return the product names."""
    starts_with = request.POST.get("starts_with")
    max_len = int(request.POST.get("max_len"))

    names = redis.smembers("product_names")
    decoded = (name.decode("utf-8") for name in names)
    filtered = (name for name in decoded if starts_with in name)
    sample = [name for index, name in enumerate(filtered) if index < max_len]

    return JsonResponse({"names": sample})

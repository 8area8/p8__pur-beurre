from django.http import HttpResponse
from django.shortcuts import render

from . import requests

# Create your views here.


def redis_names(request):
    """Redis event."""
    requests.get_product_names.delay()
    return HttpResponse("good")

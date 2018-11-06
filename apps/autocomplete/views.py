from django.http import HttpResponse, JsonResponse
# from django.shortcuts import render

from django.core.cache import cache

from apps.autocomplete import tasks

# Create your views here.


def get_names(request):
    """Get product names."""
    research = request.POST.get("starts_with")
    # max_len = int(request.POST.get("max_len"))
    names = tasks.get_product_names(research)
    # decoded = [name.decode("utf-8") for name in names]
    # filtered = (name for name in decoded if starts_with in name)
    # sample = [name for index, name in enumerate(filtered) if index < max_len]

    return JsonResponse({"names": names})

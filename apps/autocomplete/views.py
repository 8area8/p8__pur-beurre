"""Autocomplete views."""

from django.http import JsonResponse
# from django.core.cache import cache

from apps.autocomplete import tasks


def get_names(request):
    """Get product names."""
    research = request.POST.get("starts_with")
    names = tasks.get_product_names(research)

    return JsonResponse({"names": names})

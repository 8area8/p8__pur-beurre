"""Autocomplete views."""

from django.http import JsonResponse

from apps.autocomplete import cache


def get_names(request):
    """Get product names."""
    research = request.POST.get("starts_with")
    names = cache.get_product_names(request, research)

    return JsonResponse({"names": names})

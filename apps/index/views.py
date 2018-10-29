"""Test_index view."""

from django.shortcuts import render


def index(request):
    """Home view."""
    return render(request, "home.html")


# def celery(request):
#     """Celery event."""
#     tasks.add.delay()
#     return JsonResponse({"resp": "django celery works"})

"""Test_index view."""

from django.shortcuts import render
from django.views.generic import TemplateView
from django.http import JsonResponse

from . import tasks


class HomeView(TemplateView):
    """Home view."""
    template_name = "home.html"


def celery(request):
    """Celery event."""
    tasks.add.delay()
    return JsonResponse({"resp": "django celery works"})

"""Test_index view."""

from django.shortcuts import render


def index(request):
    """Home view."""
    return render(request, "home.html", {"site_title": "Home"})


def mentions(request):
    """Mentions view."""
    return render(request, "mentions.html", {"site_title": "Mentions legales"})

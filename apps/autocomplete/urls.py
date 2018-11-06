"""Autocomplete urls."""

from django.urls import path

from . import views


urlpatterns = [
    path('get_names', views.get_names, name='get_names'),
]

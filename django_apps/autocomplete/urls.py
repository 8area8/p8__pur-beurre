"""Autocomplete urls."""

from django.urls import path

from . import views


urlpatterns = [
    path('redis_names', views.redis_names, name='redis_names'),
    path('ajax_product_names', views.ajax_product_names,
         name='ajax_product_names'),
]

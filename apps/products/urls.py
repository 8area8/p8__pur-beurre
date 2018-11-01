"""Index urls."""

from django.urls import path

from . import views


urlpatterns = [
    path('full_in_database', views.full_in_database, name='full_in_database'),
]

from django.urls import path

from . import views

urlpatterns = [
    path('redis_names', views.redis_names, name='redis_names'),
]

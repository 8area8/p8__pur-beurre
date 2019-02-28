"""account urls."""

from django.urls import path
from django.conf.urls import url

from . import views


urlpatterns = [
    path('', views.account, name='account'),
    path('remove_avatar', views.remove_avatar, name='remove_avatar'),
    path('profiles/<username>/', views.profiles, name='profiles'),
]

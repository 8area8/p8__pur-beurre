"""Login urls."""

from django.urls import path
from django.conf.urls import url

from . import views


urlpatterns = [
    path('', views.signup, name=''),
    url('account_activation_sent/$', views.account_activation_sent,
        name='account_activation_sent'),
    path('activate/<uidb64>/<token>/', views.activate, name='activate'),
]

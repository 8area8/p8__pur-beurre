"""Login urls."""

from django.urls import path
from django.conf.urls import url

from . import views


urlpatterns = [
    path('signup', views.signup, name='signup'),
    url('account_activation_sent/$', views.account_activation_sent,
        name='account_activation_sent'),
    path('activate/<uidb64>/<token>/', views.activate, name='activate'),
    path('login', views.login, name='login'),
    path('logout', views.logout, name='logout')
]

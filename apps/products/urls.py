"""Index urls."""

from django.urls import path

from . import views


urlpatterns = [
    path('full_in_database', views.full_in_database, name='full_in_database'),
    path('research_product/<research>/',
         views.research_product, name='research_product'),
    path('results_list/<research>/', views.results_list, name='results_list'),
]

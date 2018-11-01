"""Products view."""

from django.shortcuts import render
from django.contrib.auth.decorators import user_passes_test
from django.conf.urls import url
from django.contrib import admin
from django.http import HttpResponse

from .get_products import ProductsGenerator as generator


@user_passes_test(lambda user: user.is_superuser)
def full_in_database(request):
    """Full in top the database."""
    generator.generate_products.delay()
    return HttpResponse("good")

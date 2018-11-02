"""Products admin."""

from django.contrib import admin
from .models import Product, Category, Substitute

from django.contrib.auth.decorators import user_passes_test
from django.contrib.admin import AdminSite
from django.contrib.admin.apps import AdminConfig
from django.views.decorators.cache import never_cache


@admin.register(Product, Category, Substitute)
class Products(admin.ModelAdmin):
    """Class."""
    pass

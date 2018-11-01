"""Products admin."""

from django.contrib import admin
from .models import Product, Category, Substitute
from .get_products import ProductsGenerator as generator
from django_object_actions import DjangoObjectActions

admin.site.register(Product)
admin.site.register(Category)
admin.site.register(Substitute)

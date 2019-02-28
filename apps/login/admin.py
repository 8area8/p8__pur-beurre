from django.contrib import admin
from .models import Profile

# Register your models here.


@admin.register(Profile)
class Products(admin.ModelAdmin):
    """Class."""
    pass

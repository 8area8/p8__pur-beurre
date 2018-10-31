"""Products models."""

from django.db import models


class Product(models.Model):
    """Product class."""

    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)

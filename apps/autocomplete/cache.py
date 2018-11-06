"""Cache methods."""

from __future__ import absolute_import, unicode_literals

from django.core.cache.backends.base import DEFAULT_TIMEOUT
from django.views.decorators.cache import cache_page
from django.conf import settings

from apps.products.models import Product

CACHE_TTL = getattr(settings, 'CACHE_TTL', DEFAULT_TIMEOUT)


@cache_page(CACHE_TTL)
def dl_products(request):
    """Get product names."""
    return Product.objects.all()


def get_product_names(request, research):
    """Get product names."""
    products = dl_products(request).filter(name__icontains=research)
    if len(products) > 15:
        products = products[:15]
    names = [product.name for product in products]

    return names

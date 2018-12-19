"""Update the products."""

import requests

from django.core.management.base import BaseCommand

from apps.products.models import Product

URL = "https://fr.openfoodfacts.org/cgi/search.pl/"
PARAMETERS = {"page_size": "1000",
              "action": "process",
              "json": "1",
              "page": "1"}


class Command(BaseCommand):
    """Command class."""

    help = 'update all products in database.'

    def add_arguments(self, parser):
        """Arguments."""
        parser.add_argument('--pages', dest='pages', type=int, required=True)

    def handle(self, *args, **options):
        """Handle the command."""
        params = PARAMETERS

        for page_number in range(params["page"]):
            params["page"] = str(page_number + 1)
            url = URL

            response = requests.get(url, params).json()
            products = response["products"]

            for element in products:
                for product in Product.objects.all():
                    name = element["product_name"].replace("/", "-")
                    if product.name == name:
                        product.update(element)

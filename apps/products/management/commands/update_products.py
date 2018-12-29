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
        parser.add_argument('--pages', dest='pages', required=True)

    def handle(self, *args, **options):
        """Handle the command."""
        params = PARAMETERS

        for page_number in range(int(options["pages"])):
            params["page"] = str(page_number + 1)
            print(f"page {page_number + 1}/{int(options['pages'])}")
            url = URL

            response = requests.get(url, params).json()
            products = response["products"]

            for product in products:
                url = str(product.get('url'))
                product_query = Product.objects.filter(open_food_fact_url=url)

                if product_query:
                    product_query[0].update(product)

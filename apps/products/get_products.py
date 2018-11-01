"""Generate the products into the database.

Use "ProductsGenerator.generate_products()".

Interesting OpenFoodFact keys:
    - "image_url" : product image
    - "link" : manufactore site
    - "product_name" : product name
    - "generic_name" : description
    - "categories": str categories
    - "nutrition_grade_fr" : nutriscore
    - "stores" : stores
    - "url" : OpenFoodFAct link

"""

import requests

from django.db import IntegrityError
from django.db.utils import DataError

from .models import Product, Category, Substitute
from celery import shared_task
import celery


URL = "https://fr.openfoodfacts.org/cgi/search.pl/"
PARAMETERS = {"page_size": "1000",
              "action": "process",
              "json": "1",
              "page": "1"}


class ProductsGenerator():
    """Generate the products."""

    @classmethod
    def generate_products(cls, delete_datas=[Product, Category, Substitute],
                          max_pages=10, url=URL, params=PARAMETERS):
        """Get Open Food Fact products."""
        if delete_datas:
            cls._delete_model_datas(delete_datas)

        for page_number in range(max_pages):
            params["page"] = str(page_number + 1)
            _generate_from_a_page.delay(url, params)
            print(f"page {page_number + 1} done.")

    @classmethod
    def _delete_model_datas(cls, models):
        """Delete all model datas."""
        for model in models:
            model.objects.all().delete()

    @classmethod
    def _create(cls, product):
        """Create the product."""
        category_names = product.pop('categories')
        categories = CategoriesHandler.create_categories(category_names)

        try:
            product = Product.objects.create(**product)
            product.categories.add(*categories)
        except (IntegrityError, DataError):
            pass


@shared_task
def _generate_from_a_page(url, params):
    """Generate and filter.

    NOTE: out of the class, to avoid Celery errors.
    """
    response = requests.get(url, params).json()
    products = response["products"]

    for product in products:
        filtered_product = FilterProduct.filtered(product)
        if filtered_product:
            ProductsGenerator._create(filtered_product)


class FilterProduct:
    """Filter product class."""

    @classmethod
    def filtered(cls, product):
        """Filter a product.

        Main method.
        """
        try:
            image = product["image_url"]
            url = product["url"]
            name = product["product_name"]
            categories = product["categories"]
            nutriscore = product["nutrition_grade_fr"]
            assert len(name) <= 150
            assert nutriscore in ("a", "b", "c", "d", "e")
            assert len(nutriscore) == 1
        except (KeyError, AssertionError):
            return None

        filtered = {
            "photo_url": image,
            "open_food_fact_url": url,
            "name": name,
            "categories": categories,
            "nutriscore": nutriscore,
            # OPTIONAL
            "personal_url": product.get("link", ""),
            "description": product.get("generic_name", ""),
            "stores": product.get("stores", ""),
        }
        return filtered


class CategoriesHandler:
    """Create categories and update the product categories field."""

    @classmethod
    def create_categories(cls, category_names):
        """Create and returns the categories."""
        categories = []
        for category in category_names.split(","):
            try:
                category = Category.objects.get(name=category)
            except Category.DoesNotExist:
                category = Category.objects.create(name=category)
            finally:
                categories.append(category)

        return categories

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
from django.core.exceptions import ObjectDoesNotExist
from celery import shared_task

from .models import Product, Category, Substitute


URL = "https://fr.openfoodfacts.org/cgi/search.pl/"
PARAMETERS = {"page_size": "1000",
              "action": "process",
              "json": "1",
              "page": "1"}


class ProductsGenerator():
    """Generate the products."""

    @classmethod
    def generate_products(cls, delete_datas=[Product, Category, Substitute],
                          max_pages=20, url=URL, params=PARAMETERS,
                          celery=True):
        """Get Open Food Fact products."""
        if delete_datas:
            cls._delete_model_datas(delete_datas)

        for page_number in range(max_pages):
            params["page"] = str(page_number + 1)
            if celery:
                _generate_from_a_page.delay(url, params)
            else:
                _generate_from_a_page.apply(args=(url, params)).get()
            print(f"page {page_number + 1} done.")

    @classmethod
    def _delete_model_datas(cls, models):
        """Delete all model datas."""
        for model in models:
            model.objects.all().delete()

    @classmethod
    def create(cls, product):
        """Create the product and the categories."""
        category_names = product.pop('categories')
        categories = CategoriesHandler.create_categories(category_names)
        if not categories:
            return

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
            ProductsGenerator.create(filtered_product)


class FilterProduct:
    """Filter product class."""

    @classmethod
    def filtered(cls, product):
        """Filter a product.

        Main method.
        """
        try:
            image = cls.return_(product["image_url"])
            url = cls.return_(product["url"])
            name = cls.return_(product["product_name"], test_length=True)
            categories = cls.return_(product["categories"])
            nutriscore = cls.return_(product["nutrition_grade_fr"])
            image_nutrition = cls.return_(product["image_nutrition_url"])

            abcde = ("a", "b", "c", "d", "e")
            if nutriscore not in abcde or len(nutriscore) != 1:
                raise ValueError

        except (KeyError, ValueError):
            return None

        filtered = {
            "photo_url": image,
            "open_food_fact_url": url,
            "name": name.replace("/", "-"),  # avoid path error.
            "categories": categories,
            "nutriscore": nutriscore,
            "image_nutrition": image_nutrition,
            # OPTIONAL
            "personal_url": product.get("link", ""),
            "description": product.get("generic_name", ""),
            "stores": product.get("stores", ""),
        }
        return filtered

    @classmethod
    def return_(cls, value, *methods, test_index=True, test_length=False):
        """Return the value or raise ValueError."""
        if test_index:
            cls.is_empty(value)
        if test_length:
            cls.has_good_length(value)

        for method in methods:
            method(value)

        return value

    @classmethod
    def is_empty(cls, value):
        """Raise ValueError if empty."""
        if not value:
            raise ValueError

    @classmethod
    def has_good_length(cls, value):
        """Raise ValueError if length is too high."""
        if len(value) >= 150:
            raise ValueError


class CategoriesHandler:
    """Create categories and update the product categories field."""

    @classmethod
    def create_categories(cls, category_names):
        """Create and returns the categories."""
        categories = []
        for category in category_names.split(","):
            if cls.check_category(category):
                try:
                    category = Category.objects.get(name=category)
                except (Category.DoesNotExist, ObjectDoesNotExist):
                    try:
                        category = Category.objects.create(name=category)
                    except IntegrityError:
                        continue
                categories.append(category)

        return categories

    @classmethod
    def check_category(cls, category):
        """Filter the category."""
        if not category or len(category) < 4 or ":" in category:
            return False
        return True

"""Products tests."""

from django.test import TestCase

from apps.products.models import Category
from apps.products.get_products import CategoriesHandler as cathandler


class CategoriesHandlerTestCase(TestCase):
    """CategoriesHandler tests class."""

    def setUp(self):
        """Set up function."""
        self.catone = Category.objects.create(name="foo")
        self.catwo = Category.objects.create(name="bar")

    def test_create_categories(self):
        """Test create_categories function."""
        category_names = "foo,bar,etc"
        response = cathandler.create_categories(category_names)
        expected = [self.catone, self.catwo, Category.objects.get(name="etc")]
        self.assertEqual(response, expected)

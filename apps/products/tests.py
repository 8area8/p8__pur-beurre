"""Products tests.

NOTE: I don't test generate_products() function.
The function is simple and it would require
to mock the function generate_from_a_page().
"""

import json

import httpretty
from django.test import TestCase, TransactionTestCase
from django.test import Client
from django.contrib.auth.models import User

from apps.products.models import Category, Product, Substitute
from apps.products.tasks import CategoriesHandler as cathandler
from apps.products.tasks import FilterProduct as filtprod
from apps.products.tasks import ProductsGenerator as prodgen
from apps.products.tasks import _generate_from_a_page
from apps.products.substitutes_algo import FindSubstitutes as findsub
from apps.products.substitutes_algo import disable_doubles


class CategoriesHandlerTestCase(TestCase):
    """CategoriesHandler tests class."""

    def setUp(self):
        """Set up function."""
        self.catone = Category.objects.create(name="foololo")
        self.catwo = Category.objects.create(name="barlolo")

    def test_create_categories_one_created(self):
        """Test create_categories function."""
        category_names = "foololo,barlolo,etcfoo"
        response = cathandler.create_categories(category_names)
        self.assertTrue(Category.objects.filter(name="etcfoo").exists())
        expected = [self.catone, self.catwo,
                    Category.objects.get(name="etcfoo")]
        self.assertEqual(response, expected)
        self.assertEqual(len(Category.objects.all()), 3)

    def test_create_categories_zero_created(self):
        """Test create_categories function."""
        category_names = "foololo,barlolo"
        response = cathandler.create_categories(category_names)
        expected = [self.catone, self.catwo]
        self.assertEqual(response, expected)
        self.assertEqual(len(Category.objects.all()), 2)

    def test_create_categories_four_created(self):
        """Test create_categories function."""
        category_names = "lala,lolo,lulu,lili"
        response = cathandler.create_categories(category_names)
        expected = Category.objects.all().exclude(name="foololo")
        expected = expected.exclude(name="barlolo")
        self.assertEqual(response, list(expected))
        self.assertEqual(len(Category.objects.all()), 6)


class FilterProductTestCase(TestCase):
    """FilterProduct tests class."""

    def setUp(self):
        """Set up function."""
        self.base_product = {
            "image_url": "example.com",
            "url": "example.com",
            "product_name": "foo",
            "categories": "one,two,three",
            "nutrition_grade_fr": "a",
            "link": "",
            "generic_name": "",
            "stores": "auchan",
            "image_nutrition_url": "example.com",
            "xxx": "xxx",
            "yyy": "yyy",
            "zzz": "zzz"
        }

    def test_filtered_no_extra_fields(self):
        """Test filtered function."""
        response = filtprod.filtered(self.base_product)
        expected = {
            "photo_url": "example.com",
            "open_food_fact_url": "example.com",
            "name": "foo",
            "categories": "one,two,three",
            "nutriscore": "a",
            "personal_url": "",
            "description": "",
            "stores": "auchan",
            "image_nutrition": "example.com"
        }
        self.assertEqual(response, expected)

    def test_filtered_wrong_name(self):
        """Test filtered function."""
        self.base_product["product_name"] = ""
        response = filtprod.filtered(self.base_product)
        self.assertIsNone(response)

    def test_filtered_wrong_nutriscore(self):
        """Test filtered function."""
        self.base_product["nutrition_grade_fr"] = "ab"
        response = filtprod.filtered(self.base_product)
        self.assertIsNone(response)


class ProductsGeneratorTestCase(TransactionTestCase):
    """ProductsGenerator tests class."""

    def setUp(self):
        """Set up function."""
        pass

    def test_create_DataError(self):
        """Test _create function."""
        filtered = {
            "photo_url": "example.com",
            "open_food_fact_url": "example.com",
            "name": "foo",
            "categories": "fooone,footwo,foothree",
            "nutriscore": "a",
            "personal_url": "x" * 300,
            "description": "",
            "stores": "auchan",
            "image_nutrition": "example.com",
        }
        prodgen._create(filtered)
        self.assertEqual(len(Product.objects.all()), 0)
        self.assertEqual(len(Category.objects.all()), 3)

    def test_create_IntegrityError(self):
        """Test _create function."""
        filtered = {
            "photo_url": "example.com",
            "open_food_fact_url": "example.com",
            "name": "foo",
            "categories": "fooone,footwo",
            "nutriscore": "a",
            "personal_url": "example.com",
            "description": "",
            "stores": "auchan",
            "image_nutrition": "example.com",
        }
        prodgen._create(filtered)
        filtered["categories"] = "fooone,footwo"
        prodgen._create(filtered)
        self.assertEqual(len(Product.objects.all()), 1)
        self.assertEqual(len(Category.objects.all()), 2)

    def test_create_good_result(self):
        """Test _create function."""
        filtered = {
            "photo_url": "example.com",
            "open_food_fact_url": "example.com",
            "name": "foo",
            "categories": "fooone,footwo,foothree",
            "nutriscore": "a",
            "personal_url": "example.com",
            "description": "",
            "stores": "auchan",
            "image_nutrition": "example.com",
        }
        prodgen._create(filtered)
        self.assertTrue(Product.objects.filter(name="foo").exists())
        self.assertEqual(len(Category.objects.all()), 3)

    @httpretty.activate
    def test_generate_from_page_good_result(self):
        """Test generate_from_a_page function.

        NOTE: celery poses some problems during the test.
        I disabled the asynchrone way.
        """
        def mock_requests():
            """Mock json."""
            json = {"products": [{
                    "image_url": "example.com",
                    "url": "example.com",
                    "product_name": "foo",
                    "categories": "fooone,footwo,foothree",
                    "nutrition_grade_fr": "a",
                    "link": "example.com",
                    "generic_name": "",
                    "stores": "auchan",
                    "image_nutrition_url": "example.com",
                    "xxx": "xxx",
                    "yyy": "yyy",
                    "zzz": "zzz"
                    }]}
            return json
        httpretty.register_uri(
            httpretty.GET,
            "https://example.com",
            body=json.dumps(mock_requests()))
        _generate_from_a_page.apply(args=("https://example.com", {})).get()
        self.assertTrue(Product.objects.filter(name="foo").exists())


class ProductViewsTestCase(TestCase):
    """Views tests class."""

    def setUp(self):
        """Set up function."""
        self.client = Client()
        self.product_url = "/products/research_product"
        self.list_url = "/products/results_list"
        self.info_url = "/products/informations"
        self.substitute_url = "/products/save_substitute/"
        User.objects.create_user(username="Foo", email="bar@example.com",
                                 password="super-secret")
        Product.objects.create(name="oreo")
        Product.objects.create(name="oreo2")

    def test_research_product_found(self):
        """Test research_product."""
        self.client.login(email="bar@example.com", password='super-secret')
        product = "oreo"
        response = self.client.get(f"{self.product_url}/{product}/")
        self.assertTemplateUsed(response, "results.html")
        self.assertEqual(response.context["other_results"], 1)
        self.assertTrue(response.context.get("product"))

    def test_research_product_not_found(self):
        """Test research_product."""
        self.client.login(email="bar@example.com", password='super-secret')
        product = "potiron"
        response = self.client.get(f"{self.product_url}/{product}/")
        self.assertTemplateUsed(response, "no_products_found.html")

    def test_results_list_results(self):
        """Test results_list."""
        self.client.login(email="bar@example.com", password='super-secret')
        product = "oreo"
        response = self.client.get(f"{self.list_url}/{product}/")
        self.assertTrue(len(response.context["products"].object_list) == 2)

    def test_results_list_no_results(self):
        """Test results_list."""
        self.client.login(email="bar@example.com", password='super-secret')
        product = "xzxzxz"
        response = self.client.get(f"{self.list_url}/{product}/")
        self.assertTrue(len(response.context["products"].object_list) == 0)

    def test_informations_not_found(self):
        """Test informations."""
        self.client.login(email="bar@example.com", password='super-secret')
        product = "xzxzxz"
        response = self.client.get(f"{self.info_url}/{product}/")
        self.assertTemplateUsed(response, "product_not_found.html")

    def test_informations_found(self):
        """Test informations."""
        self.client.login(email="bar@example.com", password='super-secret')
        product = "oreo"
        response = self.client.get(f"{self.info_url}/{product}/")
        self.assertTemplateUsed(response, "informations.html")
        self.assertTrue(response.context.get("product"))
        self.assertTrue(response.context.get("nutriscore_img"))

    def test_save_substitute_no_double(self):
        """Test informations."""
        user = User.objects.get(email="bar@example.com")
        self.client.login(email="bar@example.com", password='super-secret')
        base_product = Product.objects.get(name="oreo")
        product = Product.objects.get(name="oreo2")
        Substitute.objects.create(user=user, base_product=base_product,
                                  substituted=product)
        response = self.client.post(f"{self.substitute_url}",
                                    {"base_product": base_product,
                                     "product": product,
                                     "next": self.substitute_url})
        self.assertEqual(len(Substitute.objects.all()), 1)

    def test_save_substitute_OK(self):
        """Test informations."""
        user = User.objects.get(email="bar@example.com")
        self.client.login(email="bar@example.com", password='super-secret')
        base_product = Product.objects.get(name="oreo")
        product = Product.objects.get(name="oreo2")
        response = self.client.post(f"{self.substitute_url}",
                                    {"base_product": base_product,
                                     "product": product,
                                     "next": self.substitute_url})
        self.assertEqual(len(Substitute.objects.all()), 1)


class SubstitutesAlgoTestCase(TestCase):
    """Views tests class."""

    def setUp(self):
        """Set up function."""
        for index in range(5):
            Category.objects.create(name=f"cat-{index}")
        nutriscore = 96
        for index in range(10):
            if index % 2 == 0:
                nutriscore += 1
            product = Product.objects.create(name=f"prod-{index}",
                                             nutriscore=chr(nutriscore))
        Product.objects.get(
            name="prod-0").categories.add(*Category.objects.all()[:3])
        Product.objects.get(
            name="prod-2").categories.add(*Category.objects.all()[2:])
        Product.objects.get(
            name="prod-4").categories.add(*Category.objects.all())

    def test_filter_by_nutriscore_a_test(self):
        """Test filter_by_nutriscore function."""
        products = Product.objects
        substitutes = []
        findsub._filter_by_nutriscore("a", products, substitutes)
        self.assertEqual(len(substitutes), 2)
        nutriscores = [prod.nutriscore for prod in substitutes]
        self.assertEqual(nutriscores, ["a", "a"])

    def test_filter_by_nutriscore_no_double(self):
        """Test filter_by_nutriscore function.

        We add a product in the substitutes list before testing.
        """
        products = Product.objects
        substitutes = [products.filter(nutriscore="a")[0]]
        findsub._filter_by_nutriscore("a", products, substitutes)
        self.assertEqual(len(substitutes), 2)
        nutriscores = [prod.nutriscore for prod in substitutes]
        self.assertEqual(nutriscores, ["a", "a"])

    def test_filter_by_nutriscore_b_test(self):
        """Test filter_by_nutriscore function."""
        products = Product.objects
        substitutes = []
        findsub._filter_by_nutriscore("b", products, substitutes)
        self.assertEqual(len(substitutes), 2)
        nutriscores = [prod.nutriscore for prod in substitutes]
        self.assertEqual(nutriscores, ["a", "a"])

    def test_filter_by_nutriscore_c_test(self):
        """Test filter_by_nutriscore function."""
        products = Product.objects
        substitutes = []
        findsub._filter_by_nutriscore("c", products, substitutes)
        self.assertEqual(len(substitutes), 4)
        nutriscores = [prod.nutriscore for prod in substitutes]
        self.assertEqual(nutriscores, ["a", "a", "b", "b"])

    def test_filter_by_nutriscore_d_test(self):
        """Test filter_by_nutriscore function."""
        products = Product.objects
        substitutes = []
        findsub._filter_by_nutriscore("d", products, substitutes)
        self.assertEqual(len(substitutes), 6)
        nutriscores = [prod.nutriscore for prod in substitutes]
        self.assertEqual(nutriscores, ["a", "a", "b", "b", "c", "c"])

    def test_filter_by_nutriscore_e_test(self):
        """Test filter_by_nutriscore function."""
        products = Product.objects
        substitutes = []
        findsub._filter_by_nutriscore("e", products, substitutes)
        self.assertEqual(len(substitutes), 6)
        nutriscores = [prod.nutriscore for prod in substitutes]
        self.assertEqual(nutriscores, ["a", "a", "b", "b", "c", "c"])

    def test_search_in_categories_len_0(self):
        """Test search_in_categories function."""
        product = Product.objects.get(name="prod-0")
        name = product.name
        nutriscore = product.nutriscore
        categories = product.categories.all()
        substitutes = findsub._search_in_categories(name, nutriscore,
                                                    categories)
        self.assertEqual(len(substitutes), 0)

    def test_search_in_categories_len_1(self):
        """Test search_in_categories function."""
        product = Product.objects.get(name="prod-2")
        name = product.name
        nutriscore = product.nutriscore
        categories = product.categories.all()
        substitutes = findsub._search_in_categories(name, nutriscore,
                                                    categories)
        self.assertEqual(len(substitutes), 1)

    def test_search_in_categories_len_2(self):
        """Test search_in_categories function."""
        product = Product.objects.get(name="prod-4")
        name = product.name
        nutriscore = product.nutriscore
        categories = product.categories.all()
        substitutes = findsub._search_in_categories(name, nutriscore,
                                                    categories)
        self.assertEqual(len(substitutes), 2)

    def test_run_ok(self):
        """Test run function."""
        product = Product.objects.get(name="prod-4")
        substitutes = findsub.run(product)
        self.assertEqual(len(substitutes), 2)
        one, two = substitutes
        self.assertEqual(one.nutriscore, "nutriscore-a.png")

    def test_disable_doubles(self):
        """Test disable_doubles function."""
        user = User.objects.create_user(username="foo", password="secret")
        product = Product.objects.get(name="prod-0")
        substituted = Product.objects.get(name="prod-1")
        substitute = Substitute.objects.create(base_product=product,
                                               substituted=substituted,
                                               user=user)
        substitutes = [substituted]
        disable_doubles(substitutes, user)
        self.assertTrue(substitutes[0].double)

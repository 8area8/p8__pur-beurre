from django.core.management.base import BaseCommand, CommandError

from apps.products.tasks import ProductsGenerator as generator


class Command(BaseCommand):
    help = 'Generate all products in database.'

    def handle(self, *args, **options):
        generator.generate_products()

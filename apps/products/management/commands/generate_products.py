from django.core.management.base import BaseCommand, CommandError

from apps.products.tasks import ProductsGenerator as generator


class Command(BaseCommand):
    """Command class."""

    help = 'Generate all products in database.'

    def add_arguments(self, parser):
        """Arguments."""
        # Positional arguments
        parser.add_argument('--pages', dest='pages', type=int, required=True)
        parser.add_argument('--celery', dest='celery',
                            type=bool, required=True)

    def handle(self, *args, **options):
        """Handle the command."""
        generator.generate_products(max_pages=options["pages"],
                                    celery=options["celery"])

from typing import Optional, Any

from django.core.management import BaseCommand
from shopapp.models import Product

class Command(BaseCommand):
    ''' Creates Products '''
    def handle(self, *args: Any, **options: Any) -> Optional[str]:
        self.stdout.write('Create Products')

        products_names = [
            'Smartphone',
            'Laptop',
            'Desktop',
        ]

        for product_name in products_names:
            product, greated = Product.objects.get_or_create(name=product_name)
            self.stdout.write(f"Created {product.name}")

        self.stdout.write(self.style.SUCCESS('Products Created'))
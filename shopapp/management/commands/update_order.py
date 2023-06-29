from typing import Optional, Any

from django.core.management import BaseCommand
from django.contrib.auth.models import User
from shopapp.models import Order, Product

class Command(BaseCommand):
    def handle(self, *args: Any, **options: Any) -> Optional[str]:
        order = Order.objects.first()
        if order:
            products = Product.objects.all()
            for product in products: order.products.add(product)
            order.save()
            self.stdout.write(self.style.SUCCESS(
                f'Successfully added products {order.products.all()} to order {order}'
            ))
        else:
            self.stdout.write('No order found')
            return       
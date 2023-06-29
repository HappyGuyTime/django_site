from typing import Optional, Any, Sequence

from django.core.management import BaseCommand
from django.contrib.auth.models import User
from django.db import transaction

from shopapp.models import Order, Product

class Command(BaseCommand):
    @transaction.atomic
    def handle(self, *args: Any, **options: Any) -> Optional[str]:
        self.stdout.write('Create Order with product')
        user = User.objects.get(username='admin')
        # products: Sequence[Product] = Product.objects.all()
        # products: Sequence[Product] = Product.objects.defer('description', 'price', 'created_at').all()
        products: Sequence[Product] = Product.objects.only('id', 'name').all()
        order, created = Order.objects.get_or_create(
            delivery_address='ul Ivanova d 8',
            promocode='Promo',
            user=user,
        )
        for product in products:
            order.products.add(product)
        order.save()
        self.stdout.write(f'Created Order{order}')
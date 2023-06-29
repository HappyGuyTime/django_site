from typing import Optional, Any

from django.core.management import BaseCommand
from django.contrib.auth.models import User
from django.db.models import Avg, Max, Min, Count, Sum

from shopapp.models import Product, Order

class Command(BaseCommand):
    def handle(self, *args: Any, **options: Any) -> Optional[str]:
        self.stdout.write('Start demo bulk aggregate')

        # result = Product.objects.filter(
        #     name__contains='Smartphone'
        # ).aggregate(
        #     avg_price=Avg('price'),
        #     min_price=Min('price'),
        #     mix_price=Max('price'),
        #     count=Count('id'),
        # )
        # print(result)

        orders = Order.objects.annotate(
            total=Sum('products__price', default=0),
            products_count=Count('products'),
        )

        for order in orders:
            print(f'{order.id} \nCount_products:{order.products_count} \nTotal_price: {order.total}')

        self.stdout.write('Done')
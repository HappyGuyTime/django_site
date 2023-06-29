from io import TextIOWrapper
from csv import DictReader
from django.contrib.auth.models import User
from .models import Product, Order


def save_csv_products(file, encoding):
    csv_file = TextIOWrapper(file, encoding=encoding)
    reader = DictReader(csv_file)
    products = [
        Product(**row)
        for row in reader
    ]
    Product.objects.bulk_create(products)
    return products


def save_csv_orders(file, encoding):
    csv_file = TextIOWrapper(file, encoding=encoding)
    reader = DictReader(csv_file)

    for row in reader:
        delivery_address = row['delivery_address']
        promocode = row['promocode']
        user_id = int(row['user'])
        product_ids = [int(product_id) for product_id in row['products'].split(',')]
        user = User.objects.get(id=user_id)
        order = Order.objects.create(
            delivery_address=delivery_address,
            promocode=promocode,
            user=user
        )
        order.products.set(Product.objects.filter(id__in=product_ids))
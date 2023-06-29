from string import ascii_letters
from random import choices

from django.contrib.auth.models import User, Group, Permission
from django.conf import settings
from django.test import TestCase
from django.urls import reverse
from .models import Product, Order
from .utils import add_two_numbers


class AddTwoNumbersTestCase(TestCase):
    def test_add_two_numbers(self):
        result = add_two_numbers(2, 3)
        self.assertEqual(result, 5)


class ProductCreateViewTestCase(TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        cls.group_qwerty = Group.objects.create(name='qwerty')
        cls.credentials = dict(username='John', password='Smith')
        cls.user = User.objects.create_user(**cls.credentials)
        cls.user.groups.add(cls.group_qwerty)

    @classmethod
    def tearDownClass(cls) -> None:
        cls.user.delete()
        cls.group_qwerty.delete()

    def setUp(self) -> None:
        self.client.login(**self.credentials)
        self.product_name = ''.join(choices(ascii_letters, k=10))
        Product.objects.filter(name=self.product_name).delete()

    def test_create_product(self):
        response = self.client.post(
            reverse("shopapp:create_product"), 
            {
                'name': self.product_name,
                'price': "123.45",
                'description': "A good table",
                'discount': "10",
            }
        )
        self.assertRedirects(response, reverse("shopapp:products_list"))
        self.assertTrue(Product.objects.filter(name=self.product_name).exists())


class ProductDetailsViewTestCase(TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        cls.user = User.objects.create_user(username='John', password='Smith')
        cls.product = Product.objects.create(
            name='Best Product', 
            created_by=cls.user
            )

    @classmethod
    def tearDownClass(cls) -> None:
        cls.product.delete()
        cls.user.delete()

    # def setUp(self) -> None:
    #     self.product = Product.objects.create(name='Best Product')

    # def tearDown(self) -> None:
    #     self.product.delete()

    def test_get_product(self):
        response = self.client.get(reverse('shopapp:product_details', kwargs={'pk': self.product.pk}))
        self.assertEqual(response.status_code, 200)

    def test_get_product_and_check_content(self):
        response = self.client.get(reverse('shopapp:product_details', kwargs={'pk': self.product.pk}))
        self.assertContains(response, self.product.name)


class ProductsListViewTestCase(TestCase):
    fixtures = [
        'user-fixtures.json',
        'group-fixtures.json',
        'product-fixtures.json',
    ]

    def test_products(self):
        response = self.client.get(reverse('shopapp:products_list'))

        # products_response = response.context['products']
        # products = Product.objects.filter(archived=False).all()

        self.assertQuerysetEqual(
            qs=Product.objects.filter(archived=False).all(),
            values=(product.pk for product in response.context['products']),
            transform=lambda product: product.pk,
        )
        self.assertTemplateUsed(response, 'shopapp/products-list.html')

        # for product, product_response in zip(products, products_response):
        #     self.assertEqual(product.pk, product_response.pk)
        # for product in Product.objects.filter(archived=False).all():
        #     self.assertContains(response, product.name)


class ProductsExportViewTestCase(TestCase):
    fixtures = [
        'user-fixtures.json',
        'group-fixtures.json',
        'product-fixtures.json',
    ]

    def test_get_products_view(self):
        response = self.client.get(reverse('shopapp:products_export'))
        self.assertEqual(response.status_code, 200)
        products = Product.objects.order_by('pk').all()
        expeted_data = [
            {
                'pk': product.pk,
                'name': product.name,
                'price': str(product.price),
                'archived': product.archived,
            }
            for product in products
        ]
        products_data = response.json()
        self.assertEqual(
            products_data['products'],
            expeted_data
            )


class OrderDetailViewTestCase(TestCase):
    fixtures = [
        'user-fixtures.json',
        'group-fixtures.json',
        'product-fixtures.json',
    ]

    def setUp(self) -> None:
        self.user = User.objects.get(username='admin')
        self.client.force_login(self.user)
        order = {
            "delivery_address": "ul Gagarina d17",
            "promocode": "SALE123",
            "user": self.user,
        }
        self.order = Order.objects.create(**order)
        self.order.products.set(Product.objects.filter(archived=False))

    def tearDown(self) -> None:
        self.client.logout()
        self.order.delete()

    def test_order_details(self):
        response = self.client.get(reverse('shopapp:order_details', kwargs={'pk': self.order.pk}))
        self.assertContains(response, self.order.delivery_address)
        self.assertContains(response, self.order.promocode)
        self.assertEqual(response.context['order'].pk, self.order.pk)


class OrdersListViewTestCase(TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.user = User.objects.create_user(username='John', password='Smith')

    @classmethod
    def tearDownClass(cls) -> None:
        cls.user.delete()

    def setUp(self) -> None:
        self.client.force_login(self.user)

    def test_orders_view(self):
        response = self.client.get(reverse('shopapp:orders_list'))
        self.assertContains(response, 'Orders')

    def test_orders_view_not_authenticated(self):
        self.client.logout()
        response = self.client.get(reverse('shopapp:orders_list'))
        self.assertEqual(response.status_code , 302)
        self.assertIn(str(settings.LOGIN_URL), response.url)


class OrdersExportViewTestCase(TestCase):
    fixtures = [
        'user-fixtures.json',
        'group-fixtures.json',
        'product-fixtures.json',
        'order-fixtures.json',
    ]

    def setUp(self) -> None:
        self.client.force_login(User.objects.get(username='admin'))

    def test_get_products_view(self):
        response = self.client.get(reverse('shopapp:orders_export'))
        self.assertEqual(response.status_code, 200)
        orders = Order.objects.all()
        expeted_data = [
            {
                'pk': order.pk,
                'delivery_address': order.delivery_address,
                'promocode': order.promocode,
                'user_pk': order.user.pk,
                'products_pk': [product.pk for product in order.products.all()]
            }
            for order in orders
        ]
        orders_data = response.json()
        self.assertEqual(
            orders_data['orders'],
            expeted_data
            )
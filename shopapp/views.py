"""
В этом модуле лежат различные наборы представлений.

Разныу view интернет-магазина: по товарам, заказам и т.д..
"""
import logging
from timeit import default_timer
from typing import Any, Dict, Optional
from csv import DictWriter
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpRequest, HttpResponseRedirect, JsonResponse, Http404
from django.core.cache import cache
from django.contrib.auth.models import Group, User
from django.contrib.syndication.views import Feed
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy, reverse
from django.views import View
from django.views.decorators.cache import cache_page
from django.views.generic import TemplateView, ListView, DetailView, CreateView, UpdateView, DeleteView
from django_filters.rest_framework import DjangoFilterBackend
from django.utils.decorators import method_decorator

from rest_framework.viewsets import ModelViewSet
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.decorators import action
from drf_spectacular.utils import extend_schema, OpenApiResponse

from .models import Product, ProductImage, Order
from .forms import GroupForm, ProductForm, OrderForm
from .serializers import ProductSerializer, OrderSerializer
from .common import save_csv_products

log = logging.getLogger(__name__)

class UserOrdersListView(ListView):
    template_name = 'shopapp/user_orders_list.html'
    context_object_name = 'orders'

    def get_queryset(self):
        try:
            self.owner = User.objects.get(id=self.kwargs['user_id'])
        except User.DoesNotExist:
            raise Http404("User does not exist") 
        queryset = Order.objects.filter(user=self.owner.pk)
        return queryset

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['owner'] = self.owner
        return context


@extend_schema(description='Product views CRUD')
class ProductViewSet(ModelViewSet):
    """
    Набор представлений для действий над Product.
    Полный CRUD для сущностей товара.
    """
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [
        SearchFilter,
        DjangoFilterBackend, 
        OrderingFilter, 
    ]
    search_fields = [
        'name', 'description', 
    ]
    filterset_fields = [
        'name', 'description', 'price', 'discount', 'archived',
    ]
    ordering_fields = [
        'name', 'description', 'price', 'discount', 'archived',
    ]

    @extend_schema(
        summary='Get one product by ID',
        description='Retrieves **product**, returns 404 if not found',
        responses={
            200: ProductSerializer,
            404: OpenApiResponse(description='Empty response, product by id not found'),
        }
        )

    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @action(methods=["get"], detail=False)
    def download_csv(self, request: Request):
        file_name = 'Products-export.csv'
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = f'attachment; file_name={file_name}'
        queryset = self.filter_queryset(self.get_queryset())
        fields = [
            'name', 'description', 'price', 'discount',
        ]
        queryset = queryset.only(*fields)
        writer = DictWriter(response, fieldnames=fields)
        writer.writeheader()
        for product in queryset:
            writer.writerow({
                field: getattr(product, field)
                for field in fields
            })
        return response
    
    @action(methods=['post'], detail=False, parser_classes=[MultiPartParser, ])
    def upload_csv(self, requset: Request):
        products = save_csv_products(requset.FILES['file'].file, requset.encoding)
        serializer = self.get_serializer(products, many=True)
        return Response(serializer.data)

    @method_decorator(cache_page(50))
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)


class OrderViewSet(ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    filter_backends = [
        SearchFilter,
        DjangoFilterBackend, 
        OrderingFilter, 
    ]
    search_fields = [
        'user__username', 'delivery_address', 
    ]
    filterset_fields = [
        'user__username', 'delivery_address', 'promocode', 'products', 
    ]
    ordering_fields = [
        'user', 'delivery_address', 'promocode', 'products',
    ]


class ShopIndexView(View):

    # @method_decorator(cache_page(50))
    def get(self, request: HttpRequest) -> HttpResponse:
        products = [
        ('Smartphone', 999),
        ('Laptop', 1999),
        ('Desktop', 2999),
    ]

        context = {
            'time_running': default_timer(),
            'products' : products,
            'items': 1,
        }
        log.debug('Products for shop index: %s', products)
        log.info('Rendering shop index')
        return render(request, 'shopapp/shop-index.html', context=context)


class GroupsListView(View):
    def get(self, request: HttpRequest) -> HttpResponse:
        context = {
            'form': GroupForm(),
            'groups': Group.objects.prefetch_related('permissions').all(),
        }
        return render(request, 'shopapp/groups_list.html', context=context)

    def post(self, request: HttpRequest):
        form = GroupForm(request.POST)
        if form.is_valid():
            form.save()
        return redirect(request.path)


class ProductsListView(ListView):
    template_name = 'shopapp/products-list.html'
    # model = Product
    queryset = Product.objects.filter(archived=False)
    context_object_name = 'products'


class ProductDetailsView(DetailView):
    template_name = 'shopapp/products-details.html'
    # model = Product
    queryset = Product.objects.filter(archived=False).select_related('created_by').prefetch_related('images')
    context_object_name = 'product'


class ProductCreateView(UserPassesTestMixin, CreateView):
    model = Product
    fields = 'name', 'price', 'description', 'discount', 'preview'
    success_url = reverse_lazy("shopapp:products_list")

    def test_func(self) -> Optional[bool]:
        return self.request.user.groups.filter(name='qwerty').exists()

    def form_valid(self, form) -> HttpResponse:
        form.instance.created_by = self.request.user
        return super().form_valid(form)

 
class ProductUpdateView(UserPassesTestMixin, UpdateView):
    model = Product
    form_class = ProductForm
    # fields = 'name', 'price', 'description', 'discount', 'preview'
    template_name_suffix = '_update_form'

    def test_func(self) -> Optional[bool]:
        return (
            self.request.user.is_superuser or 
            self.request.user == self.object.created_by and self.request.user.has_perm('shopapp.change_product')
        )

    def form_valid(self, form) -> HttpResponse:
        response = super().form_valid(form)
        for image in form.files.getlist('images'):
            ProductImage.objects.create(
                product=self.object,
                image=image,
            )
        return response

    def get_success_url(self) -> str:
        return reverse(
            'shopapp:product_details', kwargs={
                'pk': self.object.pk
                },
        )


class ProductDeleteView(DeleteView):
    model = Product
    success_url = reverse_lazy('shopapp:products_list')

    def form_valid(self, form):
        success_url = self.get_success_url()
        self.object.archived = True
        self.object.save()
        return HttpResponseRedirect(success_url)


class ProductsDataExportView(View):

    def get(self, request: HttpRequest) -> JsonResponse:
        cache_key = 'products_data_export'
        products_data = cache.get(cache_key)
        if products_data is None:
            products = Product.objects.order_by('pk').all()
            products_data = [
                {
                    'pk': product.pk,
                    'name': product.name,
                    'price': product.price,
                    'archived': product.archived,
                }
                for product in products
            ]
            cache.set(cache_key, products_data, timeout=300)
        return JsonResponse({'products': products_data})


class OrdersListView(LoginRequiredMixin, ListView):
    queryset = (
        Order.objects.select_related('user').prefetch_related('products')
    )


class OrderDetailView(PermissionRequiredMixin, DetailView):
    permission_required = 'shopapp.view_order'
    queryset = (
        Order.objects.select_related('user').prefetch_related('products')
    )


class OrderCreateView(CreateView):
    model = Order
    fields = 'products', 'delivery_address', 'promocode'
    success_url = reverse_lazy("shopapp:orders_list")

    def form_valid(self, form) -> HttpResponse:
        form.instance.user = self.request.user
        return super().form_valid(form)


class OrderUpdateView(UpdateView):
    model = Order
    fields = 'products', 'delivery_address', 'promocode'
    template_name_suffix = '_update_form'

    def get_success_url(self) -> str:
        return reverse(
            'shopapp:order_details', kwargs={
                'pk': self.object.pk
                },
        )


class OrderDeleteView(DeleteView):
    model = Order
    success_url = reverse_lazy('shopapp:orders_list')


class OrdersDataExportView(UserPassesTestMixin, View):
    def test_func(self) -> Optional[bool]:
        return self.request.user.is_staff

    def get(self, request: HttpRequest) -> JsonResponse:
        orders = Order.objects.all()
        orders_data = [
            {
                'pk': order.pk,
                'delivery_address': order.delivery_address,
                'promocode': order.promocode,
                'user_pk': order.user.pk,
                'products_pk': [product.pk for product in order.products.all()],
            }
            for order in orders
        ]
        return JsonResponse({'orders': orders_data})


class UserOrdersDataExportView(View):

    def get(self, request: HttpRequest, user_id: int) -> JsonResponse:
        cache_key = f'orders_data_export_user_id_{user_id}'
        orders_data = cache.get(cache_key)
        if orders_data is None:
            try:
                self.owner = User.objects.get(id=user_id)
            except User.DoesNotExist:
                raise Http404("User does not exist")

            orders = Order.objects.filter(user=self.owner.pk)
            orders_data = [
                {
                    'pk': order.pk,
                    'delivery_address': order.delivery_address,
                    'promocode': order.promocode,
                    'user_pk': order.user.pk,
                    'products_pk': [product.pk for product in order.products.all()],
                }
                for order in orders
            ]
        cache.set(cache_key, orders_data, timeout=300)
        return JsonResponse({'orders': orders_data})


class LatestProductsFeed(Feed):
    title = 'Shop products (latest)'
    description = 'Updates on changes and addition shop products'
    link = reverse_lazy('shopapp:products_list')

    def items(self):
        return (
            Product.objects.order_by('-created_at')[:5]
        )
    
    def item_title(self, item: Product) -> str:
        return item.name

    def item_description(self, item: Product) -> str:
        return item.description[0:100] + '...'


###########################################################################################
# 
# def shop_index(request: HttpRequest):
#     products = [
#         ('Smartphone', 999),
#         ('Laptop', 1999),
#         ('Desktop', 2999),
#     ]
# 
#     context = {
#         'time_running': default_timer(),
#         'products' : products,
#     }
#     return render(request, 'shopapp/shop-index.html', context=context)
# 
# 
# def groups_list(request: HttpRequest):
#     context = {
#         'groups': Group.objects.prefetch_related('permissions').all(),
#     }
#     return render(request, 'shopapp/groups_list.html', context=context)
# 
# 
# class ProductDetailsView(View):
#     def get(self, request: HttpRequest, pk: int) -> HttpResponse:
#         # product = Product.objects.get(pk=pk)
#         product = get_object_or_404(Product, pk=pk)
#         context = {
#             'product': product,
#         }
#         return render(request, 'shopapp/products-details.html', context=context)
# 
# 
# class ProductsListView(TemplateView):
#     template_name = 'shopapp/products-list.html'

#     def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
#         context = super().get_context_data(**kwargs)
#         context['products'] = Product.objects.all()
#         return context
# 
# 
# def products_list(request: HttpRequest):
#     context = {
#         'products': Product.objects.all(),
#     }
#     return render(request, 'shopapp/products-list.html', context=context)
# 
# 
# def create_product(request: HttpRequest):
#     if request.method == 'POST':
#         form = ProductForm(request.POST)
#         if form.is_valid():
#             # Product.objects.create(**form.cleaned_data)
#             form.save()
#             url = reverse("shopapp:products_list")
#             return redirect(url)
#     else:
#         form = ProductForm()
#     context = {
#         'form': form,
#     }
#     return render(request, 'shopapp/create-product.html', context=context)
# 
# 
# def orders_list(request: HttpRequest):
#     context = {
#         'orders': Order.objects.select_related('user').prefetch_related('products').all(),
#     }
#     return render(request, 'shopapp/orders_list.html', context=context)
# 
# 
# def create_order(request: HttpRequest):
#     if request.method == 'POST':
#         form = OrderForm(request.POST)
#         if form.is_valid():
#             # Order.objects.create(**form.cleaned_data)
#             form.save()
#             url = reverse("shopapp:orders_list")
#             return redirect(url)
#     else:
#         form = OrderForm()
#     context = {
#         'form': form,
#     }
#     return render(request, 'shopapp/create-order.html', context=context)
# 
#################################################################################################
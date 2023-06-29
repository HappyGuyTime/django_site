from django.contrib import admin
from django.http import HttpRequest, HttpResponse
from django.db.models import QuerySet
from django.shortcuts import render, redirect
from django.urls import path

from io import TextIOWrapper
from csv import DictReader

from .common import save_csv_products, save_csv_orders
from .models import Product, ProductImage, Order
from .admin_mixins import ExportAsCSVMixin
from .forms import CSVImportForm


class OrderInLine(admin.TabularInline):
    model = Product.orders.through

class ProductImageInLine(admin.StackedInline):
    model = ProductImage


@admin.action(description='Archive products')
def mark_archived(model_admin: admin.ModelAdmin, request: HttpRequest, queryset: QuerySet):
    queryset.update(archived=True)


@admin.action(description='Unarchive products')
def mark_unarchived(model_admin: admin.ModelAdmin, request: HttpRequest, queryset: QuerySet):
    queryset.update(archived=False)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin, ExportAsCSVMixin):
    change_list_template = "shopapp/products-change-list.html"

    actions = [
        mark_archived,
        mark_unarchived,
        'export_csv',
    ]
    inlines = [
        OrderInLine,
        ProductImageInLine,
    ]
    list_display = 'pk', 'name', 'description_short', 'price', 'discount', 'archived'
    list_display_links = 'pk', 'name'
    ordering = '-pk','name'
    search_fields = 'name', 'description', 'price'
    fieldsets = [
        (None, {
            'fields': ('name', 'description')
        }),
        ('Price_options', {
            'fields': ('price', 'discount'),
            'classes': ('collapse', 'wide', ),
        }),
        ('Images', {
            'fields': ('preview', ),
        }),
        ('Extra_options', {
            'fields': ('archived', ),
            'classes': ('collapse', ),
            'description': "Extra options, Field 'archived' is for soft delete",
        }),
    ]

    def description_short(self, object: Product) -> str:
        if len(object.description) <= 48:
            return object.description
        else:
            return object.description[:48] + '...'
    
    def import_csv(self, request: HttpRequest) -> HttpResponse:
        if request.method == "GET":
            form = CSVImportForm()
            context = {
                'form': form,
            }
            return render(request, "admin/csv_form.html", context)
        form = CSVImportForm(request.POST, request.FILES)
        if not form.is_valid():
            context = {
                "form": form,
            }
            return render(request, "admin/csv_form.html", context, status=400)
        save_csv_products(file=form.files["csv_file"].file, encoding=request.encoding)
        self.message_user(request, "Data from CSV was imported")
        return redirect("..")

    def get_urls(self):
        urls = super().get_urls()
        new_urls = [
            path("import-products-csv/", self.import_csv, name='import_products_csv')
        ]
        return new_urls + urls

# admin.site.register(Product, ProductAdmin)


# class ProductInLine(admin.TabularInline):
class ProductInLine(admin.StackedInline):
    model = Order.products.through


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    change_list_template = "shopapp/orders-change-list.html"
    inlines = [
        ProductInLine,
    ]
    list_display = 'user_verbose', 'delivery_address', 'promocode', 'created_at'

    def get_queryset(self, request: HttpRequest) -> QuerySet:
        return Order.objects.select_related('user').prefetch_related('products')

    def user_verbose(self, object: Order) -> str:
        return object.user.first_name or object.user.username

    def import_csv(self, request: HttpRequest) -> HttpResponse:
        if request.method == "GET":
            form = CSVImportForm()
            context = {
                'form': form,
            }
            return render(request, "admin/csv_form.html", context)
        form = CSVImportForm(request.POST, request.FILES)
        if not form.is_valid():
            context = {
                "form": form,
            }
            return render(request, "admin/csv_form.html", context, status=400)
        save_csv_orders(file=form.files["csv_file"].file, encoding=request.encoding)
        self.message_user(request, "Data from CSV was imported")
        return redirect("..")

    def get_urls(self):
        urls = super().get_urls()
        new_urls = [
            path("import-orders-csv/", self.import_csv, name='import_orders_csv')
        ]
        return new_urls + urls
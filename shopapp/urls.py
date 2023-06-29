from django.urls import path, include
from django.views.decorators.cache import cache_page
from rest_framework.routers import DefaultRouter

from .views import (
    ShopIndexView, GroupsListView,
    ProductDetailsView, ProductsListView, ProductCreateView, ProductUpdateView, 
    ProductDeleteView, ProductsDataExportView, ProductViewSet, LatestProductsFeed,
    OrdersListView, OrderDetailView, OrderCreateView, UserOrdersListView, UserOrdersDataExportView,
    OrderUpdateView, OrderDeleteView, OrdersDataExportView, OrderViewSet
    )

app_name = 'shopapp'

routers = DefaultRouter()
routers.register("products", ProductViewSet)
routers.register("orders", OrderViewSet)

urlpatterns = [
    # path("", cache_page(50)(ShopIndexView.as_view()), name="index"),
    path("", ShopIndexView.as_view(), name="index"),
    path("api/", include(routers.urls)),
    path("groups/", GroupsListView.as_view(), name="groups_list"),

    path("products/", ProductsListView.as_view(), name="products_list"),
    path("products/create/", ProductCreateView.as_view(), name="create_product"),
    path("products/<int:pk>/", ProductDetailsView.as_view(), name="product_details"),
    path("products/<int:pk>/update/", ProductUpdateView.as_view(), name="product_update"),
    path("products/<int:pk>/archive/", ProductDeleteView.as_view(), name="product_delete"),
    path("products/export/", ProductsDataExportView.as_view(), name="products_export"),
    path("products/latest/feed/", LatestProductsFeed(), name="products_feed"),

    path("orders/", OrdersListView.as_view(), name="orders_list"),
    path("orders/create/", OrderCreateView.as_view(), name="create_order"),
    path("orders/<int:pk>/", OrderDetailView.as_view(), name="order_details"),
    path("orders/<int:pk>/update/", OrderUpdateView.as_view(), name="order_update"),
    path("orders/<int:pk>/delete/", OrderDeleteView.as_view(), name="order_delete"),
    path("orders/export/", OrdersDataExportView.as_view(), name="orders_export"),
    path("orders/user/<int:user_id>/", UserOrdersListView.as_view(), name="user_orders"),
    path("orders/user/<int:user_id>/export/", UserOrdersDataExportView.as_view(), name="user_orders_export"),
]

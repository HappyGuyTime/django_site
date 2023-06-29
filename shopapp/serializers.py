from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Product, Order


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = (
            "pk", "name", "description", "price", 
            "discount", "created_at", "archived", 
            "preview",
        )


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "pk", "username", 
        )


class OrderSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    class Meta:
        model = Order
        fields = (
            "pk", "user", "delivery_address", "promocode", 
            "created_at", "products", "receipt",
        )
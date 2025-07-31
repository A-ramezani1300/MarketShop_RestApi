from rest_framework import serializers
from shop.serializers import ProductSerializer
from .models import *



class CartItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer()
    class Meta:
        model = CartItem
        fields = ['id', 'cart', 'product', 'quantity', 'created', 'updated']


class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True)

    class Meta:
        model = Cart
        fields = ['id', 'user', 'items', 'created', 'updated']
        read_only_fields = ['id', 'created', 'updated']


class AddToCartSerializer(serializers.Serializer):
    product_id = serializers.IntegerField()
    quantity = serializers.IntegerField(default=0)


# class CartItemSerializer(serializers.ModelSerializer):
#     product = ProductSerializer()
#     class Meta:
#         model = CartItem
#         fields = ['id', 'cart', 'product', 'quantity', 'created', 'updated']



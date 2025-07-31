from rest_framework import  serializers
from .models import *





class OrderItemSerializer(serializers.ModelSerializer):
    get_cost = serializers.ReadOnlyField()

    class Meta:
        model = OrderItem
        fields = ['id', 'order', 'product', 'quantity', 'price', 'created', 'get_cost']



class OrdersSerializer(serializers.ModelSerializer):
    get_total_price = serializers.IntegerField(read_only=True)
    # orderitems = OrderItemSerializer(many=True, read_only=True)

    class Meta:
        model = Orders
        fields = ['id', 'buyer', 'payment', 'created', 'updated', 'get_total_price']
        read_only_fields = ['id', 'buyer', 'created', 'updated']



class DiscountSerializer(serializers.Serializer):
    code = serializers.CharField()


from django.shortcuts import render
from rest_framework.generics import get_object_or_404, RetrieveAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import generics, status
from rest_framework.mixins import CreateModelMixin, UpdateModelMixin
from .models import Cart, CartItem
from shop.models import Category, Product
from account.models import UserShop
from .serializers import CartSerializer, CartItemSerializer, AddToCartSerializer
from rest_framework.permissions import IsAdminUser, IsAuthenticated





class AddToCartView(generics.GenericAPIView, CreateModelMixin):
    permission_classes = [IsAdminUser, IsAuthenticated]
    queryset = Cart.objects.all()
    serializer_class = CartSerializer

    def post(self, request, *args, **kwargs):
        serializer = AddToCartSerializer(data=request.data)
        if serializer.is_valid():
            product_id = serializer.validated_data['product_id']
            quantity = serializer.validated_data['quantity']
            product = get_object_or_404(Product, id=product_id)
            cart, created = Cart.objects.get_or_create(user=request.user)
            cart_items, created = CartItem.objects.get_or_create(cart=cart, product=product, quantity=quantity)
            if created:
                cart_items.quantity = quantity # مقداردهی اولیه
            else:
                cart_items.quantity += quantity  # اضافه کردن به مقدار فعلی
            cart_items.save()
            print(cart_items)
            return Response({'success': 'Product by successfully added to cart!'}, status=status.HTTP_201_CREATED)
        return Response({'error': 'Product not Found or Invalid Request!'})


    # def delete(self, request, product_id):
    #     cart = get_object_or_404(Cart, user=request.user)
    #     cart_item = get_object_or_404(CartItem, cart=cart, product_id=product_id)
    #     cart_item.delete()
    #     return Response({'message': 'Product removed from cart successfully!'}, status=status.HTTP_200_OK)


class RemoveFromCartView(APIView):
    def delete(self, request, product_id):
        cart = get_object_or_404(Cart, user=request.user)
        cart_item = get_object_or_404(CartItem, cart=cart, product_id=product_id)
        cart_item.delete()
        return Response({'message': 'Product removed from cart successfully!'}, status=status.HTTP_200_OK)



class CartDetail(RetrieveAPIView):
    serializer_class = CartSerializer()
    def get_object(self):
        return get_object_or_404(Cart, user=self.request.user)

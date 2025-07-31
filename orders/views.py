from django.db import transaction
from django.views import View
from rest_framework.response import Response
from rest_framework.views import APIView
from cart.models import CartItem, Cart
from shop.models import Product
from .models import Orders, OrderItem
from .serializers import OrdersSerializer, OrderItemSerializer, DiscountSerializer
from rest_framework import status, generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination
from rest_framework.generics import CreateAPIView, RetrieveAPIView, DestroyAPIView, get_object_or_404, ListCreateAPIView
import json
import requests
from django.conf import settings
from rest_framework.mixins import CreateModelMixin




class OrderApiView(CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = OrdersSerializer
    queryset = Orders.objects.all()
    pagination_class = PageNumberPagination

    def create(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return Response({'error':'user not authenticated'}, status=status.HTTP_400_BAD_REQUEST)
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            order_instance = serializer.save(buyer=request.user)  # ذخیره سفارش اصلی
            items = request.data.get("items", [])  # دریافت لیست آیتم‌های سفارش از داده‌های درخواست
            for item in items:
                item_serializer = OrderItemSerializer(data={**item, "order": order_instance.id})
                if item_serializer.is_valid():
                    item_data = item_serializer.validated_data
                    item_serializer.save(order=order_instance, product=item_data['product'],
                                         quantity=item_data['quantity'], price=item_data['price'])
                    item_serializer.save()
                    print(item_serializer)
                else:
                    return Response({'error':'Invalid request, order not created'}, status=status.HTTP_400_BAD_REQUEST)
            return Response({'success':'order by successfully created!'}, status=status.HTTP_201_CREATED)
        return Response({'error':'Order creation failed'}, status=status.HTTP_400_BAD_REQUEST)



class OrderDetailApiView(RetrieveAPIView):
    serializer_class = OrdersSerializer()
    def get_object(self):
        order = get_object_or_404(Orders, buyer=self.request.user)
        discount_serializer = DiscountSerializer(data=self.request.query_params)
        if discount_serializer.is_valid():
            discount_code = discount_serializer.validated_data.get('code')
            if discount_code == 'code':
                order.save()
            return Response({'success':'discount code by successfully applied'}, status=status.HTTP_200_OK)
        return Response({'error':'discount code invalid or Credit'}, status=status.HTTP_400_BAD_REQUEST)



# class OrderCreateView(APIView):
#     def post(self, request):
#         user = request.user
#         cart_items = CartItem.objects.filter(user=user)
#         if not cart_items.exists():
#             return Response({"error": "سبد خرید شما خالی است."}, status=status.HTTP_400_BAD_REQUEST)
#         order = Orders.objects.create(buyer=user)
#         for item in cart_items:
#             OrderItem.objects.create(
#                 order=order,
#                 product=item.product,
#                 price=item.product.price,  # قیمت محصول را از مدل `Product` دریافت می‌کنیم
#                 quantity=item.quantity
#             )
#             # حذف اقلام از سبد خرید پس از ایجاد سفارش
#             cart_items.delete()
#         return Response({"success": "سفارش شما با موفقیت ثبت شد.", "order_id": order.id},
#                         status=status.HTTP_201_CREATED)




# class OrdersListCreate(ListCreateAPIView):
#     permission_classes = [IsAuthenticated]
#     serializer_class = OrdersSerializer
#     model = serializer_class.Meta.model
#
#     def get_queryset(self):
#         return self.request.user.order_set
#
#     def create(self, request, *args, **kwargs):
#         self.serializer_class.Meta.depth = 0
#         response = self.request.user.cart.create_order()
#         if response:
#             ser = OrderItemSerializer(instance=response, many=True)
#             return Response(ser.data, status=status.HTTP_201_CREATED)
#         return Response({'error': 'The shopping cart may be empty.'}, status=status.HTTP_400_BAD_REQUEST)



# if settings.SANDBOX:
#     sandbox = 'sandbox'
# else:
#     sandbox = 'www'
#
# ZP_API_REQUEST = f"https://{sandbox}.zarinpal.com/pg/rest/WebGate/PaymentRequest.json"
# ZP_API_VERIFY = f"https://{sandbox}.zarinpal.com/pg/rest/WebGate/PaymentVerification.json"
# ZP_API_STARTPAY = f"https://{sandbox}.zarinpal.com/pg/StartPay/"
#
# amount = 1000  # Rial / Required
# description = "توضیحات مربوط به تراکنش را در این قسمت وارد کنید"  # Required
# phone = 'YOUR_PHONE_NUMBER'  # Optional
# # Important: need to edit for realy server.
# CallbackURL = 'http://127.0.0.1:8080/verify/'
#
#
# class OrderPayApiView(APIView):
#     def get(self, request, order_id):
#         order = Orders.objects.get(id=order_id)
#         request.session['order_pay'] = {
#             'order_id': order.id
#         }
#         data = {
#             "MerchantID": settings.MERCHANT,
#             "Amount": order.get_total_price(),
#             "Description": description,
#             # "Phone": phone,
#             "CallbackURL": CallbackURL,
#         }
#         data = json.dumps(data)
#         # set content length by data
#         headers = {'content-type': 'application/json', 'content-length': str(len(data))}
#         try:
#             response = requests.post(ZP_API_REQUEST, data=data, headers=headers, timeout=10)
#
#             if response.status_code == 200:
#                 response = response.json()
#                 if response['Status'] == 100:
#                     return {'status': True, 'url': ZP_API_STARTPAY + str(response['Authority']),
#                             'authority': response['Authority']}
#                 else:
#                     return {'status': False, 'code': str(response['Status'])}
#             return response
#
#         except requests.exceptions.Timeout:
#             return {'status': False, 'code': 'timeout'}
#         except requests.exceptions.ConnectionError:
#             return {'status': False, 'code': 'connection error'}
#
#
#
# class OrderVerifyView(APIView):
#     # def verify(authority):
#     def get(self, request):
#         order_id = request.session['order_pay']['order_id']
#         order = Orders.objects.get(id=int(order_id))
#         data = {
#             "MerchantID": settings.MERCHANT,
#             "Amount": order.get_total_price(),
#             "Authority": authority,
#         }
#         data = json.dumps(data)
#         # set content length by data
#         headers = {'content-type': 'application/json', 'content-length': str(len(data))}
#         response = requests.post(ZP_API_VERIFY, data=data, headers=headers)
#
#         if response.status_code == 200:
#             response = response.json()
#             if response['Status'] == 100:
#                 return {'status': True, 'RefID': response['RefID']}
#             else:
#                 return {'status': False, 'code': str(response['Status'])}
#         return response


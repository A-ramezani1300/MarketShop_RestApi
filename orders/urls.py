from django.urls import path
from . import views


app_name = 'orders'


urlpatterns = [
    path('order_create/', views.OrderApiView.as_view(), name='order_create'),
    path('order_detail/<int:pk>/', views.OrderDetailApiView.as_view(), name='order_detail'),
    # path('order_delete/<int:pk>/', views.OrderApiView.as_view(), name='order_delete'),
    # path('order_item_detail/<int:pk>/', views.OrderItemApiView.as_view(), name='order_item_detail'),
    # path('order_verify/', views.OrderVerifyView.as_view(), name='order_verify'),
]

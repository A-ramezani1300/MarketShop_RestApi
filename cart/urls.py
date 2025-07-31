from django.urls import path
from . import views


app_name = 'cart'

urlpatterns = [
    path('add_to_cart/', views.AddToCartView.as_view(), name='add_to_cart'),
    path('remove/<int:pk>/', views.RemoveFromCartView.as_view(), name='remove'),
    path('cart_detail/', views.CartDetail.as_view(), name='cart_detail'),
]

from django.db import models
from account.models import UserShop
from shop.models import Product


class Cart(models.Model):
    user = models.ForeignKey(UserShop, on_delete=models.CASCADE, related_name='cart', verbose_name='کاربر')
    created = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')
    updated = models.DateTimeField(auto_now=True, verbose_name='تاریخ بروز رسانی')


    class Meta:
        ordering = ['user']
        indexes = [
            models.Index(fields=['user'])
        ]

        verbose_name = 'سبد خرید'
        verbose_name_plural = 'سبد خریدها'

    def __str__(self):
        return str(self.user)


class CartItem(models.Model):
    STATUS_CHOICES = [
        ('Waiting for an order', 'در انتظار ثبت سفارش'),
        ('order created', 'سفارش ثبت شد')
    ]
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='cart_item', verbose_name='سبد خرید')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='محصول')
    quantity = models.PositiveSmallIntegerField(default=0, verbose_name='تعداد')
    added_to_cart = models.DateTimeField(auto_now_add=True, blank=True, null=True, verbose_name='اضافه شده به سبد خرید')
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='pending')
    created = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')
    updated = models.DateTimeField(auto_now=True, verbose_name='تاریخ بروز رسانی')


    class Meta:
        ordering = ['cart', '-created']
        indexes = [
            models.Index(fields=['cart'])
        ]

        verbose_name = 'آیتم سبد خرید'
        verbose_name_plural = 'آیتمهای سبد خرید'

    def __str__(self):
        return f"{self.quantity} of {self.product.name} in cart"




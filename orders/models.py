from django.db import models
from account.models import UserShop
from shop.models import Product
from django.core.validators import MinValueValidator, MaxValueValidator



class Orders(models.Model):
    buyer = models.ForeignKey(UserShop, on_delete=models.CASCADE, related_name='orders', verbose_name='کاربر')
    payment = models.BooleanField(default=False, verbose_name='پرداخت')
    discount = models.IntegerField(default=None, blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')
    updated = models.DateTimeField(auto_now=True, verbose_name='تاریخ بروزرسانی')


    class Meta:
        ordering = ['-created']
        verbose_name = 'سفارش'
        verbose_name_plural = 'سفارشات'


    def get_total_price(self):
        return sum(item.get_cost() for item in self.items.all())


    def __str__(self):
        return f"Order {self.buyer}"



class OrderItem(models.Model):
    order = models.ForeignKey(Orders, on_delete=models.CASCADE, related_name='items', verbose_name='سفارش')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='محصول')
    quantity = models.PositiveIntegerField(default=0, verbose_name='تعداد')
    price = models.IntegerField(verbose_name='مبلغ کل هر محصول')
    created = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')


    class Meta:
        ordering = ['order']
        verbose_name = 'آیتم سفارش'
        verbose_name_plural = 'آیتم‌های سفارش'


    def get_cost(self):
        return self.price * self.quantity

    def __str__(self):
        return f"{self.quantity} x {self.product} (Order {self.order.id})"



class DiscountPercentage(models.Model):
    code = models.CharField(max_length=30, unique=True, verbose_name='کد تخفیف')
    valid_from = models.DateTimeField(verbose_name='شروع اعتبار')
    valid_to = models.DateTimeField(verbose_name='پایان اعتبار')
    discount = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(90)], verbose_name='درصد تخفیف')
    active = models.BooleanField(default=False, verbose_name='فعال')


    class Meta:
        ordering = ['code', 'active']
        verbose_name = 'تخفیف'
        verbose_name_plural = 'تخفیفات'


    def __str__(self):
        return self.code


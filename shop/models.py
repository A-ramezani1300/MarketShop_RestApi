import django_filters
from django.db import models
from django.template.defaultfilters import slugify
from django.urls import reverse
from account.models import UserShop
from ckeditor.fields import RichTextField


class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name='نام دسته بندی')
    slug = models.SlugField(max_length=100, unique=True, verbose_name='اسلاگ')

    class Meta:
        ordering = ['name']
        indexes = [
            models.Index(fields=['name', 'slug'])
        ]

        verbose_name = 'دسته بندی'
        verbose_name_plural = 'دسته بندی ها'

    def get_absolute_url(self):
        return reverse('shop:category', args=[self.slug])

    def __str__(self):
        return self.name


class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True, blank=True, related_name='products', verbose_name='دسته بندی محصول')
    name = models.CharField(max_length=100, verbose_name='اسم محصول')
    slug = models.SlugField(max_length=100, unique=True, verbose_name='اسلاگ')
    description = RichTextField()
    # description = models.TextField(max_length=1000, verbose_name='توضیحات محصول')
    weight = models.PositiveIntegerField(default=0, verbose_name="وزن محصول")
    quantity = models.PositiveIntegerField(default=0, verbose_name='تعداد')
    price = models.PositiveSmallIntegerField(default=0, verbose_name='قیمت')
    discount_percent = models.PositiveSmallIntegerField(default=0, verbose_name='درصد تخفیف محصول')
    inventory = models.PositiveSmallIntegerField(default=0, verbose_name='موجودی محصول')
    created = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد محصول')
    updated = models.DateTimeField(auto_now=True, verbose_name='تاریخ اپدیت محصول')

    # محاسبه درصد تخفیف قیمت هر غذا
    def get_discounted_price(self):
        discount_amount = self.price * (self.discount_percent / 100)
        discount_price = self.price - discount_amount
        return discount_price

    class Meta:
        ordering = ['name']
        indexes = [
            models.Index(fields=['name', 'id', 'slug'])
        ]

        verbose_name = 'محصول'
        verbose_name_plural = 'محصولات'

    def get_absolute_url(self):
        return reverse('shop:product_detail', args=[self.slug])

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name



class Image(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images', verbose_name='تصویر محصول')
    name = models.CharField(max_length=100, blank=True, null=True, verbose_name='نام عکس')
    description = models.TextField(null=True, blank=True, verbose_name='توضیحات تصویر')
    image_field = models.ImageField(upload_to='product_images/%Y/%m/%d/')
    created = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد تصویر')

    class Meta:
        ordering = ['-created']
        indexes = [
            models.Index(fields=['-created'])
        ]
        verbose_name = 'تصویر'
        verbose_name_plural = 'تصویرها'

    def delete(self, *args, **kwargs):
        storage, path = self.image_field.storage, self.image_field.path
        storage.delete(path)
        super().delete(*args, **kwargs)

    def __str__(self):
        return self.name if self.name else 'None'


class Comment(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='comments', blank=True, null=True, verbose_name='کامنت محصول')
    name = models.ForeignKey(UserShop, on_delete=models.CASCADE, related_name='user_comments', blank=True, null=True, verbose_name='کاربر')
    reply = models.ForeignKey('self', on_delete=models.CASCADE, related_name='reply_comment', blank=True, null=True,verbose_name='ریپلای')
    is_reply = models.BooleanField(default=False, verbose_name='ریپلای شده')
    message = models.TextField(max_length=1000, verbose_name='متن کامنت')
    created = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد کامنت')
    updated = models.DateTimeField(auto_now=True, verbose_name='تاریخ بروز رسانی کامنت')


    class Meta:
        ordering = ['name', '-created']
        indexes = [
            models.Index(fields=['name', '-created'])
        ]

        verbose_name = 'کامنت'
        verbose_name_plural = 'کامنت ها'

    def __str__(self):
        return self.message


class Ticket(models.Model):
    class Status(models.TextChoices):
        OPEN = 'open', 'باز',
        CLOSED = 'closed', 'بسته'

    name = models.CharField(max_length=100, verbose_name='نام')
    phone = models.IntegerField(verbose_name='تلفن')
    title = models.CharField(max_length=100, null=True, blank=True, verbose_name='عنوان تیکت')
    department = models.CharField(max_length=100, null=True, blank=True, verbose_name='دپارتمان')
    subject = models.CharField(max_length=100, null=True, blank=True, verbose_name='موضوع تیکت')
    message = models.TextField(max_length=5500, verbose_name='متن تیکت')
    status = models.CharField(max_length=100, choices=Status.choices, default=Status.OPEN, verbose_name='وضعیت تیکت')
    created = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد تیکت')
    updated = models.DateTimeField(auto_now=True, verbose_name='تاریخ اپدیت تیکت')

    class Meta:
        ordering = ['phone', '-created']
        indexes = [
            models.Index(fields=['phone', '-created'])
        ]

        verbose_name = 'تیکت'
        verbose_name_plural = 'تیکت ها'

    def __str__(self):
        return self.name


class TicketResponse(models.Model):
    ticket = models.ForeignKey(Ticket, on_delete=models.SET_NULL, null=True, related_name='responses', verbose_name='پاسخ تیکت')
    user_response = models.ForeignKey(UserShop, on_delete=models.SET_NULL, null=True, related_name='user_response', verbose_name='ادمین')
    message = models.TextField(verbose_name='متن پاسخ به تیکت')
    created = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ پاسخ به تیکت')
    updated = models.DateTimeField(auto_now=True, verbose_name='تاریخ اپدیت پاسخ تیکت')

    class Meta:
        ordering = ['-created']
        indexes = [
            models.Index(fields=['-created'])
        ]

        verbose_name = 'پاسخ تیکت'
        verbose_name_plural = 'پاسخ تیکتها'

    def __str__(self):
        return f'پاسخ به تیکت {self.ticket.subject} توسط {self.user_response}'



class ProductFilter(django_filters.FilterSet):
    category = django_filters.CharFilter(field_name='category__name', lookup_expr='exact')
    name = django_filters.CharFilter(lookup_expr='icontains')
    price = django_filters.RangeFilter()

    class Meta:
        model = Product
        fields = ['price', 'name', 'category']
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager


class UserManager(BaseUserManager):
    def create_user(self, phone, password=None, **extra_fields):
        if not phone:
            raise ValueError('شماره تلفن اجباری است!')
        user = self.model(phone=phone, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, phone, password=None, **extra_fields):
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_admin', True)

        if extra_fields.get('is_superuser') is not True:
            raise ValueError('is_superuser must be true')
        if extra_fields.get('is_staff') is not True:
            raise ValueError('is_staff must be true')
        if extra_fields.get('is_admin') is not True:
            raise ValueError('is_admin must be true')

        return self.create_user(phone, password, **extra_fields)


class UserShop(AbstractBaseUser, PermissionsMixin):
    first_name = models.CharField(max_length=100, verbose_name='نام')
    last_name = models.CharField(max_length=100, verbose_name='نام خانوادگی')
    phone = models.CharField(max_length=11, unique=True, verbose_name='تلفن')
    email = models.EmailField(max_length=355, verbose_name='ایمیل')
    address = models.TextField(max_length=1500, verbose_name='آدرس')
    image_field = models.ImageField(upload_to='profile_image/%Y/%m/%d/', blank=True, null=True, verbose_name='تصویر پروفایل')
    is_superuser = models.BooleanField(default=False, verbose_name='کاربر ویژه')
    is_admin = models.BooleanField(default=False, verbose_name='کاربر ادمین')
    is_active = models.BooleanField(default=True, verbose_name='کاربر فعال')
    is_staff = models.BooleanField(default=True, verbose_name='کاربر سایت')
    created = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد یوزر')
    updated = models.DateTimeField(auto_now=True, verbose_name='تاریخ اپدیت یوزر')

    objects = UserManager()

    USERNAME_FIELD = 'phone'
    REQUIRED_FIELDS = []

    class Meta:
        ordering = ['first_name', 'last_name']
        indexes = [
            models.Index(fields=['first_name', 'last_name', 'phone'])
        ]

        verbose_name = 'اکانت'
        verbose_name_plural = 'اکانت ها'

    def __str__(self):
        return self.first_name

    def has_perm(self, perm, obj=None):
        # بازگرداندن True برای تعیین مجوزهای کاربر
        return True

    def has_module_perms(self, app_label):
        # بازگرداندن True برای تعیین مجوزهای ماژول کاربر
        return True



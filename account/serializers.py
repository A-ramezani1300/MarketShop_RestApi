from django.contrib.auth import authenticate
from rest_framework import serializers
from .models import *
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.tokens import RefreshToken




class UserSerializer(serializers.ModelSerializer):
    phone = serializers.CharField()
    password = serializers.CharField(write_only=True)

    class Meta:
        model = UserShop
        fields = ['id', 'first_name', 'last_name', 'phone', 'password', 'email', 'address']
        read_only_fields = ['id', 'password', 'is_superuser', 'is_admin', 'is_staff', 'is_active', 'created', 'updated']
        extra_kwargs = {
            'id': {'read_only': True},
            'is_superuser': {'read_only': True},
            'is_admin': {'read_only': True},
            'is_staff': {'read_only': True},
            'is_active': {'read_only': True},
            'created': {'read_only': True},
            'updated': {'read_only': True},
        }

    def validate_phone_number(self, value):
        if not value.startswith('09') and not value.isdigit():
            raise serializers.ValidationError("شماره تلفن باید معتبر باشد و با پیشوند مناسب شروع شود!")
        return value

    def validate_unique_phone_number(self, value):
        if UserShop.objects.filter(phone=value).exists():
            return serializers.ValidationError('شماره تلفن تکراری است!')


# def create(self, validated_data):
    #     user = UserShop(phone=validated_data['phone'])
    #     # user.set_password(validated_data['password'])
    #     user.save()
    #     return user

    # def validate(self, data):
    #     user = authenticate(phone=data['phone'], password=data['password'])
    #     if not user:
    #         raise serializers.ValidationError('نام کاربری یا رمز عبور نادرست است')
    #     return user

    # def update(self, instance, validated_data):
    #     # بروزرسانی فیلدهای داده‌شده
    #     instance.first_name = validated_data.get('first_name', instance.first_name)
    #     instance.last_name = validated_data.get('last_name', instance.last_name)
    #     instance.phone = validated_data.get('phone', instance.phone)
    #     instance.email = validated_data.get('email', instance.email)
    #     instance.address = validated_data.get('address', instance.address)
    #     # ذخیره تغییرات
    #     instance.save()
    #     return instance


# class VerifyPhoneSerializer(serializers.Serializer):
#     phone = serializers.CharField(max_length=15)
#
#     def validate_phone_number(self, value):
#         if not value.startswith('09') and not value.isdigit():
#             raise serializers.ValidationError("شماره تلفن باید معتبر باشد و با پیشوند مناسب شروع شود!")
#         return value


    # def validate_unique_phone_number(self, value):
    #     if UserShop.objects.filter(phone=value).exists():
    #         return serializers.ValidationError('شماره تلفن تکراری است!')


class VerifyCodeSerializer(serializers.Serializer):
    code = serializers.CharField()

    def validate_code(self, value):
        # اعتبارسنجی کد (مثلاً فقط عدد باشد)
        if not value.isdigit():
            raise serializers.ValidationError("کد تأیید باید فقط شامل اعداد باشد.")
        return value


# class UserRegisterSerializer(serializers.ModelSerializer):
#     first_name = serializers.CharField()
#     last_name = serializers.CharField()
#     email = serializers.EmailField()
#     address = serializers.CharField()
#     password = serializers.CharField(write_only=True)
#     # class Meta:
#     #     model = UserShop
#     #     fields = ['first_name', 'last_name', 'phone', 'email', 'address']
#
#     def create(self, validated_data):
#         user = UserShop(first_name=validated_data['first_name'], last_name=validated_data['last_name'], phone=validated_data['phone'],
#                         email=validated_data['email'], address=validated_data['address'])
#         user.set_password(validated_data['password'])
#         user.save()
#         return user
#
#     def validate_email(self, value):
#         if not value.endswith('@example.com'):
#             raise serializers.ValidationError('Email must be from @Example.com')
#
#     def validated_data(self):
#         if not all(['first_name, last_name']):
#             raise serializers.ValidationError('This fields required')
#
#     def validate(self, password):
#         if not password or password < 8:
#             raise serializers.ValidationError('password is required or wrong!')

class UserCreateSerializer(serializers.Serializer):
    phone = serializers.CharField()
    password = serializers.CharField(write_only=True, style={'input_type': 'password'})

    def validate_password(self, password):
        if not password or len(password) < 8:
            raise serializers.ValidationError('پسورد درست نیست!')
        return password


class UserLoginSerializer(serializers.Serializer):
    phone = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        user = authenticate(phone=data['phone'], password=data['password'])
        print(user)
        if not user:
            raise serializers.ValidationError('تلفن یا رمز عبور نادرست است')
        return {'user': user}


class UserEditProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserShop
        fields = ['first_name', 'last_name','phone', 'email', 'address']

    def update(self, instance, validated_data):
        # بروزرسانی فیلدهای داده‌شده
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.phone = validated_data.get('phone', instance.phone)
        instance.email = validated_data.get('email', instance.email)
        instance.address = validated_data.get('address', instance.address)
        # ذخیره تغییرات
        instance.save()
        return instance



import json
from rest_framework.generics import get_object_or_404
from rest_framework.mixins import UpdateModelMixin, CreateModelMixin
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet, ModelViewSet
from rest_framework import status, generics
from rest_framework.views import APIView
from .kavesms.kavesms import send_sms_with_template
from rest_framework.generics import mixins
from .serializers import *
from .models import *
import random
from .permissions import Fulluser_isadmin, Fulluser_authentication
from django.core.cache import cache
from rest_framework.generics import ListAPIView, RetrieveAPIView, RetrieveUpdateAPIView
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate, logout
from rest_framework.pagination import PageNumberPagination
from rest_framework.parsers import MultiPartParser
from rest_framework.permissions import IsAuthenticated, IsAdminUser




# class VerifyPhoneView(APIView):
#     def post(self, request):
#         phone_serializer = VerifyPhoneSerializer(data=request.data)
#         if phone_serializer.is_valid():
#             phone_number = phone_serializer.validated_data['phone_number']
#             # تولید کد تأیید تصادفی
#             token = ''.join(random.choices('0123456789', k=5))
#             # ارسال پیامک (پیاده‌ سازی متد send_sms_with_template)
#             send_sms_with_template(phone_number, {'token': token}, 'verify2')
#             return Response({'message': 'کد تأیید ارسال شد'}, status=status.HTTP_200_OK)
#         else:
#             return Response({'message': 'شماره تلفن درست نیست یا وجود ندارد!'})



# @method_decorator(csrf_exempt, name='dispatch')
# class VerifyPhoneView(APIView):
#     def post(self, request):
#         phone_serializer = VerifyPhoneSerializer(data=request.data)
#         if phone_serializer.is_valid():
#             phone_number = phone_serializer.validated_data['phone_number']
#             # تولید کد تأیید تصادفی
#             token = ''.join(random.choices('0123456789', k=5))
#
#             # ذخیره کد تأیید و شماره تلفن در Redis
#             cache.set(f'verification_code:{phone_number}', token, timeout=120)  # اعتبار 5 دقیقه‌ای
#
#             # ارسال پیامک (پیاده‌سازی متد send_sms_with_template)
#             send_sms_with_template(phone_number, {'token': token}, 'verify2')
#
#             return Response({'message': 'کد تأیید ارسال شد'}, status=status.HTTP_200_OK)
#         else:
#             return Response({'message': 'شماره تلفن درست نیست یا وجود ندارد!'}, status=status.HTTP_400_BAD_REQUEST)



# class VerifyPhoneView(APIView):
#     def post(self, request):
#         print(request)
#         phone = VerifyPhoneSerializer(data=request.data)
#         print(phone)
#         if phone.is_valid():
#             phone = phone.validated_data['phone']
#             print(phone)
#             # تولید کد تأیید تصادفی
#             token = ''.join(random.choices('0123456789', k=5))
#             print(token)
#             # ذخیره کد تأیید و شماره تلفن در Redis
#             cache.set(f'verification_code:{phone}', token, timeout=3600)
#             if not cache.get(f'verification_code:{phone}', token):
#                 return Response({'message': 'خطا در ذخیره کد تأیید!'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
#             # request.session['sessionID'] = phone_number
#             # request.session.save()
#             try:
#                 send_sms_with_template(phone, {'token': token}, 'marketshop')
#             except Exception as e:
#                 print(e)
#                 return Response({'message': 'خطا در ارسال پیامک!'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
#             return Response({'message': 'کد تأیید ارسال شد'}, status=status.HTTP_200_OK)
#         elif not phone.is_valid():
#             print(phone.errors)
#         return Response({'message': 'شماره تلفن درست نیست یا وجود ندارد!'}, status=status.HTTP_400_BAD_REQUEST)

class UserCreateView(generics.GenericAPIView, CreateModelMixin):
    serializer_class = UserCreateSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            return Response({'message': 'شماره تلفن درست نیست یا وجود ندارد!', 'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        phone = serializer.validated_data['phone']
        password = serializer.validated_data['password']
        if UserShop.objects.filter(phone=phone).exists():
            return Response({'error': 'این شماره تلفن قبلا ثبت شده است!'})
        # تولید کد تأیید تصادفی
        token = ''.join(random.choices('0123456789', k=5))
        request.session['verification_data'] = {'phone': phone, 'code': token, 'password': password}
        print(request.session['verification_data'])
        request.session.set_expiry(4000)  # تنظیم زمان انقضا (60 دقیقه)
        # ذخیره کد تأیید در Redis
        # cache.set(f'verification_code:{phone}', {'phone': phone, 'code': token, 'password': password}, timeout=3600)
        # cache.set(f'phone:{phone}', timeout=3600)
        # if not cache.get(f'verification_code:{phone}'):
        #     return Response({'message': 'خطا در ذخیره کد تأیید!'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        # ارسال پیامک
        try:
            send_sms_with_template(phone, {'token': token}, 'marketshop')
        except Exception as e:
            print(e)
            # del request.session['verification_data']  # حذف اطلاعات در صورت خطا
            return Response({'message': 'خطا در ارسال پیامک!'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response({'message': 'کد تأیید ارسال شد'}, status=status.HTTP_200_OK)


# class VerifyCodeView(APIView):
#     def post(self, request):
#         serializer = VerifyCodeSerializer(data=request.data)
#         if not serializer.is_valid():
#             return Response(
#                 {'status': 'error','message': 'Invalid data', 'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
#         phone = serializer.validated_data['phone']
#         code = serializer.validated_data['code']
#         # دریافت کد از کش
#         verification_code = cache.get(f'verification_code:{phone}')
#         if not verification_code:
#             return Response(
#                 {'status': 'error', 'message': 'کد تأیید منقضی شده یا وجود ندارد'}, status=status.HTTP_400_BAD_REQUEST)
#         if str(code) != str(verification_code):
#             return Response(
#                 {'status': 'error', 'message': 'کد وارد شده اشتباه است'}, status=status.HTTP_400_BAD_REQUEST)
#         # حذف کد استفاده شده از کش
#         cache.delete(f'verification_code:{code}')
#         # user = UserShop.objects.create_user(phone=phone)
#         # user.save()
#         # print(user)
#         # ذخیره وضعیت تأیید در کش برای استفاده بعدی
#         cache.set(f'verify_phone:{phone}', True, timeout=3600)
#         print(cache.get(f'verify_phone{phone}'))
#         return Response(
#             {
#                 'status': 'success',
#                 'message': 'تأیید شماره با موفقیت انجام شد',
#                 'phone': phone}, status=status.HTTP_200_OK)


class VerifyCodeView(generics.GenericAPIView, CreateModelMixin):
    serializer_class = VerifyCodeSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            code = serializer.validated_data.get('code')
            print("کد وارد شده:", code)
            # phone = cache.get('phone')
            # phone = request.session.get('phone')
            user_data = request.session.get('verification_data')
            print(user_data)
            if not user_data:
                return Response({'error': 'کد تأیید منقضی شده یا یافت نشد!'}, status=status.HTTP_400_BAD_REQUEST)
            verify_code = user_data.get('code')
            print(verify_code)
            phone = user_data.get('phone')
            print(phone)
            password = user_data.get('password')
            print(password)
            if not phone:
                return Response({'error': 'شماره تلفن یافت نشد!'}, status=status.HTTP_400_BAD_REQUEST)
            # verify_code = cache.get(verification_code:{phone}')
            # if not verify_code or str(code) != str(verify_code):
            #     return Response({'error': 'کد وارد شده اشتباه است'}, status=status.HTTP_400_BAD_REQUEST)
            if verify_code is None or str(code) != str(verify_code):
                return Response({'error': 'کد وارد شده اشتباه است!'}, status=status.HTTP_400_BAD_REQUEST)
            user = UserShop.objects.create_user(phone=phone)
            user.set_password(password)
            user.save()
            # ذخیره وضعیت تأیید شماره تلفن در cache
            # cache.set(f'verify_phone:{phone}', True, timeout=3600)
            # حذف کد تأیید پس از اعتبارسنجی
            del request.session['verification_data']
            return Response({'success': 'user successfully created', 'phone': phone}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



# class UserCreateView(APIView):
#     serializer_class = UserSerializer
#
#     def post(self, request):
#         serializer = UserCreateSerializer(data=request.data)
#         print(serializer)
#         if not serializer.is_valid():
#             return Response({'error': 'phone or password Invalid'}, status=status.HTTP_400_BAD_REQUEST)
#         phone = serializer.validated_data['phone']
#         print(phone)
#         password = serializer.validated_data['password']
#         print(password)
#         verify_phone = cache.get(f'verify_phone:{phone}')
#         if not verify_phone:
#             return Response({'error': 'phone not found!'})
#         else:
#             user = UserShop.objects.create_user(phone=phone)
#             user.set_password(password)
#             user.save()
#             print(user)
#         cache.delete(f'verify_phone{phone}')
#         return Response({'success': 'user successfully created'})



class LoginUserView(APIView):
    serializer_class = UserLoginSerializer

    def post(self, request):
        phone = request.data.get('phone')
        password = request.data.get('password')
        user_serializer = UserLoginSerializer(data=request.data)
        print(request.data)
        if not user_serializer.is_valid():
            return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        user = authenticate(phone=phone, password=password)
        if user:
            refresh_token = RefreshToken.for_user(user)
            return Response({
                'refresh': str(refresh_token),
                'access': str(refresh_token.access_token),
            }, status=status.HTTP_200_OK)
        return Response({'error': 'user not found'}, status=status.HTTP_400_BAD_REQUEST)


# class LoginUserView(generics.GenericAPIView, CreateModelMixin):
#     serializer_class = UserLoginSerializer
#
#     def post(self, request, *args, **kwargs):
#         serializer = self.get_serializer(data=request.data)
#         if not serializer.is_valid():
#             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#         phone = serializer.validated_data.get('phone')
#         password = serializer.validated_data.get('password')
#         user = authenticate(request, phone=phone, password=password)
#         if user:
#             refresh_token = RefreshToken.for_user(user)
#             return Response({
#                 'refresh': str(refresh_token),
#                 'access': str(refresh_token.access_token),
#             }, status=status.HTTP_200_OK)
#         return Response({'error': 'user not found'}, status=status.HTTP_400_BAD_REQUEST)




class ProfileView(APIView):
    permission_classes = [Fulluser_isadmin, Fulluser_authentication]
    parser_classes = [MultiPartParser]

    def get(self, request):
        if request.user.is_authenticated:
            phone = [user.phone for user in UserShop.objects.all()]
            print(phone)
            return Response(phone)
        return Response({'error': 'user not authentication'})


# class EditUserView(APIView):
#     def get(self, request):
#         context = {
#             'phone': request.query_params.get('phone'),
#             'first_name': request.query_params.get('first_name'),
#             'last_name': request.query_params.get('last_name'),
#             'email': request.query_params.get('email'),
#             'address': request.query_params.get('address'),
#             'password': request.query_params.get('password'),
#         }
#         return Response(context)
#
#     def put(self, request):
#         phone = request.data.get('phone')
#         try:
#             # پیدا کردن کاربر براساس شماره تلفن
#             user = UserShop.objects.get(phone=phone)
#             # به‌روزرسانی اطلاعات کاربر
#             first_name = request.data.get('first_name')
#             last_name = request.data.get('last_name')
#             email = request.data.get('email')
#             address = request.data.get('address')
#             password = request.data.get('password')
#             if first_name:
#                 user.first_name = first_name
#             if last_name:
#                 user.last_name = last_name
#             if email:
#                 user.email = email
#             if address:
#                 user.profile.address = address  # فرض کنیم فیلد آدرس در پروفایل وجود دارد
#             if password:
#                 user.set_password(password)  # تغییر رمز عبور و رمزگذاری آن
#             user.save()  # ذخیره تغییرات
#             return Response({'success': 'اطلاعات کاربر با موفقیت به‌روزرسانی شد!'}, status=status.HTTP_200_OK)
#         except:
#             return Response({'error': 'کاربری با این شماره تلفن پیدا نشد!'}, status=status.HTTP_404_NOT_FOUND)


# class EditUserView(APIView):
#     def get(self, request, id):
#         user = get_object_or_404(UserShop, id=id)
#         serializer = UserEditProfileSerializer(user)
#         return Response(serializer.data)
#     def put(self, request, id):
#         user = get_object_or_404(UserShop, id=id)
#         print(user)
#         serializer = UserEditProfileSerializer(user, data=request.data)
#         print(serializer)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_200_OK)
#         if not serializer.is_valid():
#             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#         return Response({'error': 'invalid information'}, status=status.HTTP_400_BAD_REQUEST)



class EditUserView(generics.GenericAPIView, UpdateModelMixin):
    serializer_class = UserSerializer

    def put(self, request, pk=None, *args, **kwargs):
        instance = UserShop.objects.get(id=pk)
        phone = instance.phone
        print(phone)
        serializer = UserSerializer(instance=instance, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'success': 'success', 'phone': phone}, status=status.HTTP_200_OK)
        return Response(request, phone, *args, **kwargs)



class UserListView(ListAPIView):
    permission_classes = [IsAdminUser]
    pagination_class = PageNumberPagination
    queryset = UserShop.objects.all()
    serializer_class = UserSerializer



class UserDetailView(RetrieveAPIView):
    permission_classes = [IsAdminUser]
    queryset = UserShop.objects.all()
    serializer_class = UserSerializer




class LogoutApiView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            logout(request)
            return Response(
                {"message": "شما با موفقیت از سیستم خارج شدید."},
                status=status.HTTP_200_OK
            )
        except Exception as e:
            # در صورت بروز هرگونه خطا در فرآیند خروج
            print(f"Error during logout: {e}")
            return Response(
                {"message": "خطا در فرآیند خروج از سیستم. لطفا دوباره تلاش کنید."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )



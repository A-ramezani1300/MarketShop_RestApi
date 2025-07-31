from django.contrib.auth.backends import ModelBackend
from account.models import UserShop

class PhoneAuthenticationBackend(ModelBackend):
    def authenticate(self, request, phone=None, password=None, **kwargs):
        try:
            user = UserShop.objects.get(phone=phone)
            if user.check_password(password):
                return user
        except UserShop.DoesNotExist:
            return None
        return None

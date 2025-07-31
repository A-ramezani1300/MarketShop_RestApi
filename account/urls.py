from django.urls import path
from . import views
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

app_name = 'account'


urlpatterns = [
    # path('verify_phone/', views.VerifyPhoneView.as_view(), name='verify_phone'),
    path('verify_code/', views.VerifyCodeView.as_view(), name='verify_code'),
    path('user_create/', views.UserCreateView.as_view(), name='user_create'),
    path('profile/', views.ProfileView.as_view(), name='profile'),
    path('userlist/', views.UserListView.as_view(), name='userlist'),
    path('user_detail/<int:pk>/', views.UserDetailView.as_view(), name='user_detail'),
    # path('register/', views.UserRegisterApiView.as_view(), name='register'),
    path('edit_user/<int:pk>/', views.EditUserView.as_view(), name='edit_user'),
    path('login/', views.LoginUserView.as_view(), name='login'),
    path('logout/', views.LogoutApiView.as_view(), name='logout'),
    # path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]


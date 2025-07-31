"""
URL configuration for MarketShop_RestApi project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from rest_framework.schemas import get_schema_view

# urlpatterns = [
#     path('schema/', get_schema_view(title="My API Schema"), name="api-schema"),
# ]


urlpatterns = [
    path('admin/', admin.site.urls),
    path('schema/', SpectacularAPIView.as_view(), name='schema'),
    path('schema/', get_schema_view(title="My API Schema"), name="api-schema"),
    path('swagger/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger_ui'),
    path('api/account/', include('account.urls', namespace='account')),
    path('api/shop/', include('shop.urls', namespace='shop')),
    path('api/cart/', include('cart.urls', namespace='cart')),
    path('api/orders/', include('orders.urls', namespace='orders')),
]


urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
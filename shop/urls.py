from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter

# router = DefaultRouter()
# router.register(r'comments', views.CommentApiView, basename='comment')
# # urlpatterns1 = router.urls
# urlpatterns1 = [
#     path('', include(router.urls)),
# ]

app_name = 'shop'

urlpatterns = [
    path('category_list/', views.CategoryApiView.as_view(), name='category_list'),
    path('category_detail/', views.CategoryApiView.as_view(), name='category_detail'),
    path('product_list/', views.ProductApiView.as_view(), name='product_list'),
    path('product_detail/<int:pk>/', views.ProductApiView.as_view(), name='product_detail'),
    path('filter/', views.ProductFilterView.as_view(), name='product_filter'),
    path('search/', views.SearchApiView.as_view(), name='search'),
    path('comment/<int:pk>/', views.CommentApiView.as_view(), name='comment'),
    path('comment_list/', views.CommentApiView.as_view(), name='comment_list'),
    path('ticket/', views.TicketApiView.as_view(), name='ticket'),
    path('ticket_list/', views.TicketApiView.as_view(), name='ticket_list'),
    path('ticket_detail/<int:pk>/', views.TicketApiView.as_view(), name='ticket_detail'),
]

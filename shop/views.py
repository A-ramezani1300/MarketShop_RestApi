from rest_framework import generics, status
from rest_framework.decorators import permission_classes
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView, RetrieveAPIView, get_object_or_404
from .models import *
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from .serializers import *
from account.permissions import Fulluser_authentication, Fulluser_isadmin
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin, CreateModelMixin
from rest_framework.pagination import PageNumberPagination, LimitOffsetPagination
from rest_framework import viewsets
from .tasks import all_bucket_object_tasks
from rest_framework.filters import SearchFilter
from django_filters.rest_framework import DjangoFilterBackend



class CategoryApiView(generics.GenericAPIView, ListModelMixin, RetrieveModelMixin):
    permission_classes = [IsAdminUser, IsAuthenticated]
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    pagination_class = PageNumberPagination
    def get(self, request, *args, **kwargs):
        if 'pk' in kwargs:
            return self.retrieve(request, *args, **kwargs)
        else:
            return self.list(request, *args, **kwargs)


class ProductApiView(generics.GenericAPIView, ListModelMixin, RetrieveModelMixin):
    permission_classes = [IsAdminUser, IsAuthenticated]
    queryset = Product.objects.all()
    serializer_class = CategorySerializer
    pagination_class = PageNumberPagination

    def get(self, request, *args, **kwargs):
        if 'pk' in kwargs:
            return self.retrieve(request, *args, **kwargs)
        else:
            return self.list(request, *args, **kwargs)



class CommentApiView(generics.GenericAPIView, CreateModelMixin, ListModelMixin, RetrieveModelMixin):
    permission_classes = [IsAdminUser, IsAuthenticated]
    serializer_class = CommentSerializer
    queryset = Comment.objects.all()
    pagination_class = PageNumberPagination

    def get(self, request, *args, **kwargs):
        if 'pk' in kwargs:
            return self.retrieve(request, *args, **kwargs)
        else:
            return self.list(request, *args, **kwargs)


    def post(self, request, *args, **kwargs):
        serializer = CommentSerializer(data=request.data)
        product_id = kwargs.get('pk')
        product = get_object_or_404(Product, id=product_id)
        if serializer.is_valid():
            serializer.validated_data['name'] = request.user
            serializer.save(user=request.user, product=product)
            return Response({'success': 'comment with successfully created'}, status=status.HTTP_201_CREATED)
        return Response({'error': 'Invalid comment'}, status=status.HTTP_400_BAD_REQUEST)


    # def list(self, request, *args, **kwargs):
    #     comment = Comment.objects.all()
    #     serializer = self.serializer_class(comment, many=True)
    #     return Response(serializer.data, status=status.HTTP_200_OK)



class TicketApiView(generics.GenericAPIView, CreateModelMixin, ListModelMixin, RetrieveModelMixin):
    permission_classes = [IsAdminUser, IsAuthenticated]
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer
    pagination_class = PageNumberPagination

    def get(self, request, *args, **kwargs):
        if 'pk' in kwargs:
            return self.retrieve(request, *args, **kwargs)
        else:
            return self.list(request, *args, **kwargs)

    def post(self, request):
        serializer = TicketSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response({'success': 'Ticket with successfully created'}, status=status.HTTP_201_CREATED)
        return Response({'error': 'Invalid Ticket'}, status=status.HTTP_400_BAD_REQUEST)





class SearchApiView(ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [SearchFilter]
    search_fields = ['name', 'description']



class ProductFilterView(generics.GenericAPIView, RetrieveModelMixin):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend]  # فعال‌سازی فیلتر
    filterset_class = ProductFilter  # اتصال کلاس فیلتر

    def retrieve(self, request, *args, **kwargs):
        if 'pk' in request:
            return self.retrieve(request, *args, **kwargs)
        return Response({'error': 'Invalid Request'}, status=status.HTTP_400_BAD_REQUEST)




class BucketHome(APIView):
    def get(self, request):
        bucket_object = all_bucket_object_tasks()
        return Response(bucket_object)





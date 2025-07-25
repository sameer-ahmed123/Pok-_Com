from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from rest_framework import status
from rest_framework.decorators import api_view
from products.serializers import ProductListSerializer, ProductDetailSerializer
from products.models import Product
# Create your views here.


@api_view(['GET'])
def products_list_view(request):
    paginator = PageNumberPagination()
    products = Product.objects.only(
        'id',
        'pokemon_id',
        'name',
        'image_url',
        'description',
        'price',
        'is_active'
    ).all()
    paginated_products = paginator.paginate_queryset(products, request)
    product_serializer = ProductListSerializer(paginated_products, many=True)
    return paginator.get_paginated_response(product_serializer.data)


@api_view(['GET'])
def product_detail_view(request, id):
    product = get_object_or_404(Product, id=id)
    serializer = ProductDetailSerializer(product)
    data = serializer.data
    return Response(data, status.HTTP_200_OK)

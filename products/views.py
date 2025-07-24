from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from rest_framework import status
from rest_framework.decorators import api_view
from products.serializers import ProductSerializer
from products.models import Product
# Create your views here.


@api_view(['GET'])
def products_list_view(request):
    paginator = PageNumberPagination()
    if request.method == "GET":
        products = Product.objects.all()
        paginated_products = paginator.paginate_queryset(products, request)
        product_serializer = ProductSerializer(paginated_products, many=True)
        return paginator.get_paginated_response(product_serializer.data)

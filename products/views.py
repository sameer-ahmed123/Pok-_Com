from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
# Create your views here.


@api_view(['GET'])
def products_list_view(request):
    if request.method == "GET":
        data = {"page": "products_page"}
        return Response(data, status=status.HTTP_200_OK)

from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
# Create your views here.


@api_view(["GET"])
def cart_test(request):
    data = {"message": "CART_TEST"}
    return Response(data, status.HTTP_200_OK)

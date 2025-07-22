from django.urls import path
from cart.views import *

app_name = "cart"
urlpatterns = [
    path("", cart_test,name="test")
]


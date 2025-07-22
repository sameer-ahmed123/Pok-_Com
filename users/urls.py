from django.urls import path
from users.views import *


app_name = "users"
urlpatterns = [
    path("", users_test, name="test")
]

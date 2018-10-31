from django.shortcuts import render
from django.contrib.auth import views
# Create your views here.

from rest_framework.authtoken.models import Token


class SimpleUserLogin(views.LoginView):
    pass


class SimpleUserLogout(views.LogoutView):
    pass
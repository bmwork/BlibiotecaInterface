from unicodedata import name
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.contrib.auth.decorators import login_required
from . import views

urlpatterns = [
    path('', views.loginUser, name="login"),
    path('register', views.registerUser, name="register"),
    path('logout', views.logoutUser, name="logout"),
    path('inventory', views.inventoryPage, name="inventory"),
    path('inventory/read/<str:slug>', views.readPage, name="read"),
    path('inventory/rate/<str:slug>', views.ratePage, name="rate"),
]

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from . import views

urlpatterns = [
    path('', views.loginUser, name="login"),
    path('register', views.registerUser, name="register"),
    path('logout', views.logoutUser, name="logout"),
    path('account', views.accountPage, name="account"),
    path('inventory', views.inventoryPage, name="inventory"),
    path('wishlist', views.wishlist, name="wishlist"),
    path('inventory/read/<str:slug>', views.readPage, name="read"),
]

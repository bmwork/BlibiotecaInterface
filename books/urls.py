from unicodedata import name
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.contrib.auth.decorators import login_required
from . import views

urlpatterns = [
    # Book
    path('', views.browsePage.as_view(), name="browse"),
    path('visualize/<str:slug>', views.visualizeBookPage, name="visualize"),
    path('buy/<str:slug>', views.buyBookPage, name="buy"),

    # Admin
    path('adm/browse', views.browseAdminPage.as_view(), name="browseAdmin"),
    path('adm/browse/add', views.bookAddPage, name="add"),
    path('adm/browse/edit/<str:slug>', views.bookEditPage, name="edit"),
    path('adm/browse/del/<str:slug>', views.bookDelPage, name="delete"),
    
    # path('adm/browse/add', views.browseAdminPage, name="browseAdmin"),
    # path('adm/browse/edit', views.browseAdminPage, name="browseAdmin"),

]

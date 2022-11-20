from unicodedata import name
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.contrib.auth.decorators import login_required
from . import views

urlpatterns = [
    # Book
    path('browse', views.browsePage.as_view(), name="browse"),
    path('books/<str:slug>', views.visualizeBookPage, name="visualize"),
    path('borrow/<str:slug>', views.borrowBook, name="borrow"),
    path('favorite/<str:slug>', views.favoriteBookPage, name="favorite"),
    path('remove/<str:slug>', views.remove_from_favorite_book_page, name="remove"),

    # Admin
    path('adm/browse', views.browseAdminPage.as_view(), name="adminBrowse"),
    path('adm/browse/add', views.bookAddPage, name="adminAdd"),
    path('adm/browse/edit/<str:slug>', views.bookEditPage, name="adminEdit"),
    path('adm/browse/del/<str:slug>', views.bookDelPage, name="adminDelete"),

    # path('adm/browse/add', views.browseAdminPage, name="browseAdmin"),
    # path('adm/browse/edit', views.browseAdminPage, name="browseAdmin"),

]

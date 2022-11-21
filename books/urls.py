from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from . import views

urlpatterns = [
    # Book
    path('browse', views.browsePage.as_view(), name="browse"),
    path('result', views.searchBook, name="search"),
    path('books/<str:slug>', views.visualizeBookPage, name="visualize"),
    path('borrow/<str:slug>', views.borrowBook, name="borrow"),
    path('favorite/<str:slug>', views.favoriteBookPage, name="favorite"),
    path('remove/<str:slug>', views.remove_from_favorite_book_page, name="remove"),
    path('pdf/<str:slug>', views.viewPDF, name="pdf"),
    path('mp3/<str:slug>', views.viewMP3, name="mp3"),

    # Admin
    path('adm/browse', views.browseAdminPage.as_view(), name="adminBrowse"),
    path('adm/browse/add', views.bookAddPage, name="adminAdd"),
    path('adm/browse/edit/<str:slug>', views.bookEditPage, name="adminEdit"),
    path('adm/browse/del/<str:slug>', views.bookDelPage, name="adminDelete"),
]

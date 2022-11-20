from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView
from django.contrib import messages
from .models import Book
from .functions import get_by_uuid
import json
from django.apps import apps
from users.models import Customer
from books.models import Review
from django.http import HttpResponse


class browsePage(ListView):
    model = Book
    template_name = 'books/browse.html'
    context_object_name = 'books'


class browseAdminPage(ListView):
    model = Book
    template_name = 'admin/Adminbrowse.html'
    context_object_name = 'books'


def visualizeBookPage(request, slug):
    book = Book.objects.get(uuid=slug)
    ctx = {'book': book}

    if request.method == "POST":
        name = request.user.username
        comment = request.POST.get('comment')

        if comment:
            review = Review.objects.create(
                book=book, name=name, body=comment)
            review.save()

    return render(request, 'books/visualize.html', ctx)


def borrowBook(request, slug):
    if request.user.is_authenticated:
        book = Book.objects.get(uuid=slug)
        request.user.inventory.add(book)
        request.user.save()
        return redirect('inventory')

    return redirect('visualize', slug)


def remove_from_favorite_book_page(request, slug):

    # Get the user.
    user = request.user

    # Get the user class obj.
    obj = Customer.objects.get(username=user.username)
    print(obj.wishlist)
    # Transform wishlist str to list and save into decoded_whishlist.
    decoded_whishlist = eval(obj.wishlist)
    print(decoded_whishlist)
    # If the book id to remove is in the list "favorite books", remove the book id from the list and save the new list.
    if slug in decoded_whishlist:
        i = decoded_whishlist.index(slug)
        decoded_whishlist = decoded_whishlist.pop(i)
    else:
        pass

    # Convert the list to json (str) and save into var load_wishlist.
    load_wishlist = json.dumps(decoded_whishlist)

    # Rewrite the new load_wishlist str into user wishlist database field.
    obj.wishlist = load_wishlist

    # Save the changes.
    obj.save()
    return redirect("inventory")


def favoriteBookPage(request, slug):

    # Get the user.
    user = request.user

    # Get the user class obj.
    obj = Customer.objects.get(username=user.username)

    # Transform wishlist str to list and save into decoded_whishlist.
    decoded_whishlist = eval(obj.wishlist)

    # Append the slug to decoded_whishlist.
    decoded_whishlist.append(slug)

    # Convert the list to json (str) and save into var load_wishlist.
    load_wishlist = json.dumps(decoded_whishlist)

    # Rewrite the new load_wishlist str into user wishlist database field.
    obj.wishlist = load_wishlist

    # Save the changes.
    obj.save()
    return redirect("inventory")


def bookEditPage(request, slug):
    book = Book.objects.get(uuid=slug)
    ctx = {'book': book}

    if request.method == "POST":
        title = request.POST.get('title')
        author = request.POST.get('author')
        date_published = request.POST.get('date_published')
        publisher = request.POST.get('publisher')
        language = request.POST.get('language')
        description = request.POST.get('description')
        content = request.POST.get('content')

        if request.FILES:
            cover = request.FILES['cover']
            book.cover = cover

        book.title = title
        book.author = author
        book.date_published = date_published
        book.publisher = publisher
        book.language = language
        book.description = description
        book.content = content
        book.save()
        return redirect('adminEdit', slug)

    return render(request, 'admin/adminEdit.html', ctx)


def bookDelPage(request, slug):
    book = Book.objects.get(uuid=slug)
    book.delete()
    return redirect('adminBrowse')


def bookAddPage(request):
    if request.method == "POST":
        title = request.POST.get('title')
        author = request.POST.get('author')
        date_published = request.POST.get('date_published')
        publisher = request.POST.get('publisher')
        language = request.POST.get('language')
        description = request.POST.get('description')
        content = request.POST.get('content')

        if request.FILES:
            cover = request.FILES['cover']
            book = Book.objects.create(cover=cover, title=title, author=author, date_published=date_published,
                                       publisher=publisher, language=language, description=description, content=content)
            book.save()
            return redirect('adminBrowse')

        else:
            return redirect('adminAdd')

    return render(request, 'admin/adminAdd.html')

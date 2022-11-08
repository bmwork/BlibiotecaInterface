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
class browsePage(ListView):
    model = Book
    template_name = 'books/browse.html'
    context_object_name = 'books'

class browseAdminPage(ListView):
    model = Book
    template_name = 'admin/browseAdmin.html'
    context_object_name = 'books'


def visualizeBookPage(request, slug):
    books_query = Book.objects.all()
    book = get_by_uuid(books_query, slug)

    ctx = {
        'book_cover': book.cover.url,
        'book_title': book.title,
        'book_desc': book.description,
        'book_qnt': book.quantity,
        'book_uuid': book.uuid,
    }

    return render(request, 'books/visualize.html', ctx)

def buyBookPage(request, slug):
    books_query = Book.objects.all()
    book = get_by_uuid(books_query, slug)

    request.user.inventory.add(book)
    request.user.save()
    
    return redirect('browse')

def remove_from_favorite_book_page(request, slug):

    # Get the user.
    user = request.user

    # Get the user class obj.
    obj = Customer.objects.get(username = user.username)
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
    obj = Customer.objects.get(username = user.username)
    
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
    books_query = Book.objects.all()
    book = get_by_uuid(books_query, slug)

    

    ctx = {
        'book_cover': book.cover.url,
        'book_title': book.title,
        'book_desc': book.description,
        'book_cont': book.content,
        'book_qnt': book.quantity,
        'book_uuid': book.uuid,
    }

    if request.method == "POST":
        title = request.POST.get('title')
        desc = request.POST.get('desc')
        cont = request.POST.get('cont')
        qnt = request.POST.get('qnt')
        
        book.title = title
        book.description = desc
        book.content = cont
        book.quantity = qnt
        book.save()
        return redirect('browseAdmin')

    return render(request, 'admin/edit.html', ctx)

def bookDelPage(request, slug):
    books_query = Book.objects.all()
    book = get_by_uuid(books_query, slug)
    book.delete()
    return redirect('browseAdmin')

def bookAddPage(request):

    if request.method == "POST":
        title = request.POST.get('title')
        desc = request.POST.get('desc')
        cont = request.POST.get('cont')

        book = Book.objects.create(title=title, description=desc, content=cont)
        book.save()
        return redirect('browseAdmin')
    return render(request, 'admin/add.html')


    

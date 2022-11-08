from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView
from django.contrib import messages
from .models import Book
from .functions import get_by_uuid

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
        cover = request.FILES['cover']
        desc = request.POST.get('desc')
        cont = request.POST.get('cont')
        qnt = request.POST.get('qnt')
        
        book.title = title
        book.cover = cover
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
        if request.FILES:
            cover = request.FILES['cover']
            book = Book.objects.create(title=title, description=desc, content=cont, cover=cover)
            book.save()
            return redirect('browseAdmin')
        else:
            book = Book.objects.create(title=title, description=desc, content=cont)
            book.save()
        return redirect('browseAdmin')
    return render(request, 'admin/add.html')


    

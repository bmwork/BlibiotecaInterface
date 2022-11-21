from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.views.generic import ListView
from .models import Book
import json
from users.models import Customer
from books.models import Review
from django.http import HttpResponse


class browsePage(ListView):
    model = Book
    template_name = 'books/browse.html'
    paginate_by = 10
    context_object_name = 'books'


class browseAdminPage(ListView):
    model = Book
    template_name = 'admin/Adminbrowse.html'
    paginate_by = 10
    context_object_name = 'books'


def searchBook(request):
    if request.method == "GET":
        search = request.GET.get('search')
        results = Book.objects.all().filter(title=search)
        ctx = {'results': results}

        return render(request, 'books/search.html', ctx)


def viewPDF(request, slug):
    book = Book.objects.get(uuid=slug)

    response = HttpResponse(book.pdf_file, content_type="application/pdf")
    return response


def viewMP3(request, slug):
    book = Book.objects.get(uuid=slug)

    response = HttpResponse(book.mp3_file, content_type="audio/mpeg")
    return response


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

        cover = request.FILES.get('cover')
        pdf = request.FILES.get('pdf')
        mp3 = request.FILES.get('mp3')

        if not cover or not pdf or not mp3:
            return redirect('adminEdit', slug)

        book.cover = cover
        book.pdf_file = pdf
        book.mp3_file = mp3

        book.title = title
        book.author = author
        book.date_published = date_published
        book.publisher = publisher
        book.language = language
        book.description = description
        book.content = content
        book.save()
        return redirect('adminBrowse')

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

        cover = request.FILES.get('cover')
        pdf = request.FILES.get('pdf')
        mp3 = request.FILES.get('mp3')

        if not cover or not pdf or not mp3:
            return redirect('adminAdd')

        amount = request.POST.get('amount')
        if amount:
            for x in range(int(amount)):
                book = Book.objects.create(cover=cover, title=title, author=author, date_published=date_published,
                                           publisher=publisher, language=language, description=description, content=content, pdf_file=pdf, mp3_file=mp3)
                book.save()
            return redirect('adminBrowse')

        book = Book.objects.create(cover=cover, title=title, author=author, date_published=date_published,
                                   publisher=publisher, language=language, description=description, content=content, pdf_file=pdf, mp3_file=mp3)
        book.save()
        return redirect('adminBrowse')

    return render(request, 'admin/adminAdd.html')

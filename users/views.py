from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Customer
from books.functions import get_by_uuid
from books.models import Book


def loginUser(request):
    if request.user.is_authenticated:
        return redirect('browse')

    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')

        # Checks if the user email exists in the database
        # If not, handle exception by redirecting to the login page

        try:
            username = Customer.objects.get(email=email)
            print(username)
        except Customer.DoesNotExist:
            messages.warning(request, "Email not registered")
            return redirect('login')

        user = authenticate(request, username=username, password=password)

        # If the user authentication is succeded, login the user
        # If not redirect to login

        if user is not None:
            login(request, user)
            request.session["name"] = email
            return redirect('browse')

        else:
            messages.warning(request, "Password incorrect")
            return redirect('login')

    return render(request, 'auth/login.html')


def registerUser(request):

    if request.user.is_authenticated:
        return redirect('browse')

    if request.method == "POST":
        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        # Filters the username to be unique

        if Customer.objects.filter(username=username).exists():
            messages.warning(request, "Username already registered")
            return redirect('register')

        # Check if the passwords match

        if password1 != password2:
            messages.warning(request, "Passwords dont match")
            return redirect('register')

        # Filters the email in the database

        if Customer.objects.filter(email=email).exists():
            messages.warning(request, "Email already registered")
            return redirect('register')

        else:

            # Creating the user model to save in the database
            # Along with a profile

            user = Customer(username=username, email=email)
            user.set_password(password1)
            user.save()

            return redirect('login')

    return render(request, 'auth/register.html')


def logoutUser(request):
    logout(request)
    return redirect('login')


def inventoryPage(request):
    return render(request, 'users/inventory.html')


def wishlist(request):
    user_wl = request.user.wishlist
    user_wl = eval(user_wl)
    reg_books = Book.objects.all()
    wl_books = []

    for uuid in user_wl:
        casted_uuid = get_by_uuid(reg_books, uuid)
        wl_books.append(casted_uuid)

    ctx = {"wishlist": wl_books}
    print(wl_books, "AAAAAAAAAAAAAAAAAAAAAAAA")

    return render(request, 'users/wishlist.html', ctx)


def readPage(request, slug):
    owned_books_query = request.user.inventory.all()
    book = get_by_uuid(owned_books_query, slug)
    ctx = {'book': book}

    return render(request, 'users/read.html', ctx)


def accountPage(request):
    if request.method == "POST":
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        picture = request.FILES.get('picture')

        if not picture:
            return redirect('account')

        request.user.picture = picture
        request.user.username = username
        request.user.email = email
        request.user.set_password(password)
        request.user.save()

        logout(request)
        return redirect('login')

    return render(request, 'users/account.html')

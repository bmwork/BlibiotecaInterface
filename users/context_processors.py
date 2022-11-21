def load_books(request):
    if request.user.is_authenticated:
        books = request.user.inventory.all()
        wishlist = request.user.wishlist

        return {"owned_books": books,
                "wishlist": wishlist}

    return {"owned_books": []}

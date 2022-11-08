def load_books(request):
    if request.user.is_authenticated:
        books = request.user.inventory.all()
        picture = request.user.picture
        wishlist = request.user.wishlist

        return {"owned_books": books,
                "profile_pic": picture,
                "wishlist": wishlist}

    return {"owned_books": [],
            "profile_pic": ""}

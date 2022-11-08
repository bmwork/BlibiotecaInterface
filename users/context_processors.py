def load_books(request):
    if request.user.is_authenticated:
        books = request.user.inventory.all()
        picture = request.user.picture
        return { "owned_books": books,
                 "profile_pic": picture }
        
    return { "owned_books": [],
             "profile_pic": ""}


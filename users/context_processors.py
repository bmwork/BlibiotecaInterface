def load_books(request):
    if request.user.is_authenticated:
        books = request.user.inventory.all()
        return { "owned_books": books }
        
    return { "owned_books": []}


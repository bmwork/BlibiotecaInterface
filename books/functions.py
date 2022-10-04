from .models import Book

def get_by_uuid(query, uuid):
    for book in query:
        try:
            return Book.objects.get(uuid=uuid)
        except Book.DoesNotExist:
            pass
    return None
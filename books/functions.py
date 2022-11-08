from .models import Book
import uuid
def get_by_uuid(query, uuid):
    for book in query:
        try:
            return Book.objects.get(uuid=uuid)
        except Book.DoesNotExist:
            pass
    return None

def strToUUID(list):
    converted = []
    for value in list:
        converted.append(uuid.UUID(value).hex)
    return converted  
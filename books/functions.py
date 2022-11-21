from .models import Book
import uuid
from gtts import gTTS
import os


def bookTTS(textfield, language):
    audio = gTTS(text=textfield, lang=language, slow=False)
    return audio


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

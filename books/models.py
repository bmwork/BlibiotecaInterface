from email.policy import default
from django.db import models
import uuid

class Book (models.Model):
    cover = models.ImageField(default='default_book.ico', upload_to="bookcovers/", blank=True, null=True)
    title = models.CharField(max_length=30)
    description = models.CharField(max_length=100)
    content = models.CharField(max_length=10000) 
    uuid = models.UUIDField(default=uuid.uuid4, unique=True)
    quantity = models.IntegerField(default=5)


    def __str__(self) -> str:
        return self.title

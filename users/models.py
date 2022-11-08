from django.db import models
from django.contrib.auth.models import AbstractUser
from PIL import Image


class Customer (AbstractUser):
    inventory = models.ManyToManyField('books.Book')
    picture = models.ImageField(
        default='default_pic.ico', upload_to="profiles/")
    wishlist = models.TextField(
        max_length=1000, null=True, blank=True, default=[])

    def __str__(self) -> str:
        return self.username

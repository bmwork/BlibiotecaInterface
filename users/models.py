from django.db import models
from django.contrib.auth.models import AbstractUser

class Customer (AbstractUser):
    inventory = models.ManyToManyField('books.Book')

    def __str__(self) -> str:
        return self.username

from django.contrib import admin
from . import models

class BooksAdmin(admin.ModelAdmin):
    fieldsets = (
    ('Book Information', {
        'fields': ['cover', 'title', 'description', 'content', 'quantity', 'uuid']
    }),
)

admin.site.register(models.Book, BooksAdmin)
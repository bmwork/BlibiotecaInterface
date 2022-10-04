from django.contrib import admin
from . import models

class CustomerAdmin(admin.ModelAdmin):
    fieldsets = (
    ('User Information', {
        'fields': ['username', 'email', 'password']
    }),

    ('Inventory', {
        'fields': ['inventory']
    }),

    ('Other Infomartion', {
        'fields': ['date_joined', 'last_login'],
        'classes': ('collapse',)
    })
)

admin.site.register(models.Customer, CustomerAdmin)
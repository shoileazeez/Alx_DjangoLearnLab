from django.contrib import admin
from .models import Book

class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'published_date') # Display these fields in the admin list view
    list_filter = ('author', 'publication_year')  # Add filters for these fields
    search_fields = ('title', 'author') # Enable search capabilities for these fields

admin.site.register(Book, BookAdmin)
# Register your models here.

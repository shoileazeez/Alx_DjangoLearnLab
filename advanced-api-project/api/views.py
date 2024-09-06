from django.shortcuts import render
from django.views.generic import ListView
from django.views.generic import DetailView
from django.views.generic import CreateView
from django.views.generic import UpdateView
from django.views.generic import DeleteView
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from django.urls import reverse_lazy
from .models import Book
from django_filters import rest_framework
from rest_framework import generics

class BookListView(ListView):
    model = Book
    template_name = 'bookshelf/book_list.html'  # Define your template
    context_object_name = 'books'
    permission_classes = [IsAuthenticatedOrReadOnly]

class BookDetailView(DetailView):
    model = Book
    template_name = 'bookshelf/book_detail.html'  # Template for displaying a single book
    context_object_name = 'book'
    permission_classes = [IsAuthenticatedOrReadOnly]
    
class BookCreateView(CreateView):
    model = Book
    fields = ['title', 'author', 'publication_year']  # Fields to show in the form
    template_name = 'bookshelf/book_form.html'  # Template for creating a book
    success_url = reverse_lazy('book-list')
    permission_classes = [IsAuthenticated]
    
class BookUpdateView(UpdateView):
    model = Book
    fields = ['title', 'author', 'publication_year']  # Fields to edit
    template_name = 'bookshelf/book_form.html'  # Template for updating a book
    success_url = reverse_lazy('book-list') 
    permission_classes = [IsAuthenticated]
      
class BookDeleteView(DeleteView):
    model = Book
    template_name = 'bookshelf/book_confirm_delete.html'  # Template for confirming deletion
    success_url = reverse_lazy('book-list') 
    permission_classes = [IsAuthenticated]         
# Create your views here.

# Enable filtering, searching, and ordering
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]

    # Filter by title, author, and publication_year

    # Enable search functionality
    search_fields = ['title', 'author']

    # Enable ordering functionality
    ordering_fields = ['title', 'publication_year']
    ordering = ['title']  # Default ordering by title

# api/views.py

# api/views.py


    

from django.shortcuts import render
from django.views.generic import ListView
from django.views.generic import DetailView
from django.views.generic import CreateView
from django.views.generic import UpdateView
from django.views.generic import DeleteView
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.urls import reverse_lazy
from .models import Book

class BookListView(ListView):
    model = Book
    template_name = 'bookshelf/book_list.html'  # Define your template
    context_object_name = 'books'
    permission_classes = [AllowAny]

class BookDetailView(DetailView):
    model = Book
    template_name = 'bookshelf/book_detail.html'  # Template for displaying a single book
    context_object_name = 'book'
    permission_classes = [AllowAny]
    
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

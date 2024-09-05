from django.db import models

# Create your models here.
class Author(models.Model):
    name = models.CharField(max_length=50)
    
class Book(models.model):
    title = models.CharField(max_length=50)
    publication_year = models.IntegerField(max_length=50) 
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='books')

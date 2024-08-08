from models import Book
create_instances = Book.objects.create(title="1984", author="George Orwell", publication_year=1949)
create_instances.save()

retrieved_book = Book.objects.get(title='1984')
# print('Retrieved book:', retrieved_book)

# Update the title of the created book
retrieved_book.title = 'Nineteen Eighty-Four'
retrieved_book.save()
# print('Updated book title:', retrieved_book)

# Delete the book instance
retrieved_book.delete()
# print('Book deleted')
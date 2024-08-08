# delete.md

## delete  the instance create.md

from bookshelf.models import Book

```python
# deleting the  instance with the title “1984”, author “George Orwell”, and publication year 1948
retrieved_book.delete()(title="1984", author="George Orwell", publication_year=1949)

# Expected output: it delete the  file created in our instance  in the database with the given details.
# The output in Django shell might look something like this (with a different ID each time):
# <book: title = 1984>

# This documentation includes the Python command to delete a new `Book` instance and a comment explaining the expected output, demonstrating the successful retrieve of the instance.

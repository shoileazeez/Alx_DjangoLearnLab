# create.md

## Create a Book instance

```python
# Creating a Book instance with the title “1984”, author “George Orwell”, and publication year 1949
book = Book.objects.create(title="1984", author="George Orwell", publication_year=1949)

# Expected output: A new Book instance should be created in the database with the given details.
# The output in Django shell might look something like this (with a different ID each time):
# <Book: 1984 by George Orwell (1949)>


# This documentation includes the Python command to create a new `Book` instance and a comment explaining the expected output, demonstrating the successful creation of the instance.

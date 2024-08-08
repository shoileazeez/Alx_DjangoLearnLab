# retrieve.md

## create a retrieve file that retrieve file from the instance we created

```python
# Creating a Book instance with the title “1984”, author “George Orwell”, and publication year 1949
# creating an instance  that retrieve file from the instance we created

retrieved_book = Book.objects.get(title='1984')


# Expected output: it retrieve file created in our instance  in the database with the given details.
# The output in Django shell might look something like this (with a different ID each time):
# <book: title = 1984>

# This documentation includes the Python command to retrieve a new `Book` instance and a comment explaining the expected output, demonstrating the successful retrieve of the instance.

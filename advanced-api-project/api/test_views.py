from django.test import TestCase
from rest_framework.test import APITestCase, APIClient
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Book
from rest_framework import status

# Create your tests here.

class BookCreationTestCase(APITestCase):
    def setUp(self):
        # Create a user for authentication
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.client = APIClient()

    def test_create_book_authenticated(self):
        # Authenticate the client
        self.client.login(username='testuser', password='testpass')

        url = reverse('book-create')
        data = {
            'title': 'Test Book',
            'author': 'Test Author',
            'publication_year': 2021
        }
        response = self.client.post(url, data, format='json')

        # Check that the response is 201 Created
        self.assertEqual(response.status_code, 201)
        # Verify the book was created
        self.assertEqual(Book.objects.count(), 1)
        self.assertEqual(Book.objects.get().title, 'Test Book')

    def test_create_book_unauthenticated(self):
        url = reverse('book-create')
        data = {
            'title': 'Test Book',
            'author': 'Test Author',
            'publication_year': 2021
        }
        response = self.client.post(url, data, format='json')

        # Check that the response is 401 Unauthorized
        self.assertEqual(response.status_code, 401)


class BookRetrievalTestCase(APITestCase):
    def setUp(self):
        self.book = Book.objects.create(title='Existing Book', author='Existing Author', publication_year=2020)
        self.client = APIClient()

    def test_get_book_list(self):
        url = reverse('book-list')
        response = self.client.get(url, format='json')

        # Check that the response is 200 OK
        self.assertEqual(response.status_code, 200)
        # Verify that the response contains the book
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['title'], 'Existing Book')

    def test_get_book_detail(self):
        url = reverse('book-detail', args=[self.book.id])
        response = self.client.get(url, format='json')

        # Check that the response is 200 OK
        self.assertEqual(response.status_code, 200)
        # Verify that the response contains correct book data
        self.assertEqual(response.data['title'], 'Existing Book')

class BookUpdateTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.book = Book.objects.create(title='Old Title', author='Old Author', publication_year=2019)
        self.client = APIClient()

    def test_update_book_authenticated(self):
        self.client.login(username='testuser', password='testpass')
        url = reverse('book-update', args=[self.book.id])
        data = {
            'title': 'New Title',
            'author': 'New Author',
            'publication_year': 2021
        }
        response = self.client.put(url, data, format='json')

        # Check that the response is 200 OK
        self.assertEqual(response.status_code, 200)
        # Verify that the book was updated
        self.book.refresh_from_db()
        self.assertEqual(self.book.title, 'New Title')

    def test_update_book_unauthenticated(self):
        url = reverse('book-update', args=[self.book.id])
        data = {
            'title': 'New Title',
            'author': 'New Author',
            'publication_year': 2021
        }
        response = self.client.put(url, data, format='json')

        # Check that the response is 401 Unauthorized
        self.assertEqual(response.status_code, 401)
class BookDeletionTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.book = Book.objects.create(title='Book to Delete', author='Author', publication_year=2018)
        self.client = APIClient()

    def test_delete_book_authenticated(self):
        self.client.login(username='testuser', password='testpass')
        url = reverse('book-delete', args=[self.book.id])
        response = self.client.delete(url, format='json')

        # Check that the response is 204 No Content
        self.assertEqual(response.status_code, 204)
        # Verify that the book was deleted
        self.assertEqual(Book.objects.count(), 0)

    def test_delete_book_unauthenticated(self):
        url = reverse('book-delete', args=[self.book.id])
        response = self.client.delete(url, format='json')

        # Check that the response is 401 Unauthorized
        self.assertEqual(response.status_code, 401)

class BookFilterSearchOrderTestCase(APITestCase):
    def setUp(self):
        Book.objects.create(title='Harry Potter', author='J.K. Rowling', publication_year=1997)
        Book.objects.create(title='The Hobbit', author='J.R.R. Tolkien', publication_year=1937)
        Book.objects.create(title='1984', author='George Orwell', publication_year=1949)
        self.client = APIClient()

    def test_filter_by_author(self):
        url = reverse('book-list')
        response = self.client.get(url, {'author': 'Rowling'}, format='json')

        # Check that the response is 200 OK
        self.assertEqual(response.status_code, 200)
        # Verify that only the books by Rowling are returned
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['author'], 'J.K. Rowling')

    def test_search_title(self):
        url = reverse('book-list')
        response = self.client.get(url, {'search': 'hobbit'}, format='json')

        # Check that the response is 200 OK
        self.assertEqual(response.status_code, 200)
        # Verify that the correct book is returned
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['title'], 'The Hobbit')

    def test_ordering_by_publication_year(self):
        url = reverse('book-list')
        response = self.client.get(url, {'ordering': 'publication_year'}, format='json')

        # Check that the response is 200 OK
        self.assertEqual(response.status_code, 200)
        # Verify that books are ordered by publication_year
        publication_years = [book['publication_year'] for book in response.data]
        self.assertEqual(publication_years, sorted(publication_years))

class BookPermissionsTestCase(APITestCase):
    def setUp(self):
        self.book = Book.objects.create(title='Protected Book', author='Author', publication_year=2020)
        self.client = APIClient()

    def test_read_only_access_unauthenticated(self):
        # Unauthenticated user should be able to retrieve book list
        url = reverse('book-list')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, 200)

        # Unauthenticated user should not be able to create a book
        url = reverse('book-create')
        data = {'title': 'Unauthorized Create', 'author': 'No Auth', 'publication_year': 2021}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, 401)

    def test_full_access_authenticated(self):
        # Authenticate user
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.client.login(username='testuser', password='testpass')

        # Authenticated user should be able to create a book
        url = reverse('book-create')
        data = {'title': 'Authorized Create', 'author': 'Auth User', 'publication_year': 2021}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, 201)


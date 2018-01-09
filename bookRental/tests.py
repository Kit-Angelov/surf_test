from django.contrib.auth.models import AnonymousUser
import datetime
from django.utils import timezone
from django.urls import reverse
from rest_framework.test import APIRequestFactory, force_authenticate, APITestCase, APIClient
from django.test import TestCase, RequestFactory
from rest_framework.authtoken.models import Token
from .models import Lease, Book, User, Author
from dateutil.relativedelta import relativedelta


def user_create():
    user = User(username='test_user', balance=200)
    user.set_password('test_user_password')
    user.save()
    return user


def client_create(user):
    token = Token.objects.create(user=user)
    test_client = APIClient()
    test_client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
    return test_client


def author_create():
    author = Author(first_name='first_name_test_author', last_name='last_name_test_author')
    author.save()
    return author


def book_create(author):
    book = Book(name='test_book', author=author, price=66)
    book.save()
    return book


def lease_create(book, user, term):
    value = book.price * term
    if (user.balance - value) >= 0:
        user.balance -= value
        user.save()
        date_start = timezone.now()
        date_finish = date_start + relativedelta(months=term)
        lease = Lease(user=user, book=book, value=value, date_start=date_start, date_finish=date_finish)
        lease.save()
        return lease
    else:
        return None


class AuthorTests(APITestCase):

    def setUp(self):
        self.user = user_create()
        self.test_client = client_create(self.user)
        self.author = author_create()

    def test_list(self):
        response = self.test_client.get('/authors/')
        print('authors_list', response.data)
        self.assertEqual(response.status_code, 200)

    def test_detail(self):
        id = self.author.id
        response = self.test_client.get('/authors/' + str(id) + '/')
        print('authors_detail', response.data)
        self.assertEqual(response.status_code, 200)


class BookTests(APITestCase):

    def setUp(self):
        self.user = user_create()
        self.test_client = client_create(self.user)
        self.author = author_create()
        self.book = book_create(self.author)

    def test_list(self):
        response = self.test_client.get('/books/')
        print('books_list', response.data)
        self.assertEqual(response.status_code, 200)

    def test_detail(self):
        id = self.book.id
        response = self.test_client.get('/books/{}/'.format(str(id)))
        print('books_detail', response.data)
        self.assertEqual(response.status_code, 200)


class LeaseTests(APITestCase):

    def setUp(self):
        self.user = user_create()
        self.test_client = client_create(self.user)
        self.author = author_create()
        self.book = book_create(self.author)
        self.lease = lease_create(self.book, self.user, 2)

    def test_create(self):
        id = self.book.id
        response = self.test_client.post('/rent_a_book/{}/'.format(str(id)), {'term': '1'}, format='json')
        print('lease_created', response.data)
        self.assertEqual(response.status_code, 200)

    def test_list(self):
        response = self.test_client.get('/rented_books/')
        print('rented_books_list', response.data)
        self.assertEqual(response.status_code, 200)


class AuthTests(APITestCase):

    def setUp(self):
        self.user = user_create()
        self.test_client = APIClient()

    def test_auth(self):
        response = self.test_client.post('/login/',
                                         {"username": "test_user", "password": "test_user_password"},
                                         format='json')
        print(response)
        self.assertEqual(response.status_code, 200)

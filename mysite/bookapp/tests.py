from django.conf import settings
from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib.auth.models import User, Permission
from django.test import TestCase
from django.urls import reverse
from string import ascii_letters
from random import choices
from .models import Books, Order
from .utils import add_two_numbers
from .views import CreateBookView
# Create your tests here.

class AddTwoNumbersTestCase(TestCase):
    def test_add_two_numbers(self):
        res = add_two_numbers(2, 3)
        self.assertEqual(res, 5)

class CreateBookViewTestCase(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.user = User.objects.create_user(username='ivan_test',
                                            password='090206vb')

    @classmethod
    def tearDownClass(cls):
        cls.user.delete()

    def setUp(self) -> None:
        self.client.force_login(self.user)
        self.product_name = ''.join(choices(ascii_letters, k=10)) # будет взято 10 случайных символов
        Books.objects.filter(name=self.product_name).delete() # удаляем из бд, у кого совпадут имена

    def test_book_create_view(self):
        res = self.client.post(
            reverse('bookapp:create_book'),
            {
                'name':self.product_name,
                'price':'142',
                'discount':'1',
                'description':'test book ',
            }
        )
        self.assertRedirects(res, reverse('bookapp:books_list'))
        self.assertTrue(
            Books.objects.filter(name=self.product_name).exists()
        )

class BookDetailsViewTestCase(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.book = Books.objects.create(name='Test Details')

    @classmethod
    def tearDownClass(cls):
        cls.book.delete()

    def test_book_details_view(self):
        res = self.client.get(
            reverse('bookapp:book_details',
                    kwargs={'pk':self.book.pk}),
        )
        self.assertEqual(res.status_code, 200)

    def test_book_details_view_and_check_content(self):
        res = self.client.get(
            reverse('bookapp:book_details',
                    kwargs={'pk': self.book.pk}),
        )
        self.assertEqual(res, self.book.name)

class BooksListViewTestCase(TestCase):
    fixtures = [
        'books-fixtures.json'
    ]

    def test_books_list_view(self):
        res = self.client.get(reverse('bookapp:books_list'))
        #books = Books.objects.filter(archived=False).all()
        #books_ = res.context['books']

        #for b, b_ in zip(books, books_):
        #    self.assertEqual(b.pk, b_.pk)

        self.assertQuerySetEqual(
            qs=Books.objects.filter(archived=False).all(),# какие данные ожидаем получить
            values=(b.pk for b in  res.context['books']), # какие получили
            transform= lambda b: b.pk # как преобразовать данные из QuerySet, чтобы сравнить с values
        )
        self.assertTemplateUsed(res, 'bookapp/books_list.html')


class OrderListViewTestCase(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.user = User.objects.create_user(username='ivan_test',
                                            password='090206vb')

    @classmethod
    def tearDownClass(cls):
        cls.user.delete()


    def setUp(self):
        self.client.force_login(self.user)

    def test_orders_view(self):
        res = self.client.get(reverse('bookapp:orders_list'))
        self.assertContains(res, 'Orders')

    def test_orders_view_not_authenticated(self):
        self.client.logout()
        res = self.client.get(reverse('bookapp:orders_list'))
        #self.assertRedirects(res, str(settings.LOGIN_URL))
        self.assertIn(str(settings.LOGIN_URL), res.url)

class BooksExportViewTestCase(TestCase):
    fixtures = [
        'books-fixtures.json',
    ]
    def test_get_books_view(self):
        res = self.client.get(reverse('bookapp:books-export'))
        self.assertEqual(res.status_code, 200)
        books = Books.objects.order_by('pk').all()
        expected_data = [
            {
                'pk': book.pk,
                'name': book.name,
                'price': str(book.price),
                'archived': book.archived
            }
            for book in books
        ]
        books_data = res.json()
        self.assertEqual(
            books_data['books'],
            expected_data
        )


class OrderDetailViewTestCase(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.user = User.objects.create_user(username='test_user',
                                                        password='testpassword')

        permission = Permission.objects.get(codename='view_order')
        cls.user.user_permissions.add(permission)


        cls.book = Books.objects.create(name='Test Book',
                                         price=100,
                                         discount=10,
                                         description='Test book description',
                                         created_by=cls.user,
                                         )
        cls.order = Order.objects.create(delivery_address='Test Address',
                                          promocode='test',
                                          user=cls.user)
        cls.order.books.add(cls.book)

    @classmethod
    def tearDownClass(cls):
        cls.order.delete()
        cls.book.delete()
        cls.user.delete()

    def setUp(self):
        self.client.force_login(self.user)

    def test_order_details(self):
        res = self.client.get(
            reverse('bookapp:order_details',
                    kwargs={'pk': self.order.pk}))

        self.assertEqual(res.status_code, 200)
        self.assertContains(res, self.order.delivery_address)
        self.assertContains(res, self.order.promocode)
        self.assertEqual(res.context['order'].pk, self.order.pk)


class OrdersExportTestCase(TestCase):
    fixtures = [
        'users-fixtures.json',
        'books-fixtures.json',
        'orders-fixtures.json']

    @classmethod
    def setUpClass(cls):
        cls.admin_user = User.objects.create_user(
            username='admin',
            password='adminpassword',
            is_staff=True
        )

    @classmethod
    def tearDownClass(cls):
        cls.admin_user.delete()

    def setUp(self):
        self.client.force_login(self.admin_user)

    def test_get_orders_view(self):
        res = self.client.get(reverse('bookapp:export_order'))
        self.assertEqual(res.status_code, 200)

        orders = Order.objects.order_by('pk').all()
        expected_data = [
            {
                'id': order.pk,
                'delivery_address': order.delivery_address,
                'promocode': order.promocode,
                'user': order.user.pk,
                'books': list(order.books.values_list('pk', flat=True))
            }
            for order in orders
        ]
        self.assertEqual(res.json()['orders'], expected_data)

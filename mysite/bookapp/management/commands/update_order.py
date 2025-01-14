from django.contrib.auth.models import User
from django.core.management import BaseCommand

from bookapp.models import Order, Books
from bookapp.views import orders_list


class Command(BaseCommand):
    """Добавляем книги к заказу"""
    def handle(self, *args, **options):
        order = Order.objects.first()
        if not order:
            self.stdout.write('no order found')
            return
        books = Books.objects.all()
        for book in books:
            order.books.add(book)
        order.save()

        self.stdout.write(self.style.SUCCESS(
            f'Added books: {order.books.all()} to order {order}'))

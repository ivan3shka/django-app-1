from typing import Sequence

from django.contrib.auth.models import User
from django.core.management import BaseCommand
from django.db import transaction
from bookapp.models import Order, Books


class Command(BaseCommand):
    """Создаёт заказ с книгами"""
    @transaction.atomic()
    def handle(self, *args, **options):
        self.stdout.write('Create order with books')
        user = User.objects.get(username='ivan')
        # books: Sequence[Books] = Books.objects.defer(
        #     'description',
        #     'price',
        #     'created_at',
        # ).all() После defer говорим что не грузить
        books: Sequence[Books] = Books.objects.only('id')

        order, created = Order.objects.get_or_create(
                                            delivery_address='ul. Ivanova 12/2',
                                            promocode='promo2',
                                            user=user)
        """
        get_or_create возвращает кортеж, где второй объект это
        True (заказ создался) или False (заказ не создался)
        @transaction.atomic() - либо выполняется вся функция, либо ничего 
        """
        for book in books:
            order.books.add(book)
        order.save()
        self.stdout.write(self.style.SUCCESS(f'Created - {order}'))

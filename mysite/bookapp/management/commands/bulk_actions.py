from django.contrib.auth.models import User

from django.core.management import BaseCommand
from django.db import transaction
from bookapp.models import Books


class Command(BaseCommand):
    def handle(self, *args, **options):
        self.stdout.write('Start demo bulc actions')

        res = Books.objects.filter(
            name__contains='Book'
        ).update(discaunt=88)
        """
        contains - значит содержит. Значит все записи где name содержит Book
        будут обновлены.
        update(discount=88) - значит на каждой записи будет обновлено discount
        на 88
        """

        # info = [
        #     ('Bulc_1', '1099'),
        #     ('Bulc_2', '2099'),
        #     ('Bulc_3', '3099'),
        # ]
        #
        # books = [Books(name=name, price=price)
        #     for name, price in info
        # ]
        #
        # res = Books.objects.bulk_create(books)
        # """Создаем сразу несколько записей за 1 действие"""
        #
        # for obj in res:
        #     print(obj)

        self.stdout.write(self.style.SUCCESS('Done'))
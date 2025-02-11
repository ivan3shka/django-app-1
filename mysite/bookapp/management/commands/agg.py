from django.contrib.auth.models import User
from django.core.management import BaseCommand
from django.db import transaction
from django.db.models import Avg, Max, Min, Count, Sum

from bookapp.models import Books, Order


class Command(BaseCommand):
    def handle(self, *args, **options):
        self.stdout.write('Start demo aggregate')

        # res = Books.objects.filter(name__contains='Перси').aggregate(
        #     Avg('price'),
        #     Min('price'),
        #     max_price=Max('price'),
        #     count=Count('id')
        # )
        orders = Order.objects.annotate(
            total=Sum('books__price', default=0),
            books_count=Count('books'),
        )
        for order in orders:
            print(f'Order №{order.id}, with {order.books_count} books\n'
                  f'books worth {order.total}')
        self.stdout.write(self.style.SUCCESS('Done'))
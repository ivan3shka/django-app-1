from django.contrib.auth.models import User

from django.core.management import BaseCommand
from django.db import transaction
from bookapp.models import Books


class Command(BaseCommand):
    def handle(self, *args, **options):
        self.stdout.write('Start demo select fields')

        users_info = User.objects.values_list('username', flat=True)
        print(list(users_info))
        for u_info in users_info:
            print(u_info)
        # book_values = Books.objects.values('pk', 'name')
        # for b_values in book_values:
        #     print(b_values)

        self.stdout.write(self.style.SUCCESS('Done'))
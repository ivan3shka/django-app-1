from django.core.management import BaseCommand
from bookapp.models import Books

class Command(BaseCommand):
    """Создаёт книги"""
    def handle(self, *args, **options):
        self.stdout.write('Create books')
        books = ['Всадник без головы', 'Белый вождь', 'Азбука']
        for book in books:
            book, created = Books.objects.get_or_create(name=book)
            self.stdout.write(self.style.SUCCESS(f'Created - {book.name}'))
        self.stdout.write(self.style.SUCCESS('Created'))

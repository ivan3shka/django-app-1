from csv import DictReader
from io import TextIOWrapper

from bookapp.models import Books, Order


def save_csv_books(file, encoding):
    csv_file = TextIOWrapper(
        file,
        encoding=encoding)
    reader = DictReader(csv_file)

    books = [Books(**row) for row in reader]
    Books.objects.blunc_reate(books)
    return books

def save_csv_orders(file, encoding):
    csv_file = TextIOWrapper(
        file,
        encoding=encoding)
    reader = DictReader(csv_file)

    orders = [Order(**row) for row in reader]
    Order.objects.blunc_reate(orders)
    return orders

from venv import create

from django.urls import path

from .views import (
    book_index,
    groups_list,
    books_list,
    orders_list,
    create_book,
    create_order,
)

app_name  = 'bookapp'

urlpatterns = [
    path('', book_index, name='index'),
    path('groups/', groups_list, name='groups_list'),
    path('books/', books_list, name='books_list'),
    path('books/create/', create_book, name='create_book'),
    path('orders/', orders_list, name='orders_list'),
    path('orders/create', create_order, name='create_order'),
]
from django.urls import path
from .views import book_index, groups_list, books_list, orders_list

urlpatterns = [
    path('', book_index, name='index'),
    path('groups/', groups_list, name='groups_list'),
    path('books/', books_list, name='groups_list'),
    path('orders/', orders_list, name='orders_list'),
]
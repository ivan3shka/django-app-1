from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.contrib.auth.models import Group

from bookapp.models import Books, Order


# Create your views here.

def book_index(request: HttpRequest):
    books = [('война и мир', 1000), ('всадник без головы', 500), ('нарния', 700),
             ('колобок', 30)]
    date = '09/01/2025'
    count = 0
    context = {
        'books': books,
        'date': date,
        'caunt': count
    }
    return render(request, 'bookapp/book-index.html',
                  context=context)

def groups_list(request: HttpRequest):
    context = {
        'groups': Group.objects.prefetch_related('permissions').all()
    }
    return render(request, 'bookapp/groups-list.html',
                  context=context)

def books_list(request: HttpRequest):
    context = {
        'books': Books.objects.all(),
    }
    return render(request, 'bookapp/books-list.html',
                  context=context)

def orders_list(request: HttpRequest):
    context = {
        'orders': Order.objects.all()
    }
    return render(request, 'bookapp/orders-list.html',
                  context=context)

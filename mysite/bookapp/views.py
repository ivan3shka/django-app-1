from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect, reverse
from django.contrib.auth.models import Group

from bookapp.forms import CreateBookForm, CreateOrderForm
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

def create_book(request: HttpRequest) -> HttpResponse:
    if request.method == 'POST':
        form = CreateBookForm(request.POST)
        if form.is_valid():
            #name = form.cleaned_data['name']
            #price = form.cleaned_data['price']
            #Books.objects.create(name, price) -> Это вытаскивает данные из словаря, но у нас совпадают имена в словаре и которые надо, поэтому нормально
            #Books.objects.create(**form.cleaned_data)
            form.save()
            url = reverse('bookapp:books_list')
            return redirect(url)
    else:
        form = CreateBookForm()

    context = {
        'form': form
    }

    return render(request, 'bookapp/create-book.html',
                  context=context)

def create_order(request: HttpRequest) -> HttpResponse:
    if request.method == 'POST':
        form = CreateOrderForm(request.POST)
        if form.is_valid():
            #name = form.cleaned_data['name']
            #price = form.cleaned_data['price']
            #Books.objects.create(name, price) -> Это вытаскивает данные из словаря, но у нас совпадают имена в словаре и которые надо, поэтому нормально
            #Books.objects.create(**form.cleaned_data)
            form.save()
            url = reverse('bookapp:orders_list')
            return redirect(url)
    else:
        form = CreateOrderForm()

    context = {
        'form': form
    }

    return render(request, 'bookapp/create-order.html',
                  context=context)

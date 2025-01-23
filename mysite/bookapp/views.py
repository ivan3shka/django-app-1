from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib.auth.models import Group
from django.urls import reverse_lazy
from django.views.generic import (
                                TemplateView,
                                ListView,
                                DetailView,
                                CreateView,
                                UpdateView,
                                DeleteView,
                                )

from bookapp.forms import CreateBookForm, CreateOrderForm, GroupForm
from bookapp.models import Books, Order

from django.views import View

# Create your views here.

class BookIndexView(View):
    def get(self, request: HttpRequest) -> HttpResponse:
        books = [('война и мир', 1000), ('всадник без головы', 500),
                 ('нарния', 700),
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

class GroupsListView(View):
    def get(self, request: HttpRequest) -> HttpResponse:
        context = {
            'form': GroupForm(),
            'groups': Group.objects.prefetch_related('permissions').all()
        }
        return render(request, 'bookapp/groups-list.html',
                      context=context)

    def post(self, request:HttpRequest) -> HttpResponse:
        form = GroupForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(request.path)


class BookDetailsView(DetailView):
    template_name = 'bookapp/book-details-9.html'
    model = Books
    context_object_name = 'book'


class BooksListView(ListView):
    template_name = 'bookapp/books_list.html'
    #model = Books
    context_object_name = 'books'

    queryset = Books.objects.filter(archived=False)


class OrdersListView(ListView):
    queryset = (Order.objects.select_related('user').prefetch_related('books'))


class OrderDetailsView(DetailView):
    queryset = (Order.objects.select_related('user').prefetch_related('books'))


class CreateBookView(CreateView):
    model = Books
    fields = 'name', 'price', 'discount', 'description'
    success_url = reverse_lazy('bookapp:books_list')


class UpdateBookView(UpdateView):
    model = Books
    fields = 'name', 'price', 'discount', 'description'
    template_name_suffix = '_update_form'

    def get_success_url(self):# Потому что хотим вернуть страницу Details. Для этого нам нужен pk, а он не доступен на верхнем уровне
        return reverse('bookapp:book_details',
                       kwargs={'pk':self.object.pk}) #На object доступен тот объект, который сейчас обновляется


class DeleteBookView(DeleteView):
    model = Books
    success_url = reverse_lazy('bookapp:books_list')

    def form_valid(self, form): # переопределяем метод удаления, чтобы книги шли в архив, но оставались в бд
        success_url = self.get_success_url()
        self.object.archived = True
        self.object.save()
        return HttpResponseRedirect(success_url)


class CreateOrderView(CreateView):
    model = Order
    fields = 'user', 'delivery_address', 'promocode', 'books'
    success_url = reverse_lazy('bookapp:orders_list')


class UpdateOrderView(UpdateView):
    model = Order
    fields = 'user', 'delivery_address', 'promocode', 'books'
    template_name_suffix = '_update_form'

    def get_success_url(self):# Потому что хотим вернуть страницу Details. Для этого нам нужен pk, а он не доступен на верхнем уровне
        return reverse('bookapp:order_details',
                       kwargs={'pk':self.object.pk})


class DeleteOrderView(DeleteView):
    model = Order
    success_url = reverse_lazy('bookapp:orders_list')




############
"""Уже не пользуемся, но оставлю. Чтобы в случае чего были под рукой"""
############

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
    return render(request, 'bookapp/books_list.html',
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
            # name = form.cleaned_data['name']
            # price = form.cleaned_data['price']
            # Books.objects.create(name, price) -> Это вытаскивает данные из словаря, но у нас совпадают имена в словаре и которые надо, поэтому нормально
            # Books.objects.create(**form.cleaned_data)
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
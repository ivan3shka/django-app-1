from django.http import HttpRequest, HttpResponse, HttpResponseRedirect, \
    Http404, JsonResponse
from django.shortcuts import render, redirect, reverse
from django.contrib.auth.models import Group
from django.urls import reverse_lazy
from django.views.generic import (
                                ListView,
                                DetailView,
                                CreateView,
                                UpdateView,
                                DeleteView,
                                )

from bookapp.forms import GroupForm, BookForm
from bookapp.models import Books, Order, BookImage

from django.views import View
from django.contrib.auth.mixins import (LoginRequiredMixin, # нельзя попасть, пока не проёдешь логин
                                        PermissionRequiredMixin, # нельзя попасть, без нужного разрешения
                                        UserPassesTestMixin, # позволяет в качестве проверки использовать любую функ
                                        )

from rest_framework.viewsets import ModelViewSet
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from bookapp.serializers import BookSerializer, OrderSerializer


# Create your views here.

class BookViewSet(ModelViewSet):
    queryset = Books.objects.all()
    serializer_class = BookSerializer
    filter_backends = [
        SearchFilter,
        #DjangoFilterBackend,
        OrderingFilter,

    ]
    search_fields = ['name', 'description']
    filterset_fields = [
        'name',
        'description',
        'price',
        'discount',
        'archived',
    ]
    ordering_fields = [
        'name',
        'price',
        'discount',
    ]


class OrderViewSet(ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    filter_backends = [
        #SearchFilter,
        DjangoFilterBackend,
        OrderingFilter,
    ]
    search_fields = ['promocode', 'delivery_address']
    filterset_fields = [
        'user',
        'delivery_address',
        'books',
    ]
    ordering_fields = [
        'user',
        'delivery_address',
    ]


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
            'caunt': count,
            'items': 3,
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
    queryset = Books.objects.prefetch_related('images')
    #model = Books
    context_object_name = 'book'


class BooksListView(ListView):
    template_name = 'bookapp/books_list.html'
    #model = Books
    context_object_name = 'books'

    queryset = Books.objects.filter(archived=False)


class OrdersListView(LoginRequiredMixin, ListView):
    queryset = (Order.objects.select_related('user').prefetch_related('books'))


class OrderDetailsView(PermissionRequiredMixin, DetailView):
    queryset = (Order.objects.select_related('user').prefetch_related('books'))
    permission_required = 'bookapp.view_order' # показываем, какое разрешение нужно


class CreateBookView(CreateView, PermissionRequiredMixin):
    #def test_func(self):
    #    return self.request.user.is_superuser # возвращает bool
    permission_required = 'books.add_books'
    model = Books
    fields = 'name', 'price', 'discount', 'description', 'preview'
    success_url = reverse_lazy('bookapp:books_list')
    def form_valid(self, form):
        form.instance.created_by = self.request.user
        response = super().form_valid(form)
        return response


class UpdateBookView(UpdateView, PermissionRequiredMixin):
    model = Books
    #fields = 'name', 'price', 'discount', 'description', 'preview'
    form_class = BookForm
    template_name_suffix = '_update_form'
    permission_required = 'bookapp.change_books'

    def form_valid(self, form):
        res = super().form_valid(form)
        for image in form.files.getlist('images'):
            BookImage.objects.create(
                book=self.object,
                image=image,
            )
        return res

    def get_success_url(self):# Потому что хотим вернуть страницу Details. Для этого нам нужен pk, а он не доступен на верхнем уровне
        return reverse('bookapp:book_details',
                       kwargs={'pk':self.object.pk}) #На object доступен тот объект, который сейчас обновляется

    def get_queryset(self):
        user = self.request.user
        if user.is_superuser:
            return Books.objects.all()  # Суперпользователь может редактировать любую книгу
        return Books.objects.filter(
            created_by=user)  # Остальные только свои книги

    def dispatch(self, request, *args, **kwargs):
        book = self.get_object()  # Получаем книгу
        if not (
                (request.user.has_perm('bookapp.change_books')
                 and request.user == book.created_by)
                or request.user.is_superuser):
            raise Http404('You do not have permission to edit this book.')
        return super().dispatch(request, *args, **kwargs)


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


class BooksDataExportView(View):
    def get(self, request: HttpRequest) -> JsonResponse:
        books = Books.objects.order_by('pk').all()
        books_data = [
            {
            'pk': book.pk,
            'name': book.name,
            'price': book.price,
            'archived': book.archived
            }
            for book in books
        ]
        return JsonResponse({'books': books_data})


class OrdersExportView(UserPassesTestMixin, View):
    def test_func(self):
        return self.request.user.is_staff

    def handle_no_permission(self):
        return JsonResponse({'error': 'Forbidden'}, status=403)

    def get(self, request):
        orders = Order.objects.order_by('pk').all()
        orders_data = [
            {
                'id': order.pk,
                'delivery_address': order.delivery_address,
                'promocode': order.promocode,
                'user': order.user.pk,
                'books': list(order.books.values_list('pk', flat=True))
            }
            for order in orders
        ]
        return JsonResponse({'orders': orders_data})

############
"""Уже не пользуемся, но оставлю. Чтобы в случае чего были под рукой"""
############

# def book_index(request: HttpRequest):
#     books = [('война и мир', 1000), ('всадник без головы', 500), ('нарния', 700),
#              ('колобок', 30)]
#     date = '09/01/2025'
#     count = 0
#     context = {
#         'books': books,
#         'date': date,
#         'caunt': count
#     }
#     return render(request, 'bookapp/book-index.html',
#                   context=context)
#
# def groups_list(request: HttpRequest):
#     context = {
#         'groups': Group.objects.prefetch_related('permissions').all()
#     }
#     return render(request, 'bookapp/groups-list.html',
#                   context=context)
#
# def books_list(request: HttpRequest):
#     context = {
#         'books': Books.objects.all(),
#     }
#     return render(request, 'bookapp/books_list.html',
#                   context=context)
#
# def create_book(request: HttpRequest) -> HttpResponse:
#     if request.method == 'POST':
#         form = CreateBookForm(request.POST)
#         if form.is_valid():
#             #name = form.cleaned_data['name']
#             #price = form.cleaned_data['price']
#             #Books.objects.create(name, price) -> Это вытаскивает данные из словаря, но у нас совпадают имена в словаре и которые надо, поэтому нормально
#             #Books.objects.create(**form.cleaned_data)
#             form.save()
#             url = reverse('bookapp:books_list')
#             return redirect(url)
#     else:
#         form = CreateBookForm()
#
#     context = {
#         'form': form
#     }
#
#     return render(request, 'bookapp/create-book.html',
#                   context=context)
#
# def create_order(request: HttpRequest) -> HttpResponse:
#     if request.method == 'POST':
#         form = CreateOrderForm(request.POST)
#         if form.is_valid():
#             # name = form.cleaned_data['name']
#             # price = form.cleaned_data['price']
#             # Books.objects.create(name, price) -> Это вытаскивает данные из словаря, но у нас совпадают имена в словаре и которые надо, поэтому нормально
#             # Books.objects.create(**form.cleaned_data)
#             form.save()
#             url = reverse('bookapp:orders_list')
#             return redirect(url)
#     else:
#         form = CreateOrderForm()
#
#     context = {
#         'form': form
#     }
#
#     return render(request, 'bookapp/create-order.html',
#                   context=context)
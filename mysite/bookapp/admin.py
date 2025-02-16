from django.contrib import admin
from django.db.models import QuerySet
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect
from django.urls import path

from .common import save_csv_books, save_csv_orders
from .forms import CSVImportForm
# Register your models here.

from .admin_mixins import ExportAsCSVMixins
from .models import Books, Order, BookImage


@admin.action(description='Archive book')
def mark_archived(modeladmin: admin.ModelAdmin, request: HttpRequest,
                  queryset: QuerySet): #Создаёт действие, которое можно будет в админке выполнить ля всех выделенных
    queryset.update(archived=True)

@admin.action(description='Unarchive book')
def mark_unarchived(modeladmin: admin.ModelAdmin, request: HttpRequest,
                  queryset: QuerySet): #Создаёт действие, которое можно будет в админке выполнить ля всех выделенных
    queryset.update(archived=False)

class OrderInline(admin.StackedInline):
    model = Books.orders.through

class BookInline(admin.TabularInline):
    model = BookImage

@admin.register(Books)
class BooksAdmin(admin.ModelAdmin, ExportAsCSVMixins):
    actions = [
        mark_archived,
        mark_unarchived,
        'export_csv',
    ]
    inlines = [
        OrderInline,
        BookInline,
    ]
    fieldsets = [
        (None, {
            'fields': ('name',)
        }),
        ('Price options', { #Price options - название секции
            'fields': ('price', 'discount',), #fields - то что входит в секцию
            'classes': ('collapse', 'wide')  #classes- доп возможности секции, collapse - скрывает секцию, wide - добавит белого пространства
        }),
        ('Images', {
            'fields': ('preview', ),
        }),
        ('Extra options', {
            'fields': ('archived', ),
            'classes': ('collapse', ),
            'description': 'Extra options, fields: created_at'
        })

    ]
    list_display = 'pk', 'name_short', 'price', 'discount', 'archived'
    list_display_links = 'pk', 'name_short'
    ordering = ('pk',)
    search_fields = 'name', 'discount'

    change_list_template = 'bookapp/books_changelist.html'

    def name_short(self, obj: Books) -> str:
        if len(obj.name) > 15:
            return obj.name[:15] + '...'
        return obj.name


    def import_csv(self, request:HttpRequest) -> HttpResponse:
        if request.method == 'GET':
            form = CSVImportForm()
            context = {
                'form': form
            }
            return render(request, 'admin/csv_form.html', context)
        form = CSVImportForm(request.POST, request.FILES)
        if not form.is_valid():
            context = {
                'form': form
            }
            return render(request, 'admin/csv_form.html',
                          context, status=400)
        save_csv_books(
            file=form.files['csv_file'].file,
            encoding=request.encoding)
        self.message_user(request, 'Data from CSV was imported')
        return redirect('..')

    def get_urls(self):
        urls = super().get_urls()
        new_urls = [
            path('import-books-csv/', self.import_csv, name='import_books_csv')
        ]
        return new_urls + urls


class ProductInline(admin.TabularInline):
    model = Order.books.through


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    inlines = [
        ProductInline,
    ]
    list_display = 'delivery_address', 'promocode', 'created_at', 'user_verbose'

    change_list_template = 'bookapp/orders_changelist.html'

    def get_queryset(self, request):
        return Order.objects.select_related('user').prefetch_related('books')

    def user_verbose(self, obj: Order) -> str:
        return obj.user.first_name or obj.user.username

    def import_csv(self, request:HttpRequest) -> HttpResponse:
        if request.method == 'GET':
            form = CSVImportForm()
            context = {
                'form': form
            }
            return render(request, 'admin/csv_form.html', context)
        form = CSVImportForm(request.POST, request.FILES)
        if not form.is_valid():
            context = {
                'form': form
            }
            return render(request, 'admin/csv_form.html',
                          context, status=400)
        save_csv_orders(
            file=form.files['csv_file'].file,
            encoding=request.encoding)
        self.message_user(request, 'Data from CSV was imported')
        return redirect('..')

    def get_urls(self):
        urls = super().get_urls()
        new_urls = [
            path('import-orders-csv/', self.import_csv,
                 name='import_orders_csv')
        ]
        return new_urls + urls


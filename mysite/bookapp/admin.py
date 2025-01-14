from django.contrib import admin
from django.db.models import QuerySet
from django.http import HttpRequest

# Register your models here.

from .admin_mixins import ExportAsCSVMixins
from .models import Books, Order

@admin.action(description='Archive book')
def mark_archived(modeladmin: admin.ModelAdmin, request: HttpRequest,
                  queryset: QuerySet): #Создаёт действие, которое можно будет в админке выполнить ля всех выделенных
    queryset.update(archived=True)

@admin.action(description='Unarchive book')
def mark_unarchived(modeladmin: admin.ModelAdmin, request: HttpRequest,
                  queryset: QuerySet): #Создаёт действие, которое можно будет в админке выполнить ля всех выделенных
    queryset.update(archived=False)

class OrderInline(admin.TabularInline):
    model = Books.orders.through

@admin.register(Books)
class BooksAdmin(admin.ModelAdmin, ExportAsCSVMixins):
    actions = [
        mark_archived,
        mark_unarchived,
        'export_csv',
    ]
    inlines = [
        OrderInline,
    ]
    fieldsets = [
        (None, {
            'fields': ('name',)
        }),
        ('Price options', { #Price options - название секции
            'fields': ('price', 'discount',), #fields - то что входит в секцию
            'classes': ('collapse', 'wide')  #classes- доп возможности секции, collapse - скрывает секцию, wide - добавит белого пространства
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

    def name_short(self, obj: Books) -> str:
        if len(obj.name) > 15:
            return obj.name[:15] + '...'
        return obj.name

class ProductInline(admin.TabularInline):
    model = Order.books.through

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    inlines = [
        ProductInline,
    ]
    list_display = 'delivery_address', 'promocode', 'created_at', 'user_verbose'

    def get_queryset(self, request):
        return Order.objects.select_related('user').prefetch_related('books')

    def user_verbose(self, obj: Order) -> str:
        return obj.user.first_name or obj.user.username


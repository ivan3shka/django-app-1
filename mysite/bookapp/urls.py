from venv import create

from django.urls import path

from .views import (
    BookIndexView,
    GroupsListView,
    BookDetailsView,
    BooksListView,
    OrdersListView,
    OrderDetailsView,
    CreateBookView,
    UpdateBookView,
    DeleteBookView,
    CreateOrderView,
    UpdateOrderView,
    DeleteOrderView,
    BooksDataExportView,
    OrdersExportView,

)

app_name  = 'bookapp'

urlpatterns = [
    path('', BookIndexView.as_view(), name='index'),
    path('groups/', GroupsListView.as_view(), name='groups_list'),
    path('books/', BooksListView.as_view(), name='books_list'),
    path('books/<int:pk>/', BookDetailsView.as_view(), name='book_details'),
    path('books/create/', CreateBookView.as_view(), name='create_book'),
    path('books/export/', BooksDataExportView.as_view(), name='books_export'),
    path('books/<int:pk>/update/', UpdateBookView.as_view(), name='book_update'),
    path('books/<int:pk>/confirm-archive/', DeleteBookView.as_view(),
         name='book_delete'),
    path('orders/', OrdersListView.as_view(), name='orders_list'),
    path('orders/<int:pk>/', OrderDetailsView.as_view(), name='order_details'),
    path('orders/create/', CreateOrderView.as_view(), name='create_order'),
    path('orders/export/', OrdersExportView.as_view(), name='export_order'),
    path('orders/<int:pk>/update/', UpdateOrderView.as_view(),
         name='order_update'),
    path('orders/<int:pk>/confirm-delete/', DeleteOrderView.as_view(),
         name='order_delete'),
]
from venv import create

from django.urls import path, include
from django.views.decorators.cache import cache_page

from rest_framework.routers import DefaultRouter

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
    BookViewSet,
    OrderViewSet,
    LatestBooksFeed,
    OrdersByUserView,
    ExportUserOrdersView,

)

app_name  = 'bookapp'

routers = DefaultRouter()
routers.register('books', BookViewSet)
routers.register('orders', OrderViewSet)

urlpatterns = [
    path('', cache_page(60 * 3)(BookIndexView.as_view()), name='index'),
    path('groups/', GroupsListView.as_view(), name='groups_list'),
    path('api/', include(routers.urls)),
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
    path('orders/by_user/<int:pk>/', OrdersByUserView.as_view(),
         name='orders_by_user'),
    path("orders/export/<int:pk>/", ExportUserOrdersView.as_view(),
         name="export_user_orders"),
    path('orders/<int:pk>/update/', UpdateOrderView.as_view(),
         name='order_update'),
    path('orders/<int:pk>/confirm-delete/', DeleteOrderView.as_view(),
         name='order_delete'),
    path('books/latest/feed/', LatestBooksFeed(), name='books_feed'),
]
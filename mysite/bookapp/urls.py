from django.urls import path
from .views import book_index

urlpatterns = [
    path('', book_index, name='index')
]
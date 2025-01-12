from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

# Create your views here.

def shop_index(request: HttpRequest):
    books = [('война и мир', 1000), ('всадник без головы', 500), ('нарния', 700),
             ('колобок', 30)]
    date = '09/01/2025'
    count = 0
    context = {
        'books': books,
        'date': date,
        'caunt': count
    }
    return render(request, 'shopapp/shop-index.html',
                  context=context)
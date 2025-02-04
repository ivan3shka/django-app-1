from django.contrib.auth.models import User
from django.db import models


def book_preview_directory_path(instance: 'Books', filename: str) -> str:
    """
    Чтобы каждое медиа было в своей именованной папке
    instance - тот объект над которым происходит взаимодействие
    """
    return 'books/book_{pk}/preview/{filename}'.format(
        pk=instance.pk,
        filename=filename
    )

class Books(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(default=0, max_digits=8, decimal_places=2)
    discount = models.SmallIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    archived = models.BooleanField(default=False)
    description =models.TextField(null=False, blank=True)
    created_by = models.ForeignKey(User, on_delete=models.PROTECT)
    preview = models.ImageField(null=True, blank=True,
                                upload_to=book_preview_directory_path)

    def __str__(self) -> str:
        return f'Books(pk={self.pk}, name={self.name!r})'


def books_images_directory_path(instance: 'BookImage', filename: str) -> str:
    return 'books/book_{pk}/images/{filename}'.format(
        pk=instance.book.pk,
        filename=filename
    )


class BookImage(models.Model):
    book = models.ForeignKey(Books, on_delete=models.CASCADE,
                             related_name='images')
    image = models.ImageField(upload_to=books_images_directory_path)
    description = models.CharField(max_length=200, null=False, blank=True)


class Order(models.Model):
    delivery_address = models.TextField(null=True, blank=True)
    promocode = models.CharField(max_length=20, null=False, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    books = models.ManyToManyField(Books, related_name='orders')
    receipt = models.FileField(null=True, upload_to='orders/receipts/')
    """
    receipt - загружает чек после завершения заказа.
    upload_to - путь, куда загружать файлы
    """



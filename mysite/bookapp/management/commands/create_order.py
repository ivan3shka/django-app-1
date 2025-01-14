from django.contrib.auth.models import User
from django.core.management import BaseCommand

from bookapp.models import Order


class Command(BaseCommand):
    """Создаёт заказ"""
    def handle(self, *args, **options):
        self.stdout.write('Create order')
        user = User.objects.get(username='ivan')
        order = Order.objects.get_or_create(delivery_address='ul. Ylotsa 4',
                                            promocode='LOL123',
                                            user=user)
        self.stdout.write(self.style.SUCCESS(f'Created - {order}'))

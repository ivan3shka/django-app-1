from rest_framework import serializers

from .models import Books, Order


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Books
        fields = (
            'pk',
            'name',
            'price',
            'discount',
            'description',
            'preview',
            'created_at',
            'archived',

        )

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = (
            'pk',
            'user',
            'delivery_address',
            'promocode',
            'books',
            'created_at',
            'receipt',
        )
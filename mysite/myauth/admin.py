from django.contrib import admin

# Register your models here.

from django.contrib import admin
from .models import Profile  # Импортируй нужные модели

@admin.register(Profile)  # Удобный способ регистрации
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'bio', 'agreement_accepted')  # Колонки в списке
    search_fields = ('user__username', 'bio')  # Поиск по юзернейму и био

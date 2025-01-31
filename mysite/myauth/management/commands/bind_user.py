from django.contrib.auth.models import User, Group, Permission
from django.core.management import BaseCommand

class Command(BaseCommand): # создаём группу пользователей с определёнными правами
    def handle(self, *args, **options):
        user = User.objects.get(pk=4)
        group, created = Group.objects.get_or_create(
            name='profile_manager'
        )
        permission_profile = Permission.objects.get(
            codename='view_profile'
        )
        permission_logentry = Permission.objects.get(
            codename='view_logentry'
        )

        # добавления разрешения в группу
        group.permissions.add(permission_profile)

        # добавления user в группу
        user.groups.add(group)

        # связать user напрямую с разрешением
        user.user_permissions.add(permission_logentry)

        group.save()
        user.save()


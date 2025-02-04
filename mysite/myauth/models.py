from django.contrib.auth.models import User
from django.db import models

# Create your models here.

def avatar_directory_path(instance: 'Profile', filename: str):
    return 'users/user_{pk}/avatar/{filename}'.format(
        pk=instance.pk,
        filename=filename
    )

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(max_length=500, blank=True)
    avatar = models.ImageField(verbose_name=avatar_directory_path,
                               null=True, blank=True, )
    agreement_accepted = models.BooleanField(default=False)

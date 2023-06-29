from django.db import models
from django.contrib.auth.models import User


def profile_avatar_directory_path(instance: 'Profile', filename: str) -> str:
    return f'users/user {instance.user.pk}/avatar/{filename}'


class Profile(models.Model):
    user = models.OneToOneField(User, related_name='profile', on_delete=models.CASCADE)
    bio = models.TextField(max_length=500, blank=True)
    agreement_accepted = models.BooleanField(default=False)
    avatar = models.ImageField(null=True, blank=True, upload_to=profile_avatar_directory_path)

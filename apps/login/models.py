from django.db import models
from django.contrib.auth.models import User, AbstractUser
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.translation import ugettext_lazy as _

from django_gravatar.helpers import get_gravatar_url


class Profile(models.Model):
    """User extended."""

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    email_confirmed = models.BooleanField(default=False)
    news_letter = models.BooleanField(default=False)
    avatar = models.ImageField(upload_to='avatars/', blank=True)
    description = models.CharField(max_length=10000, default="")
    # other fields...


@receiver(post_save, sender=User)
def update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()

import uuid
import random
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import reverse
from django.conf import settings
from rest_framework.authtoken.models import Token
from core import managers

from django.dispatch import receiver
from django.db.models.signals import post_save


class Base(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=_('Created by'),
                                   related_name=_("%(class)s_created_by"), null=True, blank=True)
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=_('Last Updated by'),
                                   related_name=_("%(class)s_last_updated_by"), null=True, blank=True)

    class Meta:
        abstract = True


@python_2_unicode_compatible
class User(AbstractUser):

    mobile = models.CharField(max_length=20, unique=True)
    mobile_code = models.CharField(max_length=5, default='+91')
    address = models.TextField(null=True, blank=True)
    last_logged_in_ip = models.GenericIPAddressField(default=None, null=True, blank=True)
    is_locked = models.BooleanField(default=False)
    retry_attempts = models.IntegerField(default=0)
    first_time_login = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = managers.UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['mobile']

    class Meta(AbstractUser.Meta):
        AbstractUser._meta.get_field('username').max_length = 254
        AbstractUser._meta.get_field('first_name').max_length = 255
        AbstractUser._meta.get_field('last_name').max_length = 255
        # AbstractUser._meta.get_field('email').required = True

    def __str__(self):
        return self.mobile

    def get_auth_token(self):
        return "Token " + Token.objects.get(user_id=self.id).key

    def change_auth_token(self):
        Token.objects.get(user_id=self.id).delete()
        Token.objects.create(user=self)



@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)
    for u in User.objects.all():
        Token.objects.get_or_create(user=u)
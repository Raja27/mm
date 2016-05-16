__author__ = 'rajaprasanna'

from django.contrib.auth.models import BaseUserManager
from django.conf import settings
from django.apps import apps as django_apps


class UserManager(BaseUserManager):
    use_in_migrations = True

    def create_user(self, username, **extra_fields):
        """
        Creates and saves a User with the given username, email and password.
        """
        if not username:
            raise ValueError('The given username must be set')
        password = extra_fields.pop('password')
        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

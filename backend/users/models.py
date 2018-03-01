from __future__ import unicode_literals

from datetime import datetime

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.functional import cached_property
from phonenumber_field.modelfields import PhoneNumberField

from backend import settings
from backend.settings import ACCOUNT_ACTIVATION_DAYS
from users.managers import PersonManager
from utils.models_methods import _string_type


class Person(AbstractUser):
    is_active = models.BooleanField(default=False)
    friends = models.ManyToManyField('self', through='Friend', symmetrical=False)
    phone = PhoneNumberField('phone', unique=True)
    email = models.EmailField('email address', unique=True)
    birthday = models.DateField('birthday')
    manager = PersonManager

    def save(self, *args, **kwargs):
        if self.is_staff:
            self.is_active = True
        if settings.DEBUG:
            self.is_active = True  # activate user without email confirmation for dev purposes
        return super(Person, self).save()

    @property
    def activation_expired(self):
        return not self.is_active and self.date_joined + ACCOUNT_ACTIVATION_DAYS > datetime.now()

    @classmethod
    def string_type(cls):
        return _string_type(cls)


class Friend(models.Model):
    first_user = models.ForeignKey(Person, on_delete=models.CASCADE, related_name='first_set',
                                   verbose_name='friendship from')
    second_user = models.ForeignKey(Person, on_delete=models.CASCADE, related_name='second_set',
                                    verbose_name='friendhship to')

    class Meta:
        unique_together = [['first_user', 'second_user']]

    def __str__(self):
        return f'{self.first_user.username} to {self.second_user.username}'

    @classmethod
    def string_type(cls):
        return _string_type(cls)

from __future__ import unicode_literals

from datetime import datetime

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.functional import cached_property

from backend.settings import ACCOUNT_ACTIVATION_DAYS
from users.managers import PersonManager


class Person(AbstractUser):
    is_active = models.BooleanField(default=False)
    friends = models.ManyToManyField('self', through='Friend', symmetrical=False)
    manager = PersonManager

    @property
    def expired(self):
        return not self.is_active and self.date_joined + ACCOUNT_ACTIVATION_DAYS > datetime.now()


class Friend(models.Model):
    first = models.ForeignKey(Person, on_delete=models.CASCADE, related_name='first_set')
    second = models.ForeignKey(Person, on_delete=models.CASCADE, related_name='second_set')

    class Meta:
        unique_together = ['first', 'second']

    def __str__(self):
        return f'{self.first.username} to {self.second.username}'

from __future__ import unicode_literals

from datetime import datetime

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.functional import cached_property

from backend.settings import ACCOUNT_ACTIVATION_DAYS
from users.managers import PersonManager


class Person(AbstractUser):
    is_active = models.BooleanField(default=False)
    manager = PersonManager

    @property
    def expired(self):
        return not self.is_active and self.date_joined + ACCOUNT_ACTIVATION_DAYS > datetime.now()

from django.contrib.auth.models import UserManager


class PersonManager(UserManager):
    def remove_expired(self):
        self.filter(verified=False, expired=True).delete()

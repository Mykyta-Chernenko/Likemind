from django.contrib.auth.backends import ModelBackend

from users.models import Person
from utils.django_annoying import get_object_or_None


class PersonBackend(ModelBackend):
    def get_user(self, user_id):
        try:
            return Person.objects.get(pk=user_id)
        except Person.DoesNotExist:
            pass

    def authenticate(self, request, username=None, password=None, **kwargs):

        user = get_object_or_None(Person, username=username) or \
               get_object_or_None(Person, email=username) or \
               get_object_or_None(Person, phone=username)
        if user and user.check_password(password):
            return user

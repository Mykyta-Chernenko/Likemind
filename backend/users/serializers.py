from django.core.mail import send_mail
from rest_framework import serializers

from backend.settings import PUBLIC_KEY_PERSON_ID, DOMAIN
from cryptography.fernet import Fernet

from chat.models import PrivateMessage
from utils.drf_mixins import SerializerFieldsMixin
from .models import Person, Friend
from drf_queryfields import QueryFieldsMixin


class CreateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Person
        fields = ('password', 'username', 'first_name', 'last_name', 'email', 'id',)
        extra_kwargs = {
            'password': {'write_only': True},
            'username': {'required': True}
        }

    def create(self, validated_data):
        user = super(CreateUserSerializer, self).create(validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user


class NestedUserSerializer(QueryFieldsMixin, SerializerFieldsMixin, serializers.ModelSerializer):
    class Meta:
        model = Person
        fields = ('id', 'email', 'username', 'phone', 'first_name', 'last_name', 'password')
        extra_kwargs = {
            'password': {'write_only': True}
        }


class UserSerializer(NestedUserSerializer):
    class Meta(NestedUserSerializer.Meta):
        fields = NestedUserSerializer.Meta.fields
        depth = 2

    def create(self, validated_data):
        user = super(UserSerializer, self).create(validated_data)
        user.set_password(validated_data['password'])
        user.is_active = False
        user.save()
        cryption = Fernet(PUBLIC_KEY_PERSON_ID)
        user_decoded_id = cryption.encrypt(str(user.id).encode('utf-8')).decode('utf-8')
        url = f'{DOMAIN}/activate_account/{user_decoded_id}'
        send_mail(message=f'Перейдите по ссылке ниже, чтобы активировать свой аккаунт в LikeMind\n{url}',
                  from_email='LikeMind',
                  subject='Подтверждение регистрации', recipient_list=[user.email],
                  html_message=f'\n<a href="{url}">activate {url}</a>')
        print('send mail')
        return user


class FriendSerializer(QueryFieldsMixin, SerializerFieldsMixin, serializers.ModelSerializer):
    first = serializers.PrimaryKeyRelatedField(read_only=True)
    second = serializers.PrimaryKeyRelatedField(queryset=Person.objects.all())

    class Meta:
        model = Friend
        fields = ['id', 'first', 'second']
        depth = 1

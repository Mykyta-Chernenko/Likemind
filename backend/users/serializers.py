from django.core.mail import send_mail
from rest_framework import serializers
from rest_framework.authtoken.models import Token

from backend.settings import PUBLIC_KEY_PERSON_ID, DOMAIN
from cryptography.fernet import Fernet
from .models import Person
import base64


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
        Token.objects.create(user=user)
        return user


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Person
        fields = ('id', 'email', 'username', 'first_name', 'last_name', 'password')
        extra_kwargs = {
            'password': {'write_only': True}
        }

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
        return user

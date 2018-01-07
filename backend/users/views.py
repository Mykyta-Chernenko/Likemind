from django.http import HttpResponse, JsonResponse
from rest_framework import renderers
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.decorators import detail_route
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.reverse import reverse
from cryptography.fernet import Fernet
from users.encoding import decode
from backend.settings import PUBLIC_KEY_PERSON_ID
from .models import Person
from .serializers import CreateUserSerializer, UserSerializer


def activate_account(request, activate_link):
    cryption = Fernet(PUBLIC_KEY_PERSON_ID)
    id = cryption.decrypt(activate_link.encode('utf-8')).decode('utf-8')
    person = get_object_or_404(Person, id=id)
    person.is_active = True
    person.save()
    return HttpResponse('Successful activation')


class ObtainAuthToken(APIView):
    renderer_classes = (renderers.JSONRenderer,)
    serializer_class = AuthTokenSerializer
    http_method_names = ('post',)

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        user_details = UserSerializer(instance=user).data
        user_details['token'] = str(token)
        return Response(user_details)


class UserView(APIView):
    serializer_class = UserSerializer
    http_method_names = ('get', 'post', 'put')

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        person = serializer.create(serializer.validated_data)
        token = Token.objects.get_or_create(user=person)
        return JsonResponse(status=201, data={'id': person.id, 'token': str(token)})

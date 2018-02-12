from django.db.models import Q
from django.http import HttpResponse, JsonResponse, HttpRequest
from rest_framework import renderers
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.decorators import detail_route
from rest_framework.generics import get_object_or_404, GenericAPIView, CreateAPIView, UpdateAPIView, RetrieveAPIView, \
    DestroyAPIView, ListAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.reverse import reverse
from cryptography.fernet import Fernet
from rest_framework_jwt.views import obtain_jwt_token

from users.encoding import decode
from backend.settings import PUBLIC_KEY_PERSON_ID
from .models import Person, Friend
from .serializers import CreateUserSerializer, UserSerializer, FriendSerializer


def activate_account(request, activate_link):
    cryption = Fernet(PUBLIC_KEY_PERSON_ID)
    id = cryption.decrypt(activate_link.encode('utf-8')).decode('utf-8')
    person = get_object_or_404(Person, id=id)
    person.is_active = True
    person.save()
    return HttpResponse('Successful activation')


class ObtainAuthToken(GenericAPIView):
    renderer_classes = (renderers.JSONRenderer,)
    serializer_class = AuthTokenSerializer
    http_method_names = ('post',)
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        user_details = UserSerializer(instance=user).data
        user_details['token'] = str(token)
        return Response(user_details)


class UserListView(CreateAPIView):
    '''
    post:
    Create a new person. Creates email for account verifying.
    '''
    serializer_class = UserSerializer
    permission_classes = [AllowAny]
    http_method_names = ['post']

    # def create(self, request, *args, **kwargs):
    #     serializer = self.serializer_class(data=request.data)
    #     serializer.is_valid(raise_exception=True)
    #     person = serializer.create(serializer.validated_data)
    #     token = obtain_jwt_token(request._request, username=serializer.validated_data['username'],
    #                              password=serializer.validated_data['password'])
    #     return JsonResponse(status=201, data={'id': person.id, 'token': str(token)})


class UserDetailView(UpdateAPIView, RetrieveAPIView, DestroyAPIView):
    '''
    put:
    Update a person's info

    delete:
    Delete a person

    get:
    Get a person
    '''
    serializer_class = UserSerializer
    queryset = Person.objects.all()
    http_method_names = ['put', 'get', 'delete']


class SelfUserDetailView(UpdateAPIView, RetrieveAPIView, DestroyAPIView):
    '''
    Operates the user tha is taken from JWT token
    put:
    Update a person's info

    delete:
    Delete a person

    get:
    Get a person
    '''
    serializer_class = UserSerializer
    queryset = Person.objects.all()
    http_method_names = ['put', 'get', 'delete']

    def get_object(self):
        self.kwargs['pk'] = self.request.user.pk
        return super(SelfUserDetailView, self).get_object()


class FriendListView(CreateAPIView, ListAPIView):
    serializer_class = FriendSerializer
    queryset = Friend.objects.all()
    http_method_names = ['get', 'post']

    def get_queryset(self):
        person = self.request.user
        return Friend.objects.filter(Q(first=person) | Q(second=person))

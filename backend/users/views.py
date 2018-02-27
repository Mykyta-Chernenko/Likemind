from django.db.models import Q
from django.http import HttpResponse
from rest_framework import renderers
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.generics import get_object_or_404, GenericAPIView, CreateAPIView, UpdateAPIView, RetrieveAPIView, \
    DestroyAPIView, ListAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.status import HTTP_400_BAD_REQUEST, HTTP_204_NO_CONTENT
from cryptography.fernet import Fernet

from backend.settings import PUBLIC_KEY_PERSON_ID
from .models import Person, Friend
from .serializers import UserSerializer, FriendSerializer


def activate_account(request, activate_link):
    '''
    :param request: django request
    :param activate_link: link that was sent to email and can't be decoded with key
    :return: Http response about successful activation or error occurred
    '''
    cryption = Fernet(PUBLIC_KEY_PERSON_ID)
    id = cryption.decrypt(activate_link.encode('utf-8')).decode('utf-8')
    person = get_object_or_404(Person, id=id)
    person.is_active = True
    person.save()
    return HttpResponse('Successful activation')


class ObtainAuthToken(GenericAPIView):
    '''
    post:
    accepts user's username/email/phone as username field and password and returns jwt token
    '''
    renderer_classes = (renderers.JSONRenderer,)
    serializer_class = AuthTokenSerializer
    http_method_names = ['post']
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

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        following = set(Friend.objects.filter(first=instance).values_list('second', flat=True))
        followers = set(Friend.objects.filter(second=instance).values_list('first', flat=True))
        friends = following.intersection(followers)
        following = following.difference(friends)
        followers = followers.difference(friends)
        serializer = {}
        serializer['friends'] = friends
        serializer['followers'] = followers
        serializer['following'] = following
        serializer.update(self.get_serializer(instance).data)
        return Response(serializer, status=200)


class SelfUserDetailView(UserDetailView):
    '''
    Operates the user tha is taken from JWT token
    put:
    Update a person's info

    delete:
    Delete a person

    get:
    Get a person
    '''

    def get_object(self):
        self.kwargs['pk'] = self.request.user.pk
        return super(SelfUserDetailView, self).get_object()


class FriendListView(CreateAPIView, ListAPIView):
    '''
    get:
    gets list of friendship objects for the user from the token
    (If you want to get person's followers, friend etc. you'd better request user's details)
    (To check relationship between users use check relationship view
    post:
    creates one-way friendship from the token user to the second one
    '''
    serializer_class = FriendSerializer
    queryset = Friend.objects.all()
    http_method_names = ['get', 'post']

    def get_queryset(self):
        person = self.request.user
        return Friend.objects.filter(Q(first=person) | Q(second=person))

    def perform_create(self, serializer):
        serializer.save(first=self.request.user)


class FriendDetailView(DestroyAPIView):
    '''
    delete:
    removes friendship by id, doesn't return updated relationship (Don't know how it can be useful)
    '''
    serializer_class = FriendSerializer
    queryset = Friend.objects.all()
    http_method_names = ['delete']


class FriendDeleteFriendshipToUser(GenericAPIView):
    '''
    delete:
    requires param:user to whom friendship should be deleted
    (removing will be made in one way. So if users are friends and the first user deletes friendship to the second one,
    second one will become the follower of the first). Returns updated relationship between users
    '''
    serializer_class = FriendSerializer
    queryset = Friend.objects.all()
    http_method_names = ['delete']

    def delete(self, request, *args, **kwargs):
        user = request.user
        second = request.POST.get('user_id')
        if not second:
            return Response(status=HTTP_400_BAD_REQUEST, data='no second user specified')
        second = get_object_or_404(Person, pk=second)
        Friend.objects.filter(second=second).delete()
        response = {}
        response['text'] = f"{user} doesn't follow user{second} now"
        response.update(FriendCheckRelationsWithUser.get_relationship_from_first_to_second_user(user, second))
        return Response(data=f"{user} doesn't follow user{second} now", status=HTTP_204_NO_CONTENT)


class FriendCheckRelationsWithUser(GenericAPIView):
    '''
    get:
    will return 4 params: follower (True if the given user follows the user from the token), followee (vice versa), friend, nothing
    '''

    serializer_class = FriendSerializer
    queryset = Friend.objects.all()
    http_method_names = ['get']

    def get(self, request, *args, **kwargs):
        user = request.user
        second = get_object_or_404(Person, pk=kwargs['user_id'])
        if user == second:
            return Response(data='This is the user from the token send user that you want to check relationship with',
                            status=HTTP_400_BAD_REQUEST)
        relationship = self.get_relationship_from_first_to_second_user(user, second)
        return Response(relationship)

    @staticmethod
    def get_relationship_from_first_to_second_user(first, second):
        followee = Friend.objects.filter(first=first, second=second).exists()
        follower = Friend.objects.filter(first=second, second=first).exists()
        friend = followee and follower
        relationship = {}
        relationship['followee'] = not friend and followee
        relationship['follower'] = not friend and follower
        relationship['friendship'] = friend
        relationship['nothing'] = not (friend or followee or follower)
        return relationship

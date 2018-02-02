from django.contrib import admin
from django.urls import path
from rest_framework import routers
from rest_framework.documentation import include_docs_urls

from chat.views import PrivateChatList, PrivateMessageList
from users.views import ObtainAuthToken, activate_account, UserDetailView, UserListView, FriendListView, \
    SelfUserDetailView
from rest_framework_jwt.views import obtain_jwt_token

urlpatterns = [
    path('api/obtain-auth-token/', obtain_jwt_token),
    # users
    path('api/users/', UserListView.as_view(), name='user-list'),
    path('api/users/<int:pk>/', UserDetailView.as_view(), name='user-detail'),
    path('api/self-users/', SelfUserDetailView.as_view(), name='self-user-detail'),
    path('api/friends/', FriendListView.as_view(), name='friend-list'),
    path('activate-account/<str:activate_link>/', activate_account, name='activate-account'),
    # chat
    path('api/private-chats/', PrivateChatList.as_view(), name='private-chat-list'),
    path('api/private-messages/', PrivateMessageList.as_view(), name='private-message-list'),

    path('admin/', admin.site.urls),
    path('docs/', include_docs_urls(title='LikeMind API', permission_classes=[]))
]

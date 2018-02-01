"""restapi URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from django.urls import path
from rest_framework import routers
from rest_framework.documentation import include_docs_urls

from chat.views import PrivateChatList
from users.views import ObtainAuthToken, activate_account, UserDetailView, UserListView, FriendListView
from rest_framework_jwt.views import obtain_jwt_token

urlpatterns = [
    path('api/obtain-auth-token/', obtain_jwt_token),
    path('api/users/', UserListView.as_view(), name='user-list'),
    path('api/users/<int:pk>/', UserDetailView.as_view(), name='user-detail'),
    path('api/friends/', FriendListView.as_view(), name='friend-list'),
    path('api/private_chats/', PrivateChatList.as_view(), name='private-chat-list'),
    path('activate_account/<str:activate_link>/', activate_account, name='activate-account'),
    path('admin/', admin.site.urls),
    path('docs/', include_docs_urls(title='LikeMind API'))
]

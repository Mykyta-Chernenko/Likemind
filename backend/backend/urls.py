from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, register_converter, include
from rest_framework import routers
from rest_framework.documentation import include_docs_urls

from backend import settings
from chat.views import PrivateChatList, PrivateMessageList
from files.views import ChatFileList
from users.views import ObtainAuthToken, activate_account, UserDetailView, UserListView, FriendListView, \
    SelfUserDetailView
from rest_framework_jwt.views import obtain_jwt_token
from files.views import ChatFileList
from files.converters import ChatTypeConverter

register_converter(ChatTypeConverter, 'chat_type')
urlpatterns = [
    path('admin/', admin.site.urls),
    path('docs/', include_docs_urls(title='LikeMind API', permission_classes=[])),
    path('api/obtain-auth-token/', obtain_jwt_token),
    path('api/', include('users.urls')),
    path('api/', include('chat.urls')),
    path('api/', include('files.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

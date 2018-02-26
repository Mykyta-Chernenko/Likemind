from django.urls import path, register_converter

from chat.views import PrivateChatList, PrivateMessageList, PrivateMessageDetail, EncryptedPrivateMessageList, \
    GroupMessageList, ChatContent
from files.converters import ChatTypeConverter

register_converter(ChatTypeConverter, 'chat_type')
urlpatterns = [
    path('private-chats/', PrivateChatList.as_view(), name='private-chat-list'),
    path('private-messages/list/<int:chat_id>/', PrivateMessageList.as_view(), name='private-message-list'),
    path('private-messages/detail/<int:pk>/', PrivateMessageDetail.as_view(), name='private-message-detail'),
    path('encrypted-private-messages/list/<int:chat_id>/', EncryptedPrivateMessageList.as_view(),
         name='encrypted-private-message-list'),
    path('encrypted-private-messages/detail/<int:pk>/', EncryptedPrivateMessageList.as_view(),
         name='encrypted-private-message-detail'),
    path('group-messages/list/<int:chat_id>/', GroupMessageList.as_view(), name='group-message-list'),
    path('group-messages/detail/<int:pk>/', GroupMessageList.as_view(), name='group-message-detail'),
    path('chat/<chat_type:chat_model>/<int:chat_id>/content/', ChatContent.as_view(), name='chat-content-list'),
]

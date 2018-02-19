from django.urls import path

from chat.views import PrivateChatList, PrivateMessageList, PrivateMessageDetail

urlpatterns = [
    path('private-chats/', PrivateChatList.as_view(), name='private-chat-list'),
    path('private-messages/list/<int:chat_pk>/', PrivateMessageList.as_view(), name='private-message-list'),
    path('private-messages/detail/<int:pk>/', PrivateMessageDetail.as_view(), name='private-message-detail'),
]

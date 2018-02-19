from django.urls import path

from files.views import ChatFileList

urlpatterns = [
    path('files/<chat_type:chat_model>/<int:chat_id>/file', ChatFileList.as_view(), name='chat-file-list'),
]

from django.urls import path

from files.views import ChatFileList, ChatImageList, ChatAudioList, ChatVideoList

urlpatterns = [
    path('files/<chat_type:chat_model>/<int:chat_id>/file', ChatFileList.as_view(), name='chat-file-list'),
    path('files/<chat_type:chat_model>/<int:chat_id>/image', ChatImageList.as_view(), name='chat-image-list'),
    path('files/<chat_type:chat_model>/<int:chat_id>/audio', ChatAudioList.as_view(), name='chat-audio-list'),
    path('files/<chat_type:chat_model>/<int:chat_id>/video', ChatVideoList.as_view(), name='chat-video-list'),
]

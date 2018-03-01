from django.urls import path

from files.views import ChatFileList, ChatImageList, ChatAudioList, ChatVideoList, ChatFileDetail, ChatVideoDetail, \
    ChatAudioDetail, ChatImageDetail

urlpatterns = [
    path('files/<int:pk>/', ChatFileDetail.as_view(), name='chat-file-detail'),
    path('images/<int:pk>/', ChatImageDetail.as_view(), name='chat-image-detail'),
    path('audios/<int:pk>/', ChatAudioDetail.as_view(), name='chat-audio-detail'),
    path('videos/<int:pk>/', ChatVideoDetail.as_view(), name='chat-video-detail'),
    path('files/<chat_type:chat_model>/<int:chat_id>/', ChatFileList.as_view(), name='chat-file-list'),
    path('images/<chat_type:chat_model>/<int:chat_id>/', ChatImageList.as_view(), name='chat-image-list'),
    path('audios/<chat_type:chat_model>/<int:chat_id>/', ChatAudioList.as_view(), name='chat-audio-list'),
    path('videos/<chat_type:chat_model>/<int:chat_id>/', ChatVideoList.as_view(), name='chat-video-list'),
]

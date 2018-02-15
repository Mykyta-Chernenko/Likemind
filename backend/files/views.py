from asgiref.sync import async_to_sync
from django.contrib.contenttypes.models import ContentType
from django.shortcuts import render

# Create your views here.
from requests import request
from rest_framework import views
from rest_framework.generics import CreateAPIView, ListAPIView, get_object_or_404
from rest_framework.parsers import FileUploadParser
from rest_framework.viewsets import ModelViewSet

from chat.models import PrivateChat
from files.forms import ImageUploadForm
from files.serializers import ChatFileSerializer


class ChatFileList(CreateAPIView, ListAPIView):
    serializer_class = ChatFileSerializer

    def create(self, request, *args, **kwargs):
        model = kwargs.get('chat_model')
        model_id = kwargs.get('chat_id')
        chat = get_object_or_404(model, pk=model_id)
        content_type = ContentType.objects.get(app_label=chat._meta.app_label, model=chat._meta.model_name)
        object_id = model_id
        request.data['chat'] = chat
        request.data['content_type'] = content_type.id
        request.data['object_id'] = object_id
        return super(ChatFileList, self).create(request, *args, **kwargs)

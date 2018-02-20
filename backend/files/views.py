import datetime
from copy import deepcopy

import channels
from asgiref.sync import async_to_sync
from django.contrib.contenttypes.models import ContentType
from rest_framework.generics import CreateAPIView, ListAPIView, get_object_or_404
from chat.consts import TEXT_MESSAGE, REVERSE_CHAT_TYPES
from files.models import ChatFile
from files.serializers import ChatFileSerializer
from utils.websocket_utils import WebSocketEvent


class ChatFileList(CreateAPIView, ListAPIView):
    serializer_class = ChatFileSerializer
    queryset = ChatFile.objects.all()

    def get_chat(self, **kwargs):
        if kwargs:
            model = kwargs.get('chat_model')
            model_id = kwargs.get('chat_id')
        else:
            model = self.kwargs.get('chat_model')
            model_id = self.kwargs.get('chat_id')
        chat = get_object_or_404(model, pk=model_id)
        return ContentType.objects.get(app_label=chat._meta.app_label, model=chat._meta.model_name), model_id

    def create(self, request, *args, **kwargs):
        content_type, object_id = self.get_chat(**kwargs)
        request.data['content_type'] = content_type.id
        request.data['object_id'] = object_id
        result = super(ChatFileList, self).create(request, *args, **kwargs)
        chat = result.data['chat']
        file = result.data['file']
        content = f'file can be downloaded via link <a href="{file}"></a>'
        channel_layer = channels.layers.get_channel_layer()
        time = datetime.datetime.now().strftime('%Y-%m-%dT%H:%M:%S')
        model = kwargs.get('chat_model')
        model_name = REVERSE_CHAT_TYPES[model]
        model_string_name = f'{model_name}-{object_id}'
        data = {
            'action_type': TEXT_MESSAGE,
            'action': {
                'chat_type': model_name,
                'chat': chat['id'],
                'owner': request.user.id,
                'created_at': time,
                'text': content,
                'edited': False,
                'edited_at': time
            }
        }
        chat_data = deepcopy(data)
        chat_data['type'] = 'chat.message'
        chat_data = WebSocketEvent(chat_data['action_type'], chat_data['action'], chat_data['type']).to_dict_flat()
        user_data = deepcopy(data)
        user_data['type'] = 'user.event'
        user_data = WebSocketEvent(user_data['action_type'], user_data['action'], user_data['type']).to_dict()
        async_to_sync(channel_layer.group_send)(model_string_name, chat_data)
        return result

    def perform_create(self, serializer):
        content_type, object_id = self.get_chat()
        serializer.save(content_type=content_type, object_id=object_id)

    def get_queryset(self):
        content_type, object_id = self.get_chat()
        return self.queryset.filter(content_type=content_type, object_id=object_id)

    def list(self, request, *args, **kwargs):
        content_type, object_id = self.get_chat(**kwargs)
        self.queryset = self.queryset.filter(content_type=content_type, object_id=object_id)
        return super(ChatFileList, self).list(request, *args, **kwargs)

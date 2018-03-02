from copy import deepcopy
from datetime import datetime

from attr import dataclass

from chat.consts import CHAT_TEXT_MESSAGE, CHAT_UPDATE_TEXT_MESSAGE, CHAT_DELETE_TEXT_MESSAGE
from chat.consumers import CONSUMER_CHAT_MESSAGE, CONSUMER_USER_EVENT
from files.consts import CHAT_IMAGE_MESSAGE, CHAT_VIDEO_MESSAGE, CHAT_FILE_MESSAGE, CHAT_AUDIO_MESSAGE, \
    CHAT_DELETE_IMAGE_MESSAGE, CHAT_DELETE_VIDEO_MESSAGE, \
    CHAT_DELETE_AUDIO_MESSAGE, CHAT_DELETE_FILE_MESSAGE
from utils.consts import TIME_TZ_FORMAT

event_types = [CONSUMER_CHAT_MESSAGE, CONSUMER_USER_EVENT]


class ActionType:
    flat_dict = None

    def __init__(self):
        self.flat_dict = {}

    def to_dict(self):
        _dict = deepcopy(vars(self))
        _dict['action_type'] = self.action_type()
        return _dict

    def to_flat_dict(self):
        if self.flat_dict:
            return self.flat_dict
        _dict = self.to_dict()
        for key, value in _dict.items():
            self._rec_to_dict_flat(key, value)
        return self.flat_dict

    def _rec_to_dict_flat(self, key, value):
        if not isinstance(value, dict):
            if key in self.flat_dict:
                print(self.flat_dict)
                raise KeyError('key {} already exists'.format(key))
            self.flat_dict[key] = value
        else:
            for key, value in value.items():
                self._rec_to_dict_flat(key, value)

    @classmethod
    def action_type(cls):
        raise NotImplementedError


class ChatContentMessageAction(ActionType):
    id: int
    chat_type: str
    chat: int
    owner: int
    created_at: datetime
    string_type: str

    def __init__(self, id: int, chat_type: int, chat: int, owner: int, created_at: datetime, string_type: str):
        self.id = id
        self.chat_type = chat_type
        self.chat = chat
        self.owner = owner
        self.created_at = datetime.strftime(created_at, TIME_TZ_FORMAT)
        self.string_type = string_type
        super(ChatContentMessageAction, self).__init__()


class ChatTextMessageAction(ChatContentMessageAction):
    text: str
    edited: bool
    edited_at: datetime

    def __init__(self, id: int, chat_type: int, chat: int, owner: int, created_at: datetime, string_type: str,
                 text: str, edited: bool,
                 edited_at: datetime):
        self.text = text
        self.edited = edited
        self.edited_at = datetime.strftime(edited_at, TIME_TZ_FORMAT)
        super(ChatTextMessageAction, self).__init__(id, chat_type, chat, owner, created_at, string_type)

    @classmethod
    def action_type(cls):
        return CHAT_TEXT_MESSAGE


class ChatTextMessageUpdateAction(ChatTextMessageAction):

    @classmethod
    def action_type(cls):
        return CHAT_UPDATE_TEXT_MESSAGE


class ChatTextMessageDeleteAction(ChatTextMessageAction):

    @classmethod
    def action_type(cls):
        return CHAT_DELETE_TEXT_MESSAGE


class ChatImageMessageAction(ChatContentMessageAction):
    image: str

    def __init__(self, id: int, chat_type: int, chat: int, owner: int, created_at: datetime, string_type: str,
                 image: str):
        self.image = image
        super(ChatImageMessageAction, self).__init__(id, chat_type, chat, owner, created_at, string_type)

    @classmethod
    def action_type(cls):
        return CHAT_IMAGE_MESSAGE


class ChatImageMessageDeleteAction(ChatImageMessageAction):

    @classmethod
    def action_type(cls):
        return CHAT_DELETE_IMAGE_MESSAGE


class ChatVideoMessageAction(ChatContentMessageAction):
    video: str

    def __init__(self, id: int, chat_type: int, chat: int, owner: int, created_at: datetime, string_type: str,
                 video: str):
        self.video = video
        super(ChatVideoMessageAction, self).__init__(id, chat_type, chat, owner, created_at, string_type)

    @classmethod
    def action_type(cls):
        return CHAT_VIDEO_MESSAGE


class ChatVideoMessageDeleteAction(ChatVideoMessageAction):

    @classmethod
    def action_type(cls):
        return CHAT_DELETE_VIDEO_MESSAGE


class ChatAudioMessageAction(ChatContentMessageAction):
    audio: str

    def __init__(self, id: int, chat_type: int, chat: int, owner: int, created_at: datetime, string_type: str,
                 audio: str):
        self.audio = audio
        super(ChatAudioMessageAction, self).__init__(id, chat_type, chat, owner, created_at, string_type)

    @classmethod
    def action_type(cls):
        return CHAT_AUDIO_MESSAGE


class ChatAudioMessageDeleteAction(ChatAudioMessageAction):

    @classmethod
    def action_type(cls):
        return CHAT_DELETE_AUDIO_MESSAGE


class ChatFileMessageAction(ChatContentMessageAction):
    file: str

    def __init__(self, id: int, chat_type: int, chat: int, owner: int, created_at: datetime, string_type: str,
                 file: str):
        self.file = file
        super(ChatFileMessageAction, self).__init__(id, chat_type, chat, owner, created_at, string_type)

    @classmethod
    def action_type(cls):
        return CHAT_FILE_MESSAGE


class ChatFileMessageDeleteAction(ChatFileMessageAction):

    @classmethod
    def action_type(cls):
        return CHAT_DELETE_FILE_MESSAGE


class WebSocketEvent:
    def __init__(self, action: ActionType, type=None):
        if type:
            if not type in event_types:
                raise ValueError('No such consumer event type')
            self.type = type
        self.action = action

    def to_dict(self):
        _dict = deepcopy(vars(self))
        _dict.pop('action')
        _dict['action'] = self.action.to_dict()
        _dict['action_type'] = _dict['action']['action_type']
        _dict['action'].pop('action_type')
        return _dict

    def to_dict_flat(self):
        _dict = deepcopy(vars(self))
        _dict.pop('action')
        _dict.update(self.action.to_flat_dict())
        return _dict

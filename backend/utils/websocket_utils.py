from copy import deepcopy
from datetime import datetime

from chat.consts import TEXT_MESSAGE, CHAT_TYPES
from chat.consumers import CONSUMER_CHAT_MESSAGE, CONSUMER_USER_EVENT

action_types = [TEXT_MESSAGE]
event_types = [CONSUMER_CHAT_MESSAGE, CONSUMER_USER_EVENT]


class WebSocketEvent(dict):

    def __init__(self, action_type, action, type=None):
        super(WebSocketEvent, self).__init__()
        self.flat_dict = {}
        if not action_type in action_types:
            raise ValueError('No such action type')
        if not action['chat_type'] in CHAT_TYPES.keys():
            raise ValueError('No such chat type')
        if type and not type in event_types:
            raise ValueError('No such consumer event type')
        self.action_type = action_type
        if type:
            self.type = type
        _action = {}
        if action_type == TEXT_MESSAGE:
            _action['chat_type'] = action['chat_type']
            _action['chat'] = int(action['chat'])
            _action['owner'] = int(action['owner'])
            _action['created_at'] = datetime.strftime(
                action['created_at'] \
                    if isinstance(action['created_at'], datetime) \
                    else datetime.strptime(action['created_at'], '%Y-%m-%dT%H:%M:%S'),
                '%Y-%m-%dT%H:%M:%S')
            _action['text'] = str(action['text'])
            _action['edited'] = bool(action['edited'])
            _action['edited_at'] = datetime.strftime(
                action['edited_at'] \
                    if isinstance(action['edited_at'], datetime) \
                    else datetime.strptime(action['edited_at'], '%Y-%m-%dT%H:%M:%S'),
                '%Y-%m-%dT%H:%M:%S')
        self.action = _action

    def to_dict(self):
        return vars(self)

    def to_dict_flat(self):
        if self.flat_dict:
            return self.flat_dict
        dict = vars(self)
        for key, value in dict.items():
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

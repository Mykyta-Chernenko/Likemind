from chat.models import EncryptedPrivateChat, GroupChat, PrivateChat

CHAT_TYPES = {model.string_type(): model for model in (PrivateChat, GroupChat, EncryptedPrivateChat)}


class ChatTypeConverter:
    regex = ('({})|' * len(CHAT_TYPES))[:-1].format(*[key for key in CHAT_TYPES.keys()])

    def to_python(self, _key):
        for key, value in CHAT_TYPES.items():
            if key == _key:
                return value

    def to_url(self, _value):
        for key, value in CHAT_TYPES.items():
            if value == _value:
                return key

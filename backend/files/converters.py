from chat.models import PrivateChat, GroupChat, EncryptedPrivateChat


class ChatTypeConverter:
    chat_types = {'private-chat': PrivateChat, 'group-chat': GroupChat, 'encrypted-private-chat': EncryptedPrivateChat}
    regex = ('({})|' * len(chat_types))[:-1].format(*[key for key in chat_types.keys()])

    def to_python(self, _key):
        for key, value in self.chat_types.items():
            if key == _key:
                return value

    def to_url(self, _value):
        for key, value in self.chat_types.items():
            if value == _value:
                return key

from chat.models import PrivateChat, GroupChat, EncryptedPrivateChat, PrivateMessage, GroupMessage, \
    EncryptedPrivateMessage, AbstractMessage

LAST_MESSAGE = 'last-message'
MESSAGE = 'message'

PRIVATE_CHAT = PrivateChat.string_type()
ENCRYPTED_PRIVATE_CHAT = EncryptedPrivateChat.string_type()
GROUP_CHAT = GroupChat.string_type()

PRIVATE_MESSAGE = PrivateChat.string_type()
GROUP_MESSAGE = GroupMessage.string_type()
ENCRYPTED_PRIVATE_MESSAGE = EncryptedPrivateMessage.string_type()

CHAT_TEXT_MESSAGE = 'chat-text-message'

TEXT_MESSAGE_FIELD = AbstractMessage.get_field()

CHAT_TYPE_TO_MESSAGE_TYPE = {PrivateChat: PrivateMessage, GroupChat: GroupMessage,
                             EncryptedPrivateChat: EncryptedPrivateMessage}
MESSAGE_TYPE_TO_CHAT_TYPE = {value: key for key, value in CHAT_TYPE_TO_MESSAGE_TYPE.items()}

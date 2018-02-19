from chat.models import PrivateChat, GroupChat, EncryptedPrivateChat, PrivateMessage, GroupMessage, \
    EncryptedPrivateMessage

LAST_MESSAGE = 'last-message'
PRIVATE_CHAT = PrivateChat.string_type()
ENCRYPTED_PRIVATE_CHAT = EncryptedPrivateChat.string_type()
GROUP_CHAT = GroupChat.string_type()
MESSAGE = 'message'
TEXT_MESSAGE = 'text-message'
CHAT_TYPES = {PRIVATE_CHAT: PrivateChat, GROUP_CHAT: GroupChat, ENCRYPTED_PRIVATE_CHAT: EncryptedPrivateChat}
REVERSE_CHAT_TYPES = {value: key for key, value in CHAT_TYPES.items()}
CHAT_TYPE_TO_MESSAGE_TYPE = {PrivateChat: PrivateMessage, GroupChat: GroupMessage,
                             EncryptedPrivateChat: EncryptedPrivateMessage}

from chat.models import PrivateChat, GroupChat, EncryptedPrivateChat, PrivateMessage, GroupMessage, \
    EncryptedPrivateMessage

LAST_MESSAGE = 'last_message'
PRIVATE_CHAT = 'private_chat'
ENCRYPTED_PRIVATE_CHAT = 'encrypted_private_chat'
GROUP_CHAT = 'group_chat'
MESSAGE = 'message'
TEXT_MESSAGE = 'text_message'
CHAT_TYPES = {PRIVATE_CHAT: PrivateChat, GROUP_CHAT: GroupChat, ENCRYPTED_PRIVATE_CHAT: EncryptedPrivateChat}
REVERSE_CHAT_TYPES = {value: key for key, value in CHAT_TYPES.items()}
CHAT_TYPE_TO_MESSAGE_TYPE = {PrivateChat: PrivateMessage, GroupChat: GroupMessage,
                             EncryptedPrivateChat: EncryptedPrivateMessage}

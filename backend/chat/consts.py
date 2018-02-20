from chat.models import PrivateChat, GroupChat, EncryptedPrivateChat, PrivateMessage, GroupMessage, \
    EncryptedPrivateMessage

LAST_MESSAGE = 'last-message'
PRIVATE_CHAT = PrivateChat.string_type()
ENCRYPTED_PRIVATE_CHAT = EncryptedPrivateChat.string_type()
GROUP_CHAT = GroupChat.string_type()
MESSAGE = 'message'
CHAT_TEXT_MESSAGE = 'chat-text-message'
CHAT_FILE_MESSAGE = 'chat-file-message'
CHAT_IMAGE_MESSAGE = 'chat-image-message'
CHAT_AUDIO_MESSAGE = 'chat-audio-message'
CHAT_VIDEO_MESSAGE = 'chat-video-message'

CHAT_TYPES = {PRIVATE_CHAT: PrivateChat, GROUP_CHAT: GroupChat, ENCRYPTED_PRIVATE_CHAT: EncryptedPrivateChat}
REVERSE_CHAT_TYPES = {value: key for key, value in CHAT_TYPES.items()}
CHAT_TYPE_TO_MESSAGE_TYPE = {PrivateChat: PrivateMessage, GroupChat: GroupMessage,
                             EncryptedPrivateChat: EncryptedPrivateMessage}

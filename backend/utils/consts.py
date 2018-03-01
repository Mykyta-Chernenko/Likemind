from chat.consts import PRIVATE_CHAT, GROUP_CHAT, ENCRYPTED_PRIVATE_CHAT, PRIVATE_MESSAGE, GROUP_MESSAGE, \
    ENCRYPTED_PRIVATE_MESSAGE
from chat.models import PrivateChat, GroupChat, EncryptedPrivateChat, PrivateMessage, GroupMessage, \
    EncryptedPrivateMessage
from files.consts import FILE_MESSAGE_FIELD, AUDIO_MESSAGE_FIELD, VIDEO_MESSAGE_FIELD, IMAGE_MESSAGE_FIELD, CHAT_FILE, \
    CHAT_AUDIO, CHAT_VIDEO, CHAT_IMAGE, CHAT_FILE_MESSAGE, CHAT_IMAGE_MESSAGE, CHAT_AUDIO_MESSAGE, CHAT_VIDEO_MESSAGE
from files.models import ChatFile, ChatVideo, ChatAudio, ChatImage

TIME_TZ_FORMAT = '%Y-%m-%dT%H:%M:%S.%fZ'

MODEL_FROM_FIELD = {FILE_MESSAGE_FIELD: ChatFile, AUDIO_MESSAGE_FIELD: ChatAudio,
                    VIDEO_MESSAGE_FIELD: ChatVideo, IMAGE_MESSAGE_FIELD: ChatImage}

MODEL_FROM_STRING = {PRIVATE_CHAT: PrivateChat, GROUP_CHAT: GroupChat, ENCRYPTED_PRIVATE_CHAT: EncryptedPrivateChat,
                     PRIVATE_MESSAGE: PrivateMessage, GROUP_MESSAGE: GroupMessage,
                     ENCRYPTED_PRIVATE_MESSAGE: EncryptedPrivateMessage,
                     CHAT_FILE: ChatFile, CHAT_AUDIO: ChatAudio, CHAT_VIDEO: ChatVideo, CHAT_IMAGE: ChatImage}

MODEl_FROM_MESSAGE = {CHAT_FILE_MESSAGE: ChatFile, CHAT_IMAGE_MESSAGE: ChatImage, CHAT_AUDIO_MESSAGE: ChatAudio,
                      CHAT_VIDEO_MESSAGE: ChatVideo}

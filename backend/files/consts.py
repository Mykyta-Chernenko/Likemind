from chat.consts import PRIVATE_CHAT, GROUP_CHAT, ENCRYPTED_PRIVATE_CHAT
from chat.models import PrivateChat, GroupChat, EncryptedPrivateChat
from files.models import ChatFile, ChatImage, ChatVideo, ChatAudio

CHAT_FILE_MESSAGE = 'chat-file-message'
CHAT_IMAGE_MESSAGE = 'chat-image-message'
CHAT_AUDIO_MESSAGE = 'chat-audio-message'
CHAT_VIDEO_MESSAGE = 'chat-video-message'


CHAT_DELETE_FILE_MESSAGE = 'chat-delete-file-message'
CHAT_DELETE_IMAGE_MESSAGE = 'chat-delete-image-message'
CHAT_DELETE_AUDIO_MESSAGE = 'chat-delete-audio-message'
CHAT_DELETE_VIDEO_MESSAGE = 'chat-delete-video-message'

FILE_MESSAGE_FIELD = ChatFile.get_field()
AUDIO_MESSAGE_FIELD = ChatAudio.get_field()
VIDEO_MESSAGE_FIELD = ChatVideo.get_field()
IMAGE_MESSAGE_FIELD = ChatImage.get_field()

CHAT_FILE = ChatFile.string_type()
CHAT_AUDIO = ChatAudio.string_type()
CHAT_VIDEO = ChatVideo.string_type()
CHAT_IMAGE = ChatImage.string_type()

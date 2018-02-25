from chat.consts import PRIVATE_CHAT, GROUP_CHAT, ENCRYPTED_PRIVATE_CHAT
from chat.models import PrivateChat, GroupChat, EncryptedPrivateChat
from files.models import ChatFile, ChatImage, ChatVideo, ChatAudio

FILE_MESSAGE_FIELD = ChatFile.file.field.name
AUDIO_MESSAGE_FIELD = ChatAudio.audio.field.name
VIDEO_MESSAGE_FIELD = ChatVideo.video.field.name
IMAGE_MESSAGE_FIELD = ChatImage.image.field.name
FILE_MODEL_FROM_FIELD = {FILE_MESSAGE_FIELD: ChatFile, AUDIO_MESSAGE_FIELD: ChatAudio,
                         VIDEO_MESSAGE_FIELD: ChatVideo, IMAGE_MESSAGE_FIELD: ChatImage}
CHAT_FILE_MESSAGE = 'chat-file-message'
CHAT_IMAGE_MESSAGE = 'chat-image-message'
CHAT_AUDIO_MESSAGE = 'chat-audio-message'
CHAT_VIDEO_MESSAGE = 'chat-video-message'
FILE_MODEL_FROM_MESSAGE = {CHAT_FILE_MESSAGE: ChatFile, CHAT_AUDIO_MESSAGE: ChatVideo, CHAT_IMAGE_MESSAGE: ChatImage,
                           CHAT_VIDEO_MESSAGE: ChatVideo}


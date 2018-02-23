from chat.consts import PRIVATE_CHAT, GROUP_CHAT, ENCRYPTED_PRIVATE_CHAT
from chat.models import PrivateChat, GroupChat, EncryptedPrivateChat
from files.models import ChatFile, ChatImage, ChatVideo, ChatAudio

FILE_MESSAGE_FIELD = ChatFile.file.field.name
AUDIO_MESSAGE_FIELD = ChatAudio.audio.field.name
VIDEO_MESSAGE_FIELD = ChatVideo.video.field.name
IMAGE_MESSAGE_FIELD = ChatImage.image.field.name
file_model_from_field = {FILE_MESSAGE_FIELD: ChatFile, AUDIO_MESSAGE_FIELD: ChatAudio,
                         VIDEO_MESSAGE_FIELD: ChatVideo, IMAGE_MESSAGE_FIELD: ChatImage}
CHAT_FILE_MESSAGE = 'chat-file-message'
CHAT_IMAGE_MESSAGE = 'chat-image-message'
CHAT_AUDIO_MESSAGE = 'chat-audio-message'
CHAT_VIDEO_MESSAGE = 'chat-video-message'
FILE_TYPES = {PRIVATE_CHAT: PrivateChat, GROUP_CHAT: GroupChat, ENCRYPTED_PRIVATE_CHAT: EncryptedPrivateChat}
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path,  include
from rest_framework.documentation import include_docs_urls

from backend import settings
urlpatterns = [
    path('admin/', admin.site.urls),
    path('docs/', include_docs_urls(title='LikeMind API', permission_classes=[])),
    path('api/', include('users.urls')),
    path('api/', include('chat.urls')),
    path('api/', include('files.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

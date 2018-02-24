from django.urls import path
from rest_framework_jwt.views import obtain_jwt_token
from users.views import UserListView, UserDetailView, SelfUserDetailView, FriendListView, activate_account

urlpatterns = [
        path('users/', UserListView.as_view(), name='user-list'),
        path('users/<int:pk>/', UserDetailView.as_view(), name='user-detail'),
        path('self-users/', SelfUserDetailView.as_view(), name='self-user-detail'),
        path('friends/', FriendListView.as_view(), name='friend-list'),
        path('activate-account/<str:activate_link>/', activate_account, name='activate-account'),
        path('obtain-jwt-token/', obtain_jwt_token, name='obtain-jwt-for-email-username-phone')
]

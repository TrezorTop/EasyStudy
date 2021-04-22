from django.urls import path
from .views import (
    my_profile_view,
    invites_received_view,
    friend_list_view,
    ProfileDetailView,
    ProfileListView,
    send_invitation,
    remove_from_friends,
    accept_invitation,
    reject_invitation,
)

app_name = 'profiles'

urlpatterns = [
    path('', ProfileListView.as_view(), name='all_profiles_view'),
    path('my_profile/', my_profile_view, name='my_profile_view'),
    path('my_invites/', invites_received_view, name='my_invites_view'),
    path('friends/', friend_list_view, name='friends_list_view'),
    path('send_invite/', send_invitation, name='send_invite'),
    path('remove_friend/', remove_from_friends, name='remove_friend'),
    path('<slug>/', ProfileDetailView.as_view(), name='profile_detail_view'),
    path('my_invites/accept', accept_invitation, name='accept_invite'),
    path('my_invites/reject', reject_invitation, name='reject_invite'),
]

from django.urls import path
from .views import (
    my_profile_view,
    invites_received_view,
    profiles_list_view,
    invite_profiles_list_view,
    ProfileListView
)

app_name = 'profiles'

urlpatterns = [
    path('myprofile/', my_profile_view, name='my_profile_view'),
    path('my_invites/', invites_received_view, name='my_invites_view'),
    path('all_profiles/', ProfileListView.as_view(), name='all_profiles_view'),
    path('to_invite/', invite_profiles_list_view, name='invite_profiles_list_view'),
]

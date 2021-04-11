from .models import Profile, Relationship


def profile_picture(request):
    if request.user.is_authenticated:
        profile_object = Profile.objects.get(user=request.user)
        picture = profile_object.avatar
        return {
            'picture': picture
        }
    return {}


def invitations_received_number(request):
    if request.user.is_authenticated:
        profile_object = Profile.objects.get(user=request.user)
        query_set_count = Relationship.objects.invitations_received(profile_object).count()
        return {
            'invites_number': query_set_count
        }
    return {}

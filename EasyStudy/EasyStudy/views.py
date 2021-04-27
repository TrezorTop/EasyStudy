from django.http import HttpResponse
from django.shortcuts import render
from profiles.models import Profile
from posts.models import Post


def home_view(request):
    user = request.user
    profile = Profile.objects.get(user=user)
    subscriptions = profile.get_subscriptions()

    context = {
        'posts': ''
    }

    return render(request, 'main/home.html', context)

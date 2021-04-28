from django.http import HttpResponse
from django.shortcuts import render
from profiles.models import Profile
from posts.models import Post


def home_view(request):
    user = request.user
    context = {
        'posts': ''
    }

    return render(request, 'main/home.html', context)

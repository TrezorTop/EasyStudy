from django.http import HttpResponse
from django.shortcuts import render
from profiles.models import Profile
from posts.models import Post
from posts.forms import CommentModelForm
from django.contrib.auth.decorators import login_required


def home_view(request):
    user = request.user
    if request.user.is_authenticated:
        profile = Profile.objects.get(user=request.user)
        posts = Post.objects.filter(author__in=profile.get_subscriptions())
        context = {
            'profile': profile,
            'posts': posts
        }
    else:
        context = {'test': 'test'}

    return render(request, 'main/home.html', context)


@login_required
def post_comment_create_and_list_view(request):
    user = request.user
    if request.user.is_authenticated:
        profile = Profile.objects.get(user=request.user)
        query_set = Post.objects.filter(author__in=profile.get_subscriptions())

        comment_form = CommentModelForm()

        if 'submit_comment_form' in request.POST:
            comment_form = CommentModelForm(request.POST)
            if comment_form.is_valid():
                instance = comment_form.save(commit=False)
                instance.user = profile
                instance.post = Post.objects.get(id=request.POST.get('post_id'))
                instance.save()
                comment_form = CommentModelForm()

        context = {
            'query_set': query_set,
            'profile': profile,
            'comment_form': comment_form,
        }

    else:
        context = {'test': 'test'}

    return render(request, 'main/home.html', context)

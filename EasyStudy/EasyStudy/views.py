from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import render
from posts.forms import CommentModelForm
from posts.models import Post
from profiles.models import Profile


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
        friends = profile.get_friends()
        query_set = Post.objects.filter(Q(author__in=profile.get_subscriptions()) | Q(
            author__in=Profile.objects.filter(user__in=friends)))

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

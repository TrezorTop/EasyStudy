from django.shortcuts import render, redirect
from .models import Post, Like
from profiles.models import Profile


def post_comment_create_and_list_view(request):
    query_set = Post.objects.all()
    profile = Profile.objects.get(user=request.user)

    context = {
        'query_set': query_set,
        'profile': profile,
    }

    return render(request, 'posts/main.html', context)


def like_unlike_post(request):
    user = request.user
    if request.method == 'POST':
        post_id = request.POST.get('post_id')
        post_object = Post.objects.get(id=post_id)
        profile = Profile.objects.get(user=user)

        if profile in post_object.liked.all():
            post_object.liked.remove(profile)
        else:
            post_object.liked.add(profile)

        like, created = Like.objects.get_or_create(user=profile, post_id=post_id)

        if not created:
            if Like.value == 'Like':
                like.value = 'Unlike'
            else:
                like.value = 'Like'
        else:
            like.value = 'Like'

            post_object.save()
            like.save()

    return redirect('posts:main_post_view')

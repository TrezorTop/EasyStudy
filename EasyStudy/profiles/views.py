from django.shortcuts import render, redirect, get_object_or_404
from .models import Profile, Relationship
from .forms import ProfileModelForm
from django.views.generic import ListView, DetailView
from django.contrib.auth.models import User
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse, HttpResponseRedirect
from documents.models import File
from posts.forms import CommentModelForm
from posts.models import Post


@login_required
def my_profile_view(request):
    profile = Profile.objects.get(user=request.user)
    form = ProfileModelForm(request.POST or None, request.FILES or None, instance=profile)
    confirm = False

    if request.method == 'POST':
        if form.is_valid():
            form.save()
            confirm = True

    context = {
        'profile': profile,
        'form': form,
        'confirm': confirm,
    }

    return render(request, 'profiles/myprofile.html', context)


@login_required
def invites_received_view(request):
    profile = Profile.objects.get(user=request.user)
    query_set = Relationship.objects.invitations_received(profile)
    results = list(map(lambda x: x.sender, query_set))
    is_empty = False
    if len(results) == 0:
        is_empty = True

    context = {
        'query_set': results,
        'is_empty': is_empty,
    }

    return render(request, 'profiles/my_invites.html', context)


@login_required
def accept_invitation(request):
    if request.method == "POST":
        pk = request.POST.get('profile_pk')
        sender = Profile.objects.get(pk=pk)
        receiver = Profile.objects.get(user=request.user)
        relation = get_object_or_404(Relationship, sender=sender, receiver=receiver)
        if relation.status == 'send':
            relation.status = 'accepted'
            relation.save()
    return redirect('profiles:my_invites_view')


@login_required
def reject_invitation(request):
    if request.method == "POST":
        pk = request.POST.get('profile_pk')
        sender = Profile.objects.get(pk=pk)
        receiver = Profile.objects.get(user=request.user)
        relation = get_object_or_404(Relationship, sender=sender, receiver=receiver)
        relation.delete()
    return redirect('profiles:my_invites_view')


@login_required
def friend_list_view(request):
    user = request.user
    query_set = Profile.objects.get(user=user)

    context = {'query_set': query_set}

    return render(request, 'profiles/to_invite.html', context)


@login_required
def profiles_list_view(request):
    user = request.user
    query_set = Profile.objects.get_all_profiles(user)

    context = {'query_set': query_set}

    return render(request, 'profiles/profile_list.html', context)


def search_results(request):
    if request.is_ajax():
        res = None
        profile_name = request.POST.get('profile')
        query_set = Profile.objects.filter(
            Q(first_name__icontains=profile_name) | Q(last_name__icontains=profile_name) | Q(
                user__username__icontains=profile_name))

        if len(query_set) > 0 and len(profile_name) > 0:
            data = []
            for pos in query_set:
                item = {
                    'slug': pos.slug,
                    'first_name': pos.first_name,
                    'last_name': pos.last_name,
                    'user': pos.user.username,
                    'image': str(pos.avatar.url),
                }
                data.append(item)
                res = data

        else:
            res = 'No profiles found'

        return JsonResponse(
            {
                'data': res
            }
        )


def search_list_results(request):
    profile_name = request.GET.get('profile_search')

    if profile_name:
        profiles = Profile.objects.filter(
            Q(first_name__icontains=profile_name) | Q(last_name__icontains=profile_name) | Q(
                user__username__icontains=profile_name))
    else:
        return redirect('profiles:all_profiles_view')

    context = {
        'query_set': profiles
    }

    return render(request, 'profiles/profile_list.html', context)


class ProfileDetailView(LoginRequiredMixin, DetailView):
    model = Profile
    template_name = 'profiles/detail.html'
    comment_form = CommentModelForm

    def get_object(self, queryset=None):
        slug = self.kwargs.get('slug')
        profile = Profile.objects.get(slug=slug)

        return profile

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        user = User.objects.get(username__iexact=self.request.user)
        profile = Profile.objects.get(user=user)
        relation_receiver = Relationship.objects.filter(sender=profile)
        relation_sender = Relationship.objects.filter(receiver=profile)
        files = File.objects.filter(author=self.get_object())[:5]

        relation_receiver_listed = []
        relation_sender_listed = []
        subs_listed = []

        for item in relation_receiver:
            relation_receiver_listed.append(item.receiver.user)

        for item in relation_sender:
            relation_sender_listed.append(item.sender.user)

        for item in profile.get_subscriptions():
            subs_listed.append(item.user)

        context["subs"] = subs_listed
        context["relation_receiver"] = relation_receiver_listed
        context["relation_sender"] = relation_sender_listed
        context["comment_form"] = self.comment_form
        context["posts"] = self.get_object().get_all_author_posts()
        context["len_posts"] = True if len(self.get_object().get_all_author_posts()) > 0 else False
        context["files"] = files

        return context

    def post(self, request, *args, **kwargs):
        comment_form = self.comment_form(request.POST)
        if comment_form.is_valid():
            profile = Profile.objects.get(user=request.user)

            instance = comment_form.save(commit=False)
            instance.user = profile
            instance.post = Post.objects.get(id=request.POST.get('post_id'))
            instance.save()

        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


class ProfileListView(LoginRequiredMixin, ListView):
    model = Profile
    template_name = 'profiles/profile_list.html'

    context_object_name = 'query_set'

    def get_queryset(self):
        query_set = Profile.objects.get_all_profiles(self.request.user)
        return query_set

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        user = User.objects.get(username__iexact=self.request.user)
        profile = Profile.objects.get(user=user)
        relation_receiver = Relationship.objects.filter(sender=profile)
        relation_sender = Relationship.objects.filter(receiver=profile)

        relation_receiver_listed = []
        relation_sender_listed = []

        for item in relation_receiver:
            relation_receiver_listed.append(item.receiver.user)

        for item in relation_sender:
            relation_sender_listed.append(item.sender.user)

        context["relation_receiver"] = relation_receiver_listed
        context["relation_sender"] = relation_sender_listed
        context['is_empty'] = False

        if len(self.get_queryset()) == 0:
            context['is_empty'] = True

        return context


@login_required
def follow_profile(request):
    if request.method == 'POST':
        pk = request.POST.get('profile_pk')
        profile = Profile.objects.get(user=request.user)
        profile_to_follow = Profile.objects.get(pk=pk)
        if profile_to_follow not in profile.get_subscriptions():
            profile.subscriptions.add(profile_to_follow)
        else:
            profile.subscriptions.remove(profile_to_follow)
        return redirect(request.META.get('HTTP_REFERER'))

    return redirect('profiles:my_profile_view')


@login_required
def send_invitation(request):
    if request.method == 'POST':
        pk = request.POST.get('profile_pk')
        user = request.user
        sender = Profile.objects.get(user=user)
        receiver = Profile.objects.get(pk=pk)

        relation = Relationship.objects.create(sender=sender, receiver=receiver, status='send')

        return redirect(request.META.get('HTTP_REFERER'))
    return redirect('profiles:my_profile_view')


@login_required
def remove_from_friends(request):
    if request.method == 'POST':
        pk = request.POST.get('profile_pk')
        user = request.user
        sender = Profile.objects.get(user=user)
        receiver = Profile.objects.get(pk=pk)

        relation = Relationship.objects.get(
            (Q(sender=sender) & Q(receiver=receiver)) | (Q(sender=receiver) & Q(receiver=sender))
        )
        relation.delete()
        return redirect(request.META.get('HTTP_REFERER'))
    return redirect('profiles:my_profile_view')

from django.shortcuts import render, redirect
from .models import Profile, Relationship
from .forms import ProfileModelForm
from django.views.generic import ListView
from django.contrib.auth.models import User
from django.db.models import Q


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


def invites_received_view(request):
    profile = Profile.objects.get(user=request.user)
    query_set = Relationship.objects.invitations_received(profile)

    context = {'query_set': query_set}

    return render(request, 'profiles/my_invites.html', context)


def invite_profiles_list_view(request):
    user = request.user
    query_set = Profile.objects.get_all_profiles_to_invite(user)

    context = {'query_set': query_set}

    return render(request, 'profiles/to_invite.html', context)


def profiles_list_view(request):
    user = request.user
    query_set = Profile.objects.get_all_profiles(user)

    context = {'query_set': query_set}

    return render(request, 'profiles/profile_list.html', context)


class ProfileListView(ListView):
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


def send_invitation(request):
    if request.method == 'POST':
        pk = request.POST.get('profile_pk')
        user = request.user
        sender = Profile.objects.get(user=user)
        receiver = Profile.objects.get(pk=pk)

        relation = Relationship.objects.create(sender=sender, receiver=receiver, status='send')

        return redirect(request.META.get('HTTP_REFERER'))
    return redirect('profiles:my_profile_view')


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

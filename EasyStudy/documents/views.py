from django.shortcuts import render, redirect
from .forms import FileForm, CategoryForm
from .models import Profile, File, Category
from django.views.generic import ListView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.urls import reverse_lazy


def file_upload(request):
    if request.method == 'POST':
        form = FileForm(request.POST, request.FILES)
        if form.is_valid():
            user = User.objects.get(username__iexact=request.user)
            profile = Profile.objects.get(user=user)

            instance = form.save(commit=False)
            instance.author = profile
            instance.save()

            return redirect('documents:file_list')
    else:
        form = FileForm()
    return render(request, 'documents/file_upload.html', {
        'form': form
    })


def file_list(request):
    user = User.objects.get(username__iexact=request.user)
    profile = Profile.objects.get(user=user)
    categories = Category.objects.filter(profile=profile).order_by('-created_at')

    files = File.objects.filter(author=profile)
    return render(request, 'documents/file_list.html', {
        'files': files,
        'categories': categories
    })


def file_delete(request, pk):
    if request.method == 'POST':
        file = File.objects.get(pk=pk)
        file.delete()
        return redirect('documents:file_list')


def category_create(request):
    user = User.objects.get(username__iexact=request.user)
    profile = Profile.objects.get(user=user)
    categories = Category.objects.filter(profile=profile).order_by('-created_at')
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            user = User.objects.get(username__iexact=request.user)
            profile = Profile.objects.get(user=user)

            instance = form.save(commit=False)
            instance.profile = profile
            instance.save()

            return redirect('documents:category_create')
    else:
        form = CategoryForm()
    context = {
        'categories': categories,
        'form': form
    }
    return render(request, 'documents/category_create.html', context)


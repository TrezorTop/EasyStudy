from django.shortcuts import render, redirect
from .forms import FileForm, CategoryAddForm, FileCategoryForm, CreateFileCategoryForm
from .models import Profile, File, Category
from django.contrib.auth.models import User


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


def file_list(request, *args, **kwargs):
    user = User.objects.get(username__iexact=request.user)
    profile = Profile.objects.get(user=user)
    categories = Category.objects.filter(profile=profile).order_by('-created_at')

    files = File.objects.filter(author=profile)

    return render(request, 'documents/file_list.html', {
        'files': files,
        'categories': categories,
    })


def file_details(request, pk, *args, **kwargs):
    user = User.objects.get(username__iexact=request.user)
    profile = Profile.objects.get(user=user)

    file = File.objects.get(pk=pk)
    form = CreateFileCategoryForm(request.POST or None, profile=profile, instance=file)
    confirm = False

    if request.method == 'POST':
        if form.is_valid():
            form.save()
            confirm = True

            return redirect('documents:file_list')

    context = {
        'file': file,
        'form': form,
        'confirm': confirm
    }
    return render(request, 'documents/file_details.html', context)


def file_delete(request, pk):
    if request.method == 'POST':
        file = File.objects.get(pk=pk)
        file.delete()
        return redirect('documents:file_list')


# def file_category_add(request, pk):
#     if request.method == 'POST':
#         form = FileCategoryForm(request.POST)
#         if form.is_valid():
#             instance = form.save(commit=False)
#             instance.save()
#
#             return redirect('documents:file_list')
#     else:
#         form = FileCategoryForm()
#     context = {
#         'form': form
#     }


def category_create(request):
    user = User.objects.get(username__iexact=request.user)
    profile = Profile.objects.get(user=user)
    categories = Category.objects.filter(profile=profile).order_by('-created_at')
    if request.method == 'POST':
        form = CategoryAddForm(request.POST)
        if form.is_valid():
            user = User.objects.get(username__iexact=request.user)
            profile = Profile.objects.get(user=user)

            instance = form.save(commit=False)
            instance.profile = profile
            instance.save()

            return redirect('documents:category_create')
    else:
        form = CategoryAddForm()
    context = {
        'categories': categories,
        'form': form
    }
    return render(request, 'documents/category_create.html', context)

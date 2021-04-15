from django.shortcuts import render, redirect
from django.core.files.storage import FileSystemStorage
from django.contrib.auth.decorators import login_required
from .forms import FileForm
from .models import Profile, File
from django.views.generic import ListView


@login_required
def upload(request):
    context = {}
    if request.method == 'POST':
        uploaded_file = request.FILES['document']
        file_storage = FileSystemStorage()
        name = file_storage.save(uploaded_file.name, uploaded_file)
        url = file_storage.url(name)
        context['url'] = file_storage.url(name)
    return render(request, 'upload/upload.html', context)


def file_list(request):
    profile = Profile.objects.get(user=request.user)
    files = File.objects.filter(author=profile)

    context = {
        'files': files
    }
    return render(request, 'file_list.html', context)


@login_required
def file_upload(request):
    profile = Profile.objects.get(user=request.user)

    if request.method == 'POST':
        file_form = FileForm(request.POST, request.FILES)
        if file_form.is_valid():
            instance = file_form.save(commit=False)
            instance.author = profile
            instance.save()
            return redirect('documents:file_list')
    else:
        file_form = FileForm()

    context = {
        'form': file_form
    }
    return render(request, 'file_upload.html', context)


class FileListView(ListView):
    model = File
    template_name = 'file_list.html'
    context_object_name = 'files'

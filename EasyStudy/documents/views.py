from django.shortcuts import render, redirect
from django.core.files.storage import FileSystemStorage
from django.contrib.auth.decorators import login_required
from .forms import FileForm
from .models import Profile, File
from django.views.generic import ListView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.urls import reverse_lazy


# @login_required
# def upload(request):
#     context = {}
#     if request.method == 'POST':
#         uploaded_file = request.FILES['document']
#         file_storage = FileSystemStorage()
#         name = file_storage.save(uploaded_file.name, uploaded_file)
#         url = file_storage.url(name)
#         context['url'] = file_storage.url(name)
#     return render(request, 'upload/upload.html', context)


# @login_required
# def file_upload(request):
#     profile = Profile.objects.get(user=request.user)
#
#     if request.method == 'POST':
#         file_form = FileForm(request.POST, request.FILES)
#         if file_form.is_valid():
#             instance = file_form.save(commit=False)
#             instance.author = profile
#             instance.save()
#             return redirect('documents:file_list')
#     else:
#         file_form = FileForm()
#
#     context = {
#         'form': file_form
#     }
#     return render(request, 'file_upload.html', context)

def file_delete(request, pk):
    if request.method == 'POST':
        file = File.objects.get(pk=pk)
        file.delete()
        return redirect('documents:file_list')


class FileListView(LoginRequiredMixin, ListView):
    model = File
    queryset = File.objects.all().order_by('-created_at')
    template_name = 'file_list.html'
    context_object_name = 'files'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(FileListView, self).get_context_data(**kwargs)
        context['user_files'] = self.get_user_files()
        return context

    def get_user_files(self):
        user = User.objects.get(username__iexact=self.request.user)
        profile = Profile.objects.get(user=user)
        return super(FileListView, self).get_queryset().filter(author=profile)


class FileUploadView(LoginRequiredMixin, CreateView):
    model = File
    form_class = FileForm
    success_url = reverse_lazy('file_list')
    template_name = 'file_upload.html'

    def form_valid(self, form):
        user = User.objects.get(username__iexact=self.request.user)
        profile = Profile.objects.get(user=user)

        self.instance = form.save(commit=False)
        self.instance.author = profile
        self.instance.save()

        return redirect('documents:file_list')

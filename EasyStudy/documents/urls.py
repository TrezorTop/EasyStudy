from django.urls import path
from .views import *

app_name = 'documents'

urlpatterns = [
    path('', upload, name='upload_file'),
    path('files', file_list, name='file_list'),
    path('files/upload', file_upload, name='file_upload'),

    path('class/files', FileListView.as_view(), name='class_file_list'),
]

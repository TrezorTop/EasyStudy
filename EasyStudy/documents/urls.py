from django.urls import path
from .views import *

app_name = 'documents'

urlpatterns = [
    path('', FileListView.as_view(), name='file_list'),
    path('upload', FileUploadView.as_view(), name='file_upload'),
    path('delete/<int:pk>', file_delete, name='file_delete'),
]

from django.urls import path
from .views import *

app_name = 'documents'

urlpatterns = [
    path('', file_list, name='file_list'),
    path('upload', file_upload, name='file_upload'),
    path('delete/<int:pk>', file_delete, name='file_delete'),
    path('category_create', category_create, name='category_create'),
]

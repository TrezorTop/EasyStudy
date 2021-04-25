from django.urls import path
from .views import *

app_name = 'documents'

urlpatterns = [
    path('', file_list, name='file_list'),
    path('upload', file_upload, name='file_upload'),
    path('delete/<int:pk>', file_delete, name='file_delete'),
    path('<int:pk>', file_details, name='file_details'),
    # path('category/add/<int:pk>', file_category_add, name='file_category_add'),
    path('category/create', category_create, name='category_create'),
]

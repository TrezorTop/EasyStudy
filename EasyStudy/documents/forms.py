from django import forms
from .models import File, Category


class FileForm(forms.ModelForm):
    class Meta:
        model = File
        fields = ('title', 'user_file')


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ('title',)

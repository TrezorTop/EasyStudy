from django import forms
from django.contrib.auth.models import User

from .models import File, Category


class FileForm(forms.ModelForm):
    class Meta:
        model = File
        fields = ('title', 'user_file',)


class FileCategoryForm(forms.ModelForm):
    class Meta:
        model = File
        fields = ('category',)


class CreateFileCategoryForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        self.profile = kwargs.get('profile', None)
        del kwargs['profile']
        super(CreateFileCategoryForm, self).__init__(*args, **kwargs)
        self.fields["category"].queryset = Category.objects.filter(profile=self.profile)

    class Meta:
        model = File
        fields = ('title', 'category')

    category = forms.ModelMultipleChoiceField(
        queryset=Category.objects.all(),
        widget=forms.CheckboxSelectMultiple
    )


class CategoryAddForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ('title',)

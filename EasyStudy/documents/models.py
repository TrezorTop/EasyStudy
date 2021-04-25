from django.db import models
from profiles.models import Profile


class File(models.Model):
    title = models.CharField(max_length=128, blank=True, default=None)
    user_file = models.FileField(upload_to='documents/files/')
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(Profile, on_delete=models.CASCADE)
    category = models.ManyToManyField('Category', blank=True)

    def __str__(self):
        return self.title

    def delete(self, *args, **kwargs):
        self.user_file.delete()
        super().delete(*args, **kwargs)

    def get_category(self):
        return self.category.all()


class Category(models.Model):
    title = models.CharField(max_length=128, db_index=True)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

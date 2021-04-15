from django.db import models
from profiles.models import Profile


class File(models.Model):
    title = models.CharField(max_length=128)
    user_file = models.FileField(upload_to='documents/files/')
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(Profile, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

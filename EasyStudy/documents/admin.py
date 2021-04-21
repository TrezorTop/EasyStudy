from django.contrib import admin
from .models import File


class FileAdmin(admin.ModelAdmin):
    list_display = ('title', 'user_file', 'updated_at', 'created_at', 'author')
    search_fields = ('title',)
    list_filter = ('author',)


admin.site.register(File, FileAdmin)

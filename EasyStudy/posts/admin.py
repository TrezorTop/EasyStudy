from django.contrib import admin
from .models import Post, Comment, Like


class PostAdmin(admin.ModelAdmin):
    list_display = ('content', 'image', 'author', 'created', 'updated')
    search_fields = ('content',)
    list_filter = ('author',)


class CommentAdmin(admin.ModelAdmin):
    list_display = ('user', 'post', 'body', 'created', 'updated')
    search_fields = ('body',)
    list_filter = ('user',)


class LikeAdmin(admin.ModelAdmin):
    list_display = ('user', 'post', 'value', 'updated', 'created')


admin.site.register(Post, PostAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Like, LikeAdmin)

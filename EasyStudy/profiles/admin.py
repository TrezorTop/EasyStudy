from django.contrib import admin

from .models import Profile, Relationship


class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'first_name', 'last_name', 'bio', 'email', 'slug', 'created', 'updated')
    search_fields = ('user', 'first_name', 'last_name')


class RelationshipAdmin(admin.ModelAdmin):
    list_display = ('sender', 'receiver', 'status', 'created', 'updated')
    search_fields = ('user', 'first_name', 'last_name')


admin.site.register(Profile, ProfileAdmin)
admin.site.register(Relationship, RelationshipAdmin)

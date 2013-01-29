from django.contrib import admin
from profiles.models import UserProfile


class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'profile_photo')
    search_fields = ('user__username',)

admin.site.register(UserProfile, UserProfileAdmin)


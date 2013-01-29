from django.contrib import admin
from profiles.models import UserProfile, SocialLink


class SocialLinkInline(admin.TabularInline):
    model = SocialLink


class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'profile_photo')
    search_fields = ('user__username',)
    inlines = [SocialLinkInline]

admin.site.register(UserProfile, UserProfileAdmin)


from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin

from profiles.models import UserProfile, SocialLink


class SocialLinkInline(admin.TabularInline):
    model = SocialLink


class NewUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'date_joined', 'profile_photo')

    def profile_photo(self, obj):
        return obj.userprofile.profile_photo

class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'user_email', 'user_full_name', 'user_date_joined', 'profile_photo')
    search_fields = ('user__username',)
    ordering = ('-user__date_joined',)
    inlines = [SocialLinkInline]

    def user_email(self, obj):
        return obj.user.email

    def user_full_name(self, obj):
        return obj.user.get_full_name()

    def user_date_joined(self, obj):
        return obj.user.date_joined

admin.site.unregister(User)
admin.site.register(User, NewUserAdmin)

admin.site.register(UserProfile, UserProfileAdmin)


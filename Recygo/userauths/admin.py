from django.contrib import admin
from userauths.models import User, Profile

class UserAdmin(admin.ModelAdmin):
    search_fields  = ['username', 'email']
    list_display = ['username', 'email']
    list_per_page = 100

class ProfileAdmin(admin.ModelAdmin):
    search_fields  = ['user__username', 'full_name', 'user__email']
    list_display = ['user', 'full_name', 'profile_image']
    list_per_page = 100


admin.site.register(User, UserAdmin)
admin.site.register(Profile, ProfileAdmin)
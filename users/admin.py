from django.contrib import admin

from users.models import User


class UserAdmin(admin.ModelAdmin):
    list_display = ['email', 'id','full_name']


admin.site.register(User, UserAdmin)

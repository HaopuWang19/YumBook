from django.contrib import admin
from yum.models import User

class UserAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("username",)}

admin.site.register(User, UserAdmin)

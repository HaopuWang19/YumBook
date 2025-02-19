from django.contrib import admin
from yum.models import User

class UserAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}

admin.site.register(User, UserAdmin)

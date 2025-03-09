from django.contrib import admin
from django.contrib.auth.models import User

from yum.models import *


class UserAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("username",)}

admin.site.register(UserProfile)
admin.site.register(Cuisine)
admin.site.register(MealType)
admin.site.register(Recipe)
admin.site.register(Comment)
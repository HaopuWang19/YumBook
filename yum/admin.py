from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User

from yum.models import *


class UserAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("username",)}

class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'email', 'is_staff', 'is_active')

class CuisineAdmin(admin.ModelAdmin):
    list_display = ('cuisine_id', 'name')

class MealTypeAdmin(admin.ModelAdmin):
    list_display = ('meal_type_id', 'name')

admin.site.register(User, CustomUserAdmin)
admin.site.register(Cuisine, CuisineAdmin)
admin.site.register(MealType, MealTypeAdmin)
admin.site.register(Recipe)
admin.site.register(Comment)
admin.site.register(RecipeImage)
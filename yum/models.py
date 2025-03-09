from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, User
from django.db import models
from django.template.defaultfilters import slugify


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='userprofile')
    slug = models.SlugField(unique=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.user.username)
        super(UserProfile, self).save(*args, **kwargs)

    def __str__(self):
        return self.user.username


class Cuisine(models.Model):
    cuisine_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name

class MealType(models.Model):
    meal_type_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name

class Recipe(models.Model):
    recipe_id = models.AutoField(primary_key=True)
    author = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    cuisine = models.ManyToManyField(Cuisine)
    meal_type = models.ManyToManyField(MealType)
    ingredients = models.TextField(max_length=200)
    title = models.TextField(max_length=100)
    post_date = models.DateTimeField(auto_now_add=True)
    images = models.ImageField(upload_to='recipe_images', blank=True)
    description = models.TextField(max_length=10000)

    def __str__(self):
        return self.title

    def comment_count(self):
        return self.comments.count()

class Comment(models.Model):
    comment_id = models.AutoField(primary_key=True)
    author = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    recipe_id = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name='comments')
    created_at = models.DateTimeField(auto_now_add=True)
    text = models.TextField(max_length=200)

    def __str__(self):
        return self.text

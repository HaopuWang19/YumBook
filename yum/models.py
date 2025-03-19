from django.contrib.auth.models import AbstractUser
from django.db import models
from django.template.defaultfilters import slugify


class User(AbstractUser):
    slug = models.SlugField(unique=True, blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.username)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.username


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
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    cuisine = models.ManyToManyField(Cuisine)   # A recipe can belong to multiple cuisines.
    meal_type = models.ManyToManyField(MealType)    # A recipe can be suitable for multiple meal types.
    ingredients = models.TextField(max_length=200)
    title = models.TextField(max_length=100)
    post_date = models.DateTimeField(auto_now_add=True)
    description = models.TextField(max_length=10000)

    def __str__(self):
        return self.title

    def comment_count(self):
        return self.comments.count()

class Comment(models.Model):
    comment_id = models.AutoField(primary_key=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    # Link to Recipe with related_name 'comments'
    recipe_id = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name='comments')
    created_at = models.DateTimeField(auto_now_add=True)
    text = models.TextField(max_length=200)

    def __str__(self):
        return self.text

class RecipeImage(models.Model):
    # Link image to Recipe with related_name 'images'
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='recipe_images/')
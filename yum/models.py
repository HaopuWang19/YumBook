from django.db import models

# Create your models here.
from django.db import models
from django.template.defaultfilters import slugify

class User(models.Model):
    user_id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=20)
    password = models.CharField(max_length=20)
    email = models.EmailField(unique=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.username)
        super(User, self).save(*args, **kwargs)

    def __str__(self):
        return self.user_id


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
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    cuisine_id = models.ForeignKey(Cuisine, on_delete=models.CASCADE)
    meal_type_id = models.ForeignKey(MealType, on_delete=models.CASCADE)
    ingredients = models.TextField(max_length=200)
    title = models.TextField(max_length=100)
    post_date = models.DateTimeField(auto_now_add=True)
    description = models.TextField(max_length=10000)

    def __str__(self):
        return self.title

class Comment(models.Model):
    comment_id = models.AutoField(primary_key=True)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    recipe_id = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    text = models.TextField(max_length=200)

    def __str__(self):
        return self.text

# tests/test_models.py

from django.test import TestCase
from yum.models import User, Cuisine, MealType, Recipe, Comment

class UserModelTest(TestCase):
    def test_slug_is_set_on_save(self):
        user = User.objects.create(username="TestUser", email="test@example.com")
        self.assertEqual(user.slug, "testuser")
        
    def test_user_str(self):
        user = User.objects.create(username="TestUser")
        self.assertEqual(str(user), "TestUser")

class CuisineModelTest(TestCase):
    def test_cuisine_str(self):
        cuisine = Cuisine.objects.create(name="Italian")
        self.assertEqual(str(cuisine), "Italian")

class MealTypeModelTest(TestCase):
    def test_meal_type_str(self):
        meal = MealType.objects.create(name="Lunch")
        self.assertEqual(str(meal), "Lunch")
        
class RecipeModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create(username="Author", email="author@example.com")
        self.cuisine = Cuisine.objects.create(name="Italian")
        self.meal_type = MealType.objects.create(name="Dinner")
        self.recipe = Recipe.objects.create(
            author=self.user,
            ingredients="Tomato, Pasta",
            title="Pasta",
            description="Cook pasta with tomato sauce."
        )
        self.recipe.cuisine.add(self.cuisine)
        self.recipe.meal_type.add(self.meal_type)
        
    def test_recipe_str(self):
        self.assertEqual(str(self.recipe), "Pasta")
        
    def test_comment_count(self):
        # The initial number of reviews should be 0
        self.assertEqual(self.recipe.comment_count(), 0)
        # The number should be updated after adding comments
        Comment.objects.create(
            author=self.user,
            recipe_id=self.recipe,
            text="Great recipe!"
        )
        self.assertEqual(self.recipe.comment_count(), 1)
        
class CommentModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create(username="Commenter")
        self.recipe = Recipe.objects.create(
            author=self.user,
            ingredients="Eggs, Flour",
            title="Pancakes",
            description="Mix ingredients and fry."
        )
        
    def test_comment_str(self):
        comment = Comment.objects.create(author=self.user, recipe_id=self.recipe, text="Delicious!")
        self.assertEqual(str(comment), "Delicious!")

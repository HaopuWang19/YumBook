# tests/test_views.py

from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from yum.models import Recipe, Cuisine, MealType, Comment

User = get_user_model()

class ViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username="testuser", password="secret")
        # Create the Cuisine and MealType objects for the RecipeForm
        self.cuisine = Cuisine.objects.create(name="Italian")
        self.meal_type = MealType.objects.create(name="Dinner")
        # Create a Recipe for detailing, editing, and deleting tests
        self.recipe = Recipe.objects.create(
            author=self.user,
            ingredients="Tomato, Pasta",
            title="Test Pasta",
            description="Cook pasta in tomato sauce."
        )
        self.recipe.cuisine.add(self.cuisine)
        self.recipe.meal_type.add(self.meal_type)
        
    def test_index_view(self):
        response = self.client.get(reverse('yum:index'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'yum/index.html')
        
    def test_about_view(self):
        response = self.client.get(reverse('yum:about'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'yum/about.html')
        
    def test_contact_view(self):
        response = self.client.get(reverse('yum:contact'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'yum/contact.html')
        
    def test_add_recipe_view_get(self):
        self.client.login(username="testuser", password="secret")
        response = self.client.get(reverse('yum:add_recipe'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'yum/addRecipe.html')
        
    def test_add_recipe_view_post(self):
        self.client.login(username="testuser", password="secret")
        post_data = {
            'title': 'New Recipe',
            'ingredients': 'Ingredient1, Ingredient2',
            'description': 'Recipe description',
            'cuisine': [self.cuisine.pk],
            'meal_type': [self.meal_type.pk],
        }
        response = self.client.post(reverse('yum:add_recipe'), data=post_data)
        # Redirect on successful commit (status code 302)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Recipe.objects.filter(title='New Recipe').exists())
        
    def test_profile_view(self):
        response = self.client.get(reverse('yum:profile', kwargs={'user_id': self.user.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'yum/profile.html')
        
    def test_login_page_get(self):
        response = self.client.get(reverse('yum:login'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'yum/login.html')
        
    def test_register_view_post(self):
        post_data = {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password': 'secret123',
            'confirm_password': 'secret123'
        }
        response = self.client.post(reverse('yum:register'), data=post_data)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(User.objects.filter(username='newuser').exists())
        
    def test_logout_page(self):
        self.client.login(username="testuser", password="secret")
        response = self.client.get(reverse('yum:logout'))
        self.assertEqual(response.status_code, 302)
        # Log out and visit the index page to check if the user is anonymous
        response = self.client.get(reverse('yum:index'))
        self.assertFalse(response.context.get('user').is_authenticated)
        
    def test_detail_view_get(self):
        response = self.client.get(reverse('yum:detail', kwargs={'recipe_id': self.recipe.recipe_id}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'yum/detail.html')
        
    def test_detail_view_post_comment(self):
        self.client.login(username="testuser", password="secret")
        post_data = {'text': 'Great recipe!'}
        response = self.client.post(reverse('yum:detail', kwargs={'recipe_id': self.recipe.recipe_id}), data=post_data)
        self.assertEqual(response.status_code, 302)
        # Check if the comment was created successfully
        self.assertEqual(self.recipe.comment_count(), 1)
        
    def test_edit_recipe_view_get(self):
        self.client.login(username="testuser", password="secret")
        response = self.client.get(reverse('yum:edit_recipe', kwargs={'recipe_id': self.recipe.recipe_id}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'yum/addRecipe.html')
        
    def test_edit_recipe_view_post(self):
        self.client.login(username="testuser", password="secret")
        post_data = {
            'title': 'Updated Recipe',
            'ingredients': 'Updated ingredients',
            'description': 'Updated description',
            'cuisine': [self.cuisine.pk],
            'meal_type': [self.meal_type.pk],
        }
        response = self.client.post(reverse('yum:edit_recipe', kwargs={'recipe_id': self.recipe.recipe_id}), data=post_data)
        self.assertEqual(response.status_code, 302)
        self.recipe.refresh_from_db()
        self.assertEqual(self.recipe.title, 'Updated Recipe')
        
    def test_delete_recipe_view(self):
        self.client.login(username="testuser", password="secret")
        response = self.client.get(reverse('yum:delete_recipe', kwargs={'recipe_id': self.recipe.recipe_id}))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Recipe.objects.filter(recipe_id=self.recipe.recipe_id).exists())

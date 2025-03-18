# tests/test_forms.py

from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile
from yum.forms import FileFieldForm, UserForm, LoginForm, RecipeForm, CommentForm
from yum.models import User, Cuisine, MealType

class FileFieldFormTest(TestCase):
    def test_multiple_file_clean(self):
        # Use SimpleUploadedFile to simulate the uploaded file
        file1 = SimpleUploadedFile("file1.txt", b"content1")
        file2 = SimpleUploadedFile("file2.txt", b"content2")
        form_data = {}
        form_files = {'file_field': [file1, file2]}
        form = FileFieldForm(data=form_data, files=form_files)
        self.assertTrue(form.is_valid())
        # The check returns a list of length 2
        cleaned_files = form.cleaned_data['file_field']
        self.assertEqual(len(cleaned_files), 2)

class UserFormTest(TestCase):
    def test_password_mismatch(self):
        form_data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'password': 'secret123',
            'confirm_password': 'secret321'
        }
        form = UserForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("Passwords don't match", form.non_field_errors())
        
    def test_valid_user_form(self):
        form_data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'password': 'secret123',
            'confirm_password': 'secret123'
        }
        form = UserForm(data=form_data)
        self.assertTrue(form.is_valid())
        # Verify that the password is encrypted after saving the user
        user = form.save()
        self.assertNotEqual(user.password, 'secret123')
        self.assertTrue(user.check_password('secret123'))

class LoginFormTest(TestCase):
    def test_login_form_fields(self):
        form_data = {'username': 'testuser', 'password': 'secret123'}
        form = LoginForm(data=form_data)
        self.assertTrue(form.is_valid())

class RecipeFormTest(TestCase):
    def setUp(self):
        # Create the necessary data for the ModelMultipleChoiceField
        self.cuisine = Cuisine.objects.create(name="Italian")
        self.meal_type = MealType.objects.create(name="Dinner")
        
    def test_recipe_form_valid(self):
        form_data = {
            'title': 'Test Recipe',
            'ingredients': 'Tomato, Cheese, Basil',
            'description': 'Mix and cook.',
            'cuisine': [self.cuisine.pk],
            'meal_type': [self.meal_type.pk],
        }
        form = RecipeForm(data=form_data)
        self.assertTrue(form.is_valid())
        
    def test_recipe_form_missing_fields(self):
        form_data = {}
        form = RecipeForm(data=form_data)
        self.assertFalse(form.is_valid())

class CommentFormTest(TestCase):
    def test_comment_form_valid(self):
        form_data = {'text': 'Nice recipe!'}
        form = CommentForm(data=form_data)
        self.assertTrue(form.is_valid())
        
    def test_comment_form_empty_text(self):
        form_data = {'text': ''}
        form = CommentForm(data=form_data)
        self.assertFalse(form.is_valid())

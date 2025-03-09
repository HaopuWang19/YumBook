from django import forms
from yum.models import *

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    confirm_password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password and confirm_password and password != confirm_password:
            raise forms.ValidationError("Passwords don't match")

        return cleaned_data


class LoginForm(forms.Form):
    username = forms.CharField(max_length=20, widget=forms.TextInput(attrs={'placeholder': 'username'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'password'}))


class RecipeForm(forms.ModelForm):
    title = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={'placeholder': 'Enter recipe title'}),
        error_messages={'required': 'title is required'}
    )

    cuisine = forms.ModelMultipleChoiceField(
        queryset=Cuisine.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=True,
        error_messages={'required': 'cuisine is required at least one'}
    )

    meal_type = forms.ModelMultipleChoiceField(
        queryset=MealType.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=True,
        error_messages={'required': 'meal_type is required at least one'}
    )

    ingredients = forms.CharField(
        widget=forms.Textarea(attrs={'placeholder': 'List ingredients, separated by comma'}),
        error_messages={'required': 'ingredients is required'}
    )

    description = forms.CharField(
        widget=forms.Textarea(attrs={'placeholder': 'Write the cooking steps here...'}),
        error_messages={'required': 'description is required'}
    )

    images = forms.FileField(
        widget=forms.ClearableFileInput(attrs={'multiple': False}),
        required=False
    )

    class Meta:
        model = Recipe
        fields = ['title', 'cuisine', 'meal_type', 'ingredients', 'description', 'images']


class CommentForm(forms.ModelForm):
    text = forms.CharField(
        widget=forms.Textarea(attrs={'placeholder': 'Write your comment'}),
        error_messages={'required': 'text is required'}
    )

    class Meta:
        model = Comment
        fields = ['text']
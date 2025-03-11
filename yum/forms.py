from django import forms
from yum.models import *

class MultipleFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True


class MultipleFileField(forms.FileField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("widget", MultipleFileInput())
        super().__init__(*args, **kwargs)

    def clean(self, data, initial=None):
        single_file_clean = super().clean
        if isinstance(data, (list, tuple)):
            result = [single_file_clean(d, initial) for d in data]
        else:
            result = single_file_clean(data, initial)
        return result


class FileFieldForm(forms.Form):
    file_field = MultipleFileField()


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(), label="Password")
    confirm_password = forms.CharField(widget=forms.PasswordInput(), label="Confirm Password")

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

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user

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

    images = MultipleFileField(required=False)

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



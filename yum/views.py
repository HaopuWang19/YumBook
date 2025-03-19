from datetime import timedelta
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect, get_object_or_404
from django.templatetags.static import static
from django.utils.timezone import now
from yum.forms import *
from yum.models import *


# Homepage view: lists recipes with images, comments count, and formatted time.
def index(request):
    posts = Recipe.objects.all().order_by('-post_date')
    for post in posts:
        print(f"Recipe ID: {post.recipe_id}")
        if post.images:
            first_image = post.images.first()
            if first_image:
                post.first_image_url = first_image.image.url
            else:
                post.first_image_url = static('/images/default.jpg')
        post.comments_count = post.comment_count()
        post.formatted_time = format_time(post.post_date)
    context = {'posts': posts}
    return render(request, 'yum/index.html', context)


# Static pages.
def about(request):
    return render(request, 'yum/about.html', context={})


def privacy(request):
    return render(request, 'yum/privacy.html', context={})


def contact(request):
    return render(request, 'yum/contact.html', context={})


# Add a new recipe; only accessible to logged in users.
@login_required
def add_recipe(request):
    if request.method == "POST":
        form = RecipeForm(request.POST, request.FILES)
        if form.is_valid():
            recipe = form.save(commit=False)
            recipe.author = request.user
            recipe.save()
            form.save_m2m()
            return redirect('/')
    else:
        form = RecipeForm()
    return render(request, 'yum/addRecipe.html', context={'form': form})


# Display a user's profile and their recipes.
def profile(request, user_id):
    user = User.objects.get(pk=user_id)
    posts = Recipe.objects.filter(author=user).order_by('-post_date')
    context = {'posts': posts, 'user': user}
    return render(request, 'yum/profile.html', context)


# User login view.
def login_page(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('/')
    else:
        form = AuthenticationForm()
    context = {'form': form}
    return render(request, 'yum/login.html', context)


# User registration view.
def register(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('/')
    else:
        form = UserForm()
    context = {'form': form}
    return render(request, 'yum/register.html', context)


# User logout view.
def logout_page(request):
    print("logging out user:", request.user)
    logout(request)
    return redirect('/')


# Recipe detail view with comment submission.
def detail(request, recipe_id):
    recipe = get_object_or_404(Recipe, pk=recipe_id)
    comments = Comment.objects.filter(recipe_id=recipe).order_by('-created_at')

    if request.method == "POST":
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.author = request.user
            comment.recipe_id = recipe
            comment.save()
            return redirect('yum:detail', recipe_id=recipe.recipe_id)
    else:
        comment_form = CommentForm()
    context = {'recipe': recipe,
               'comments': comments,
               'comment_form': comment_form,
               'formatted_time': format_time(recipe.post_date)}
    return render(request, 'yum/detail.html', context)


# Helper function to format the recipe post time.
def format_time(created_at):
    delta = now() - created_at
    if delta < timedelta(days=1):
        return created_at.strftime("%H:%M")
    elif delta < timedelta(days=10):
        return f"{delta.days} days ago"
    elif delta < timedelta(days=365):
        return created_at.strftime("%m-%d")
    else:
        return created_at.strftime("%Y-%m-%d")


# Edit an existing recipe; allows adding additional images.
@login_required
def edit_recipe(request, recipe_id):
    recipe = get_object_or_404(Recipe, recipe_id=recipe_id)
    if request.method == "POST":
        form = RecipeForm(request.POST, request.FILES, instance=recipe)
        if form.is_valid():
            recipe = form.save(commit=False)
            recipe.save()

            images = request.FILES.getlist('images')
            if images:
                for img in images[:20]:
                    RecipeImage.objects.create(recipe=recipe, image=img)

            return redirect('yum:detail', recipe_id=recipe.recipe_id)
    else:
        form = RecipeForm(instance=recipe)
    context = {'form': form, 'is_edit': True, 'recipe': recipe}
    return render(request, 'yum/addRecipe.html', context)


# Delete a recipe; only the recipe's author can delete it.
def delete_recipe(request, recipe_id):
    recipe = get_object_or_404(Recipe, pk=recipe_id)

    if request.user != recipe.author:
        return redirect('yum:profile', user_id=request.user.id)
    recipe.delete()
    return redirect('yum:profile', user_id=request.user.id)

from datetime import timedelta

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.utils.timezone import now

from yum.forms import *
from yum.models import *




def index(request):
    posts = Recipe.objects.all().order_by('-post_date')
    for post in posts:
        print(f"Recipe ID: {post.recipe_id}")
        post.comments_count = post.comment_count()
        post.formatted_time = format_time(post.post_date)
    context = {'posts': posts}
    return render(request, 'yum/index.html', context)


def about(request):
    return render(request, 'yum/about.html', context={})


def privacy(request):
    return render(request, 'yum/privacy.html', context={})


def contact(request):
    return render(request, 'yum/contact.html', context={})

@login_required
def add_recipe(request):
    if request.method == "POST":
        form = RecipeForm(request.POST, request.FILES)
        if form.is_valid():
            user_profile, created = UserProfile.objects.get_or_create(user=request.user)
            recipe = form.save(commit=False)
            recipe.author = user_profile
            recipe.save()

            recipe.cuisine.set(form.cleaned_data['cuisine'])
            recipe.meal_type.set(form.cleaned_data['meal_type'])

            images = request.FILES.getlist('images')
            if images:
                for img in images[:20]:
                    Recipe.objects.create(
                        author=request.author,
                        title=recipe.title,
                        ingredients=recipe.ingredients,
                        description=recipe.description,
                        image=img)
            else:
                recipe.image = 'static/images/default.jpg'
                recipe.save()
            return redirect('yum:index')
    else:
        form = RecipeForm()
    return render(request, 'yum/addRecipe.html', context={'form': form})


def profile(request, user_id):
    if not request.user.is_authenticated:
        return redirect('yum:login')

    user_profile, created = UserProfile.objects.get_or_create(user_id=user_id)
    posts = Recipe.objects.filter(author=user_profile).order_by('-post_date')

    context = {'posts': posts, 'user_profile': user_profile}
    return render(request, 'yum/profile.html', context)


def login_page(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)

            if user:
                #if user.is_superuser:
                #    return render(request, 'yum/login.html', {'form': form,'error': 'Admin accounts cannot log in here.'})
                login(request, user)
                return redirect('/')
            else:
                context = {'form': form, 'error': 'Invalid username or password'}
                return render(request, 'yum/login.html', context)
    else:
        form = LoginForm()
    context = {'form': form}
    return render(request, 'yum/login.html', context)


def register(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()

            authenticate_user = authenticate(username=user.username, password=form.cleaned_data['password'])
            if authenticate_user:
                login(request, authenticate_user)
                return redirect('/')
            else:
                print("Authentication failed after registration.")
    else:
        form = UserForm()
    context = {'form': form}
    return render(request, 'yum/register.html', context)


def logout_page(request):
    print("logging out user:", request.user)
    logout(request)
    return redirect('/')


def detail(request, recipe_id):
    recipe = get_object_or_404(Recipe, pk=recipe_id)
    comments = Comment.objects.filter(recipe_id=recipe).order_by('-created_at')
    comment_form = CommentForm()

    if request.method == "POST":
        if request.user.is_authenticated:
            form = CommentForm(request.POST)
            if form.is_valid():
                user_profile = UserProfile.objects.get(user=request.user)
                comment = form.save(commit=False)
                comment.author = user_profile
                comment.recipe_id = recipe
                comment.save()
                return redirect('yum:detail', recipe_id=recipe_id)
        else:
            return redirect('yum:login')
    context = {'recipe': recipe,
               'comments': comments,
               'comment_form': comment_form,
               'formatted_time': format_time(recipe.post_date)}
    return render(request, 'yum/detail.html', context)


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


def edit_recipe(request, recipe_id):
    recipe = get_object_or_404(Recipe, pk=recipe_id)
    if request.method == "POST":
        form = RecipeForm(request.POST, request.FILES, instance=recipe)
        if form.is_valid():
            form.save()
            return redirect('yum:profile', user_id=request.user.userprofile.user_id)
    else:
        form = RecipeForm(instance=recipe)
    context = {'form': form, 'is_edit': True}
    return render(request, 'yum/addRecipe.html', context)

def delete_recipe(request, recipe_id):
    recipe = get_object_or_404(Recipe, pk=recipe_id)

    if request.user != recipe.author.user:
        return redirect('yum:profile', user_id=request.user.userprofile.user_id)
    recipe.delete()
    return redirect('yum:profile', user_id=request.user.userprofile.user_id)
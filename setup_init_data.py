import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'YumBook.settings')
django.setup()

from yum.models import User, Cuisine, MealType


# ✅ 创建测试用户
def create_test_users():
    users_data = [
        {'username': 'testuser1', 'email': 'test1@example.com', 'password': 'test123'},
        {'username': 'testuser2', 'email': 'test2@example.com', 'password': 'test123'},
        {'username': 'testuser3', 'email': 'test3@example.com', 'password': 'test123'}
    ]

    for user_data in users_data:
        user, created = User.objects.get_or_create(username=user_data['username'], email=user_data['email'])
        if created:
            user.set_password(user_data['password'])  # 🔒 加密密码
            user.save()
            print(f'🟢 Created test user: {user.username}')


# ✅ 预创建 `Cuisine` 和 `MealType`
def setup_data():
    cuisines = ['Chinese Dish', 'American Dish', 'French Dish', 'Japanese Dish', 'Korean Dish']
    meal_types = ['Breakfast', 'Lunch', 'Afternoon Tea', 'Dinner', 'Dessert']

    for cuisine in cuisines:
        Cuisine.objects.get_or_create(name=cuisine)

    for meal in meal_types:
        MealType.objects.get_or_create(name=meal)

    print('✅ Cuisine & MealType setup completed!')


if __name__ == '__main__':
    print('🔹 Setting up users & basic data...')
    create_test_users()
    setup_data()
    print('✅ Users & base data setup completed!')

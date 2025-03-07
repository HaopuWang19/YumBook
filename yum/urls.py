from django.urls import path
from yum import views

app_name = 'yum'

urlpatterns = [
    path('', views.index, name='index'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('privacy/', views.privacy, name='privacy'),
    path('add_food/', views.add_food, name='add_food'),
    path('profile/', views.profile, name='profile'),
]
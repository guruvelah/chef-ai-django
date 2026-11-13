from django.urls import path
from . import views

app_name = 'recipes'

urlpatterns = [
    path('', views.home, name='home'),
    path('recipe/<int:pk>/', views.recipe_detail, name='detail'),
    path('api/chat/', views.chat_api, name='chat_api'),
    path('api/pantry/', views.pantry_match, name='pantry_match'),
    path('api/recipes/', views.api_recipes, name='api_recipes'),
]

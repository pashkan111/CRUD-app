from django.urls import path, include
from .views import (
SignUp, MyTokenObtainPairView, get_posts, create_post, update_post, delete_post, get_post
    )
from rest_framework_simplejwt.views import TokenRefreshView


urlpatterns = [
    path('users/register/', SignUp.as_view()),
    path('users/login/', MyTokenObtainPairView.as_view()),
    path('users/refresh/', TokenRefreshView.as_view()),
    path('posts/', get_posts),
    path('post/<str:id>', get_post),
    path('create-post/', create_post),
    path('update-post/', update_post),
    path('delete-post/<int:id>', delete_post),
]

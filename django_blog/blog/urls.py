from django.urls import path
from .views import register, profile, List_view,  Delete_view, Detail_View, create_view, Update_View
from django.contrib.auth.views import LogoutView
from django.contrib.auth.views import LoginView

urlpatterns = [
    path('register/', register, name='register'),
    path('profile/', profile, name='profile_update'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('posts/', List_view.as_view(), name='post_list'),       # List all posts
    path('posts/<int:pk>/', Detail_View.as_view(), name='post_detail'),  # View a specific post
    path('posts/new/', create_view.as_view(), name='post_create'),  # Create a new post
    path('posts/<int:pk>/edit/', Update_View.as_view(), name='post_edit'),  # Edit an existing post
    path('posts/<int:pk>/delete/', Delete_view.as_view(), name='post_delete'),  # Delete a post
    
]

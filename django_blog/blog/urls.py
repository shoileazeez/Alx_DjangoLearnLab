from django.urls import path
from .views import register, profile, List_view,  Delete_view, Detail_View, create_view, Update_View, CommentCreateView, CommentUpdateView,CommentDeleteView
from django.contrib.auth.views import LogoutView
from django.contrib.auth.views import LoginView


urlpatterns = [
    path('register/', register, name='register'),
    path('profile/', profile, name='profile_update'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('post/', List_view.as_view(), name='post_list'),       # List all posts
    path('post/<int:pk>/comments/new/', Detail_View.as_view(), name='post_detail'),  # View a specific post
    path('post/new/', create_view.as_view(), name='post_create'),  # Create a new post
    path('post/<int:pk>/update/', Update_View.as_view(), name='post_edit'),  # Edit an existing post
    path('post/<int:pk>/delete/', Delete_view.as_view(), name='post_delete'),  # Delete a post
    path('post/<int:pk>/comments/new/', CommentCreateView.as_view(), name='add_comment'),
    path('comment/<int:pk>/update/', CommentUpdateView.as_view(), name='comment_edit'),
    path('comment/<int:pk>/delete/', CommentDeleteView.as_view(), name='comment_delete'), 

]

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PostViewSet, CommentViewSet,FeedView,LikePostAPIView,UnlikePostAPIView

# Initialize the router
router = DefaultRouter()

# Register the PostViewSet and CommentViewSet with the router
router.register(r'posts', PostViewSet, basename='post')
router.register(r'comments', CommentViewSet, basename='comment')

# Include the router-generated URL patterns
urlpatterns = [
    path('', include(router.urls)),
    path('feed/', FeedView.as_view(), name='feed'),
    path('posts/<int:post_id>/like/', LikePostAPIView.as_view(), name='like-post'),
    path('posts/<int:post_id>/unlike/', UnlikePostAPIView.as_view(), name='unlike-post'),
    # This will include all routes for posts and comments
]

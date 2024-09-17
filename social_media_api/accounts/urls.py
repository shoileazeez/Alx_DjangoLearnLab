from django.urls import path,include
from .views import UserRegistrationView, UserLoginView, UserProfileView
from .views import FollowViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'users', FollowViewSet, basename='users')

urlpatterns = [
    path('register/', UserRegistrationView.as_view(), name='register'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('profile/', UserProfileView.as_view(), name='profile'),
    path('', include(router.urls)),
    path('follow/<int:user_id>', FollowViewSet.as_view({'post': 'follow_user'}), name='follow_user'),
    path('unfollow/<int:user_id>/', FollowViewSet.as_view({'post': 'unfollow_user'}), name='unfollow_user'),
    path('followers/', FollowViewSet.as_view({'get': 'list_followers'}), name='list_followers'),
    path('following/', FollowViewSet.as_view({'get': 'list_following'}), name='list_following'),
]
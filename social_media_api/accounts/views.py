from django.shortcuts import render
from django.contrib.auth import authenticate,login,get_user_model
from django.shortcuts import get_object_or_404
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status, viewsets
from .serializers import UserRegistrationSerializer,  UserProfileSerializer
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.contrib.auth import get_user_model
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination

# User Registration View
class UserRegistrationView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            token, created = Token.objects.get_or_create(user=user)
            return Response({
                'token': token.key,
                'message': 'User registered successfully.'
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Login View
class UserLoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=username, password=password)

        if user:
            login(request, user)
            token, created = Token.objects.get_or_create(user=user)
            return Response({
                'token': token.key,
                'message': 'Login successful.'
            }, status=status.HTTP_200_OK)
        else:
            return Response({
                'error': 'Invalid credentials'
            }, status=status.HTTP_400_BAD_REQUEST)


class UserProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        serializer = UserProfileSerializer(user)
        return Response(serializer.data)

    def put(self, request):
        user = request.user
        serializer = UserProfileSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    



User = get_user_model()

class FollowViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    @action(detail=True, methods=['post'], url_path='follow')
    def follow_user(self, request, pk=None):
        """Follow a user, with checks to avoid duplicates."""
        user_to_follow = get_object_or_404(User, pk=pk)

        if request.user == user_to_follow:
            return Response({'error': 'You cannot follow yourself.'}, status=status.HTTP_400_BAD_REQUEST)

        if user_to_follow in request.user.following.all():
            return Response({'error': f'You are already following {user_to_follow.username}.'}, status=status.HTTP_400_BAD_REQUEST)

        request.user.following.add(user_to_follow)
        return Response({'message': f'You are now following {user_to_follow.username}.'}, status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'], url_path='unfollow')
    def unfollow_user(self, request, pk=None):
        """Unfollow a user."""
        user_to_unfollow = get_object_or_404(User, pk=pk)

        if request.user == user_to_unfollow:
            return Response({'error': 'You cannot unfollow yourself.'}, status=status.HTTP_400_BAD_REQUEST)

        if user_to_unfollow not in request.user.following.all():
            return Response({'error': f'You are not following {user_to_unfollow.username}.'}, status=status.HTTP_400_BAD_REQUEST)

        request.user.following.remove(user_to_unfollow)
        return Response({'message': f'You have unfollowed {user_to_unfollow.username}.'}, status=status.HTTP_200_OK)
    
     
    
    @action(detail=False, methods=['get'], url_path='followers')
    def list_followers(self, request):
        """List followers with pagination."""
        paginator = PageNumberPagination()
        paginator.page_size = 10  # Adjust as needed
        followers = request.user.followers.all()
        paginated_followers = paginator.paginate_queryset(followers, request)
        return paginator.get_paginated_response([{'username': user.username} for user in paginated_followers])

    @action(detail=False, methods=['get'], url_path='following')
    def list_following(self, request):
        """List following with pagination."""
        paginator = PageNumberPagination()
        paginator.page_size = 10  # Adjust as needed
        following = request.user.following.all()
        paginated_following = paginator.paginate_queryset(following, request)
        return paginator.get_paginated_response([{'username': user.username} for user in paginated_following])

    
# Create your views here.






generics.GenericAPIView", "permissions.IsAuthenticated", "CustomUser.objects.all()
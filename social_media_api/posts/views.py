import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from django.shortcuts import render
from rest_framework import viewsets, permissions
from .models import Post, Comment,Like
from .serializers import PostSerializer, CommentSerializer
from .permissions import IsOwnerOrReadOnly
from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from notifications.models import Notification
from django.utils.timezone import now
from .models import Post



class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['title', 'content']  
    ordering_fields = ['created_at', 'title']  
    ordering = ['-created_at']

    def perform_create(self, serializer):
        # Set the author to the current logged-in user
        serializer.save(author=self.request.user)

class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

    def perform_create(self, serializer):
        # Save the comment and set the author to the current logged-in user
        comment = serializer.save(author=self.request.user)
        
        # Access the related Post from the comment
        post = comment.post
        
        # Create the notification, notifying the post's author
        Notification.objects.create(
            recipient=post.author,  # Notify the post's author
            sender=self.request.user,  # The current logged-in user is the sender
            action=f"commented on your post '{post.title}'",  # Add a message with the post title
            post=post  # Link the notification to the post
        )


    

class FeedView(generics.ListAPIView):
    """Feed showing posts from followed users."""
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Get posts from users the current user is following."""
        user = self.request.user
        following_users = user.following.all()  # Users that the current user is following
        return Post.objects.filter(author__in=following_users).order_by('-created_at')
# Create your views here.



class LikePostAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, post_id):
        post = get_object_or_404(Post, id=post_id)
        user = request.user

        # Check if the post is already liked by the user
        if Like.objects.filter(user=user, post=post).exists():
            return Response({"detail": "You have already liked this post."}, status=status.HTTP_400_BAD_REQUEST)

        # Create a like for the post
        Like.objects.create(user=user, post=post)

        # Create a notification if the user liking the post is not the author
        if post.author != user:
            Notification.objects.create(
                recipient=post.author,
                actor=user,
                verb='liked your post',
                target=post
            )

        return Response({"detail": "Post liked successfully!"}, status=status.HTTP_200_OK)

class UnlikePostAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, post_id):
        post = get_object_or_404(Post, id=post_id)
        user = request.user

        # Find the like for this user and post
        like = Like.objects.filter(user=user, post=post).first()
        if like:
            like.delete()
            return Response({"detail": "Post unliked successfully!"}, status=status.HTTP_200_OK)

        return Response({"detail": "You haven't liked this post yet."}, status=status.HTTP_400_BAD_REQUEST)
    
    
posts/views.py doesn't contain: ["generics.get_object_or_404(Post, pk=pk)", "Like.objects.get_or_create(user=request.user, post=post)"]
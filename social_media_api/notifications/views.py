from django.shortcuts import render
from rest_framework import generics
from .models import Notification
from .serializers import NotificationSerializer
from rest_framework.permissions import IsAuthenticated

class NotificationListView(generics.ListAPIView):
    """Fetch notifications with unread notifications prioritized."""
    serializer_class = NotificationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Fetch unread notifications first, followed by read notifications
        user = self.request.user
        unread_notifications = Notification.objects.filter(recipient=user, is_read=False)
        read_notifications = Notification.objects.filter(recipient=user, is_read=True)
        return unread_notifications | read_notifications  # Concatenate both sets

# Create your views here.

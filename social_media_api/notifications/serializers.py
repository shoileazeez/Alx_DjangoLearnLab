from rest_framework import serializers
from .models import Notification

class NotificationSerializer(serializers.ModelSerializer):
    recipient = serializers.CharField(source='recipient.username', read_only=True)
    actor = serializers.CharField(source='actor.username', read_only=True)
    target = serializers.SerializerMethodField()

    class Meta:
        model = Notification
        fields = ['id', 'recipient', 'actor', 'verb', 'target', 'timestamp', 'is_read']  # Include 'is_read'

    def get_target(self, obj):
        if obj.target:
            return str(obj.target)
        return None

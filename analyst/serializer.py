from rest_framework import serializers
from .models import Sessions, Messages

class SessionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sessions
        fields = ('id', 'user_id', 'created_at', 'date_modified')

class MessagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Messages
        fields = ('id', 'session_id', 'human', 'ai', 'created_at', 'date_modified')
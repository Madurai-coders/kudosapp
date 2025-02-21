from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Kudos

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']

class KudosSerializer(serializers.ModelSerializer):
    giver = UserSerializer(read_only=True)  # Read-only giver
    receiver = UserSerializer(read_only=True)  # Read-only receiver
    receiver_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), source="receiver", write_only=True
    )  # Accept `receiver_id` but map to `receiver`

    class Meta:
        model = Kudos
        fields = ["id", "giver", "receiver", "receiver_id", "message", "created_at"]
        read_only_fields = ["id", "giver", "created_at"]

    def create(self, validated_data):
        """Override create to assign giver automatically"""
        request = self.context.get("request")  # Get request from context
        validated_data["giver"] = request.user  # Set giver automatically
        return super().create(validated_data)
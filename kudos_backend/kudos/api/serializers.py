from rest_framework import serializers
from .models import Kudos
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    """Serializer for User model."""
    
    organization = serializers.StringRelatedField()  # Return org name instead of ID

    
    class Meta:
        model = User
        fields = ["id", "username", "email","organization"]
        

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    """Customize JWT response to include user info and organization"""

    def validate(self, attrs):
        data = super().validate(attrs)

        user = self.user  # Get the authenticated user
        data["user"] = {
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "organization": {
                "id": user.organization.id if user.organization else None,
                "name": user.organization.name if user.organization else ("Admin (No Organization)" if user.is_superuser else None),
            }
        }
        return data


class KudosSerializer(serializers.ModelSerializer):
    """Serializer for Kudos model with giver and receiver details."""

    giver = UserSerializer(read_only=True)  # Include giver details (read-only)
    receiver = UserSerializer(read_only=True)  # Include receiver details (read-only)
    receiver_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), source="receiver", write_only=True
    )  # Accept `receiver_id` as input but map it to `receiver`

    class Meta:
        model = Kudos
        fields = ["id", "giver", "receiver", "receiver_id", "message", "created_at"]
        read_only_fields = ["id", "giver", "created_at"]

    def create(self, validated_data):
        """Automatically assign the authenticated user as the giver."""
        request = self.context.get("request")
        if not request or not request.user.is_authenticated:
            raise serializers.ValidationError("User must be authenticated.")
        
        validated_data["giver"] = request.user  # Set authenticated user as giver
        return super().create(validated_data)

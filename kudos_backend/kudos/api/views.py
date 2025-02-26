from django.utils.timezone import now
from django.shortcuts import get_object_or_404
from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import action, permission_classes, api_view
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView

from .models import Kudos, KudosQuota
from .serializers import UserSerializer, KudosSerializer, CustomTokenObtainPairSerializer
from django.contrib.auth import get_user_model
from django.db.models import Q

User = get_user_model()
MAX_KUDOS_PER_WEEK = 3  # Weekly kudos limit per user

# ------------------------------
# User Endpoints (Organization-Based)
# ------------------------------

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_users(request):
    """Retrieve all users within the same organization, except the authenticated user."""
    if request.user.is_superuser:
        users = User.objects.exclude(id=request.user.id)  # Superusers see all users
    else:
        users = User.objects.filter(organization=request.user.organization).exclude(id=request.user.id) | User.objects.filter(is_superuser=True)

    serializer = UserSerializer(users, many=True)
    return Response(serializer.data)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_kudos_quota(request):
    """Get the remaining kudos quota for the authenticated user."""
    quota, _ = KudosQuota.objects.get_or_create(user=request.user, defaults={"kudos_remaining": MAX_KUDOS_PER_WEEK})
    return Response({"kudos_remaining": max(quota.kudos_remaining, 0)})


# ------------------------------
# Kudos Endpoints (Organization-Based)
# ------------------------------

class KudosViewSet(viewsets.ModelViewSet):
    """Viewset for handling Kudos-related actions (organization-scoped)."""
    serializer_class = KudosSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Filter Kudos by the user's organization (unless superuser)."""
        if self.request.user.is_superuser:
            return Kudos.objects.all().order_by("-created_at")
        return Kudos.objects.filter(
        Q(giver__organization=self.request.user.organization) |
        Q(receiver__organization=self.request.user.organization)
        ).order_by("-created_at")

    def get_serializer_context(self):
        """Pass request context to serializer."""
        return {"request": self.request}

    def perform_create(self, serializer):
        """Allow admins to give kudos across organizations while enforcing quota."""
        user = self.request.user
        receiver = serializer.validated_data.get("receiver")

        # Allow superusers to give kudos to anyone
        if not user.is_superuser:
            # Regular user: Must belong to an organization and give kudos within it
            if not user.organization:
                return Response(
                    {"error": "You must belong to an organization to give kudos."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            # Allow regular users to send kudos to superusers
            if not receiver.is_superuser and receiver.organization != user.organization:
                return Response(
                    {"error": "You can only give kudos within your organization, except for superusers."},
                    status=status.HTTP_403_FORBIDDEN,
                )

        # Enforce the same kudos quota for both regular users and admins
        quota, _ = KudosQuota.objects.get_or_create(user=user, defaults={"kudos_remaining": MAX_KUDOS_PER_WEEK})
        if quota.kudos_remaining <= 0:
            return Response(
                {"error": "Kudos quota exceeded for this week."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Deduct quota for both admins and regular users
        KudosQuota.objects.filter(user=user).update(kudos_remaining=quota.kudos_remaining - 1)

        serializer.save()  # Save the Kudos object


    @action(detail=False, methods=["get"])
    def received(self, request):
        """Get all kudos received by the authenticated user (within organization)."""
        kudos = Kudos.objects.filter(receiver=request.user)
        serializer = self.get_serializer(kudos, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=["get"])
    def given(self, request):
        """Get all kudos given by the authenticated user (within organization)."""
        kudos = Kudos.objects.filter(giver=request.user)
        serializer = self.get_serializer(kudos, many=True)
        return Response(serializer.data)


# ------------------------------
# Authentication Views
# ------------------------------

class CustomTokenObtainPairView(TokenObtainPairView):
    """Custom JWT view returning user details including organization."""
    serializer_class = CustomTokenObtainPairSerializer


class LogoutView(APIView):
    """Logout a user by blacklisting their refresh token."""
    permission_classes = [IsAuthenticated]

    def post(self, request):
        refresh_token = request.data.get("refresh_token")
        if not refresh_token:
            return Response({"error": "Refresh token is required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            RefreshToken(refresh_token).blacklist()  # Blacklist the token
            return Response({"message": "Successfully logged out"}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

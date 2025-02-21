from django.shortcuts import render
from django.contrib.auth.models import User
from rest_framework import viewsets, permissions ,status
from rest_framework.response import Response
from rest_framework.decorators import action,permission_classes, api_view
from rest_framework.permissions import IsAuthenticated
from .serializers import UserSerializer
from .models import Kudos
from .serializers import KudosSerializer
from django.utils.timezone import now, timedelta
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from .models import Kudos, KudosQuota
from rest_framework.status import HTTP_400_BAD_REQUEST



@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_users(request):
    users = User.objects.exclude(id=request.user.id)  # Exclude the current user
    serializer = UserSerializer(users, many=True)
    return Response(serializer.data)

MAX_KUDOS_PER_WEEK = 3  # Kudos limit per user per week

@api_view(["GET"])
@permission_classes([permissions.IsAuthenticated])
def get_kudos_quota(request):
    """Returns the remaining kudos quota for the authenticated user."""
    quota, _ = KudosQuota.objects.get_or_create(user=request.user, defaults={"kudos_remaining": MAX_KUDOS_PER_WEEK})
    return Response({"kudos_remaining": max(quota.kudos_remaining, 0)})

class KudosViewSet(viewsets.ModelViewSet):
    queryset = Kudos.objects.all().order_by("-created_at")
    serializer_class = KudosSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_context(self):
        """Pass request context to serializer"""
        return {"request": self.request}

    def perform_create(self, serializer):
        """Reduce the remaining kudos every time the user sends a kudos"""
        quota, _ = KudosQuota.objects.get_or_create(
            user=self.request.user, defaults={"kudos_remaining": MAX_KUDOS_PER_WEEK}
        )

        if quota.kudos_remaining <= 0:
            return Response({"error": "Kudos quota exceeded for this week."}, status=HTTP_400_BAD_REQUEST)

        quota.kudos_remaining -= 1  # Reduce kudos count
        quota.save(update_fields=["kudos_remaining"])  # Save updated quota

        serializer.save(giver=self.request.user)  # Save the kudos entry

    @action(detail=False, methods=["get"])
    def received(self, request):
        """Get kudos received by the authenticated user"""
        kudos = Kudos.objects.filter(receiver=request.user)
        serializer = self.get_serializer(kudos, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=["get"])
    def given(self, request):
        """Get kudos given by the authenticated user"""
        kudos = Kudos.objects.filter(giver=request.user)
        serializer = self.get_serializer(kudos, many=True)
        return Response(serializer.data)


class LogoutView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.data.get("refresh_token")  # Get token from request
            if not refresh_token:
                return Response({"error": "Refresh token is required"}, status=status.HTTP_400_BAD_REQUEST)

            token = RefreshToken(refresh_token)  # Convert to token object
            token.blacklist()  # Blacklist the refresh token
            
            return Response({"message": "Successfully logged out"}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

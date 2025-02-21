from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import KudosViewSet, get_users, get_kudos_quota, LogoutView, CustomTokenObtainPairView

# Register routes using Django Rest Framework's DefaultRouter
router = DefaultRouter()
router.register(r'kudos', KudosViewSet, basename='kudos')

# Define API endpoints
urlpatterns = [
    path('', include(router.urls)),  # Includes all viewset routes
    path("users/", get_users, name="get_users"),  # Get list of users
    path("user/quota/", get_kudos_quota, name="get_kudos_quota"),  # Get kudos quota
    path("logout/", LogoutView.as_view(), name="logout"),  # Logout endpoint
    path("login/", CustomTokenObtainPairView.as_view(), name="token_obtain_pair"),

]

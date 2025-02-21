from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import KudosViewSet,get_users, get_kudos_quota,LogoutView

router = DefaultRouter()
router.register(r'kudos', KudosViewSet, basename='kudos')

urlpatterns = [
    path('', include(router.urls)),
    path("users/", get_users, name="get_users"),
    path("user/quota/", get_kudos_quota, name="get_kudos_quota"),
    path("logout/", LogoutView.as_view(), name="logout"),

]

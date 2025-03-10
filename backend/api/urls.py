from django.urls import path, include
from rest_framework.routers import SimpleRouter
from .views import UserViewSet, PostViewSet, CachedUserViewSet

router = SimpleRouter()
router.register(r'users', UserViewSet, basename='user')
router.register(r'posts', PostViewSet, basename='post')
router.register(r'cached_users', CachedUserViewSet, basename='cached_user')

urlpatterns = [
    path('api/', include(router.urls)),
]
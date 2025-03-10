from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserViewSet, PostViewSet, CachedUserViewSet
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView

# Define API v1 router and register viewsets
router_v1 = DefaultRouter()
router_v1.register(r'users', UserViewSet, basename='user')  # User endpoints
router_v1.register(r'posts', PostViewSet, basename='post')  # Post endpoints
router_v1.register(r'cached_users', CachedUserViewSet, basename='cached-user')  # Cached user endpoints

urlpatterns = [
    # Include API v1 routes
    path('api/v1/', include(router_v1.urls)),

    # API Schema and Documentation
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/schema/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
]

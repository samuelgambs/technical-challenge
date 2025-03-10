from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from django.urls import path

# URL patterns for JWT authentication
urlpatterns = [
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),  # Generate access & refresh tokens
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),  # Refresh the access token
]

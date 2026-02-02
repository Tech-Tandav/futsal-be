from django.urls import path

from backend.users.api.socialaccount.views import (
    GoogleLoginView
)

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

# JWT refresh tokens
urlpatterns = [
    path('login/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('login/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]

urlpatterns += [
    path('google/auth/', GoogleLoginView.as_view(), name='google-login')
]
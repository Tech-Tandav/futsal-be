from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from dj_rest_auth.registration.views import SocialLoginView
from allauth.socialaccount.providers.oauth2.client import OAuth2Client, OAuth2Error

from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken

class GoogleLoginView(SocialLoginView):
    adapter_class = GoogleOAuth2Adapter
    client_class = OAuth2Client

    def get_response(self):
        """
        overriding to return the jwt tokens instead of the default key return
        """
        try:
            user=self.user
            refresh=RefreshToken.for_user(user)

            data = {
                "access":str(refresh.access_token),
                "refresh":str(refresh)
            }

            return Response(data, status=status.HTTP_200_OK)

        except OAuth2Error as e:
            return Response(
                {"error": "Google token invalid or request failed", "details": str(e)},
                status=status.HTTP_400_BAD_REQUEST,
            )
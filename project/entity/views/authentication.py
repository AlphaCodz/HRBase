from rest_framework import viewsets, permissions, views, response, status
from rest_framework_simplejwt.views import TokenObtainPairView
from . import User, UserSerializer, MyTokenObtainPairSerializer
from rest_framework_simplejwt.token_blacklist.models import BlacklistedToken, OutstandingToken
from rest_framework_simplejwt.tokens import RefreshToken


class SignUpUser(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (permissions.AllowAny,)


class SignInUserView(TokenObtainPairView):
    permission_classes = (permissions.AllowAny,)
    serializer_class = MyTokenObtainPairSerializer
    


class CustomTokenBlacklistView(views.APIView):
    def post(self, request, *args, **kwargs):
        try:
            # Extract the refresh token from the request
            refresh_token = request.data.get('refresh')

            if not refresh_token:
                return response.Response({"error": "Refresh token is required"}, status=status.HTTP_400_BAD_REQUEST)

            # Blacklist the token
            token = RefreshToken(refresh_token)
            token.blacklist()

            # Return a custom response after blacklisting
            return response.Response({
                "message": "Token successfully blacklisted",
                "blacklisted_token": refresh_token,
                "status": "Blacklisted"
            }, status=status.HTTP_205_RESET_CONTENT)

        except Exception as e:
            return response.Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
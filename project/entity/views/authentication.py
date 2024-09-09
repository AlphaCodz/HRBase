from rest_framework import viewsets, permissions, views, response, status
from rest_framework_simplejwt.views import TokenObtainPairView
from . import User, UserSerializer, MyTokenObtainPairSerializer
from rest_framework_simplejwt.token_blacklist.models import BlacklistedToken, OutstandingToken
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.decorators import action
import logging

logger = logging.getLogger(__name__)

class SignUpUser(viewsets.ViewSet):
    def get_queryset(self):
        return User.objects.all()
    
    def get_object(self, pk):
        try:
            return User.objects.get(pk=pk)
        except User.DoesNotExist:
            raise response.Http404
        
    def get_serializer(self, *args, **kwargs):
        return UserSerializer(*args, **kwargs)
    
    # Create User Account
    @action(detail=False, methods=['post'], url_path='create', url_name='account_create')
    def create_user(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return response.Response(serializer.data, status=status.HTTP_201_CREATED)
        return response.Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    # Get all Users
    @action(detail=False, methods=['get'], url_path='get_all_users', url_name='users')
    def get_all_users(self, request):
        users = self.get_queryset()
        user_serializer = self.get_serializer(users, many=True)
        return response.Response(user_serializer.data, status=status.HTTP_200_OK)
    
    @action(detail=True, methods=['get'], url_path='get_user', url_name='retrieve_user')
    def retrieve_user(self, request, pk=None):
        try:
            user = self.get_object(pk)
        except User.DoesNotExist:
            logger.error("An Error Occured", exc_info=True)
            raise response.Response("User Does Not Exist", status=status.HTTP_404_NOT_FOUND)
        
        user_serializer = self.get_serializer(user)
        return response.Response(user_serializer.data, status=status.HTTP_200_OK)
    
    @action(detail=True, methods=['get'], url_path='delete', url_name='delete-user')
    def delete_user(self, request, pk=None):
        try:
            user = self.get_object(pk)
        except User.DoesNotExist:
            logger.error("An Error Occured", exc_info=True)
            raise response.Http404
        
        user.delete()
        return response.Response("User Account Deleted Successfully!", status=status.HTTP_204_NO_CONTENT)
        


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
from rest_framework import viewsets, permissions
from rest_framework_simplejwt.views import TokenObtainPairView
from . import User, UserSerializer, MyTokenObtainPairSerializer



class SignUpUser(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (permissions.AllowAny,)


class SignInUserView(TokenObtainPairView):
    permission_classes = (permissions.AllowAny,)
    serializer_class = MyTokenObtainPairSerializer
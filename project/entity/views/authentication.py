from rest_framework import viewsets, permissions
from . import User, UserSerializer



class SignUpUser(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (permissions.AllowAny,)
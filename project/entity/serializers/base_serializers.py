from rest_framework import serializers
from . import User
import re

class UserSerializer(serializers.ModelSerializer):
    date_joined = serializers.DateTimeField(read_only=True)
    last_login = serializers.TimeField(read_only=True)
    
    class Meta:
        model = User
        fields = ["id", "name", "email", "role", "address", "password", "date_joined", "last_login"]
        
    def validate(self, attrs):
        email = attrs.get("email")
        password = attrs.get('password')
        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError({'error': 'A user with this email already exists.'})
        
        if password:
        # Validate the password using regular expressions
            if not re.match(r'^(?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*\W).+$', password):
                raise serializers.ValidationError({"error":"Passwords must include at least one special symbol, one number, one lowercase letter, and one uppercase letter."})
            elif len(password) <= 5:
                raise serializers.ValidationError({'error': 'Passwords must be longer than 5 letters.'})
            
        return attrs
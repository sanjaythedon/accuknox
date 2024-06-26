from rest_framework import serializers
from .models import ModifiedUser


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = ModifiedUser
        fields = ['id', 'name', 'username', 'email']
        
        
class SignupSerializer(serializers.Serializer):
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)
    email = serializers.EmailField(required=True)
    password = serializers.CharField(required=True)
    
    
class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(required=True)
        
        

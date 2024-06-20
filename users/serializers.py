from rest_framework import serializers
from .models import ModifiedUser


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = ModifiedUser
        fields = ['id', 'name', 'username', 'email']
        
        

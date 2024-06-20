from rest_framework import serializers
from .models import FriendRequests
from users.models import ModifiedUser

class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = ModifiedUser
        fields = ['id', 'name', 'username', 'email']


class FriendsSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(source='sender_id.id')
    name = serializers.CharField(source='sender_id.name')
    email = serializers.CharField(source='sender_id.email')
    
    class Meta:
        model = FriendRequests
        fields = ['id', 'name', 'email']
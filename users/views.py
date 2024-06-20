from .serializers import UserSerializer
from .models import ModifiedUser

from rest_framework.views import APIView
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework.throttling import UserRateThrottle
from rest_framework.pagination import PageNumberPagination
from rest_framework.mixins import ListModelMixin
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated


class UserRegistration(APIView):    
    def post(self, request):
        ser = UserSerializer(data=request.data)
        if ser.is_valid():
            u = ModifiedUser.objects.create(**request.data)
            u.set_password(request.data['password'])
            u.save()
            return Response({'msg': 'User created'})
        else:
            return Response({'msg': 'User not created'})            
        
        
class Logout(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        request.user.auth_token.delete()
        return Response({'msg': 'Token deleted'})
    
    
class GetAllUsers(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        users = ModifiedUser.objects.all().order_by('id')
        name = request.query_params.get('name')
        email = request.query_params.get('email')
        if name:
            users = users.filter(name__icontains=name)
        elif email:
            users = users.filter(email__icontains=email)
        page = PageNumberPagination()
        page.page_size = 10
        users = page.paginate_queryset(users, request)
        ser = UserSerializer(users, many=True)
        response = page.get_paginated_response(ser.data)
        return response
    
    

        
    
            




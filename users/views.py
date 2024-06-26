from typing import Any
from django.contrib.auth.base_user import AbstractBaseUser
from django.http import HttpRequest
from .serializers import UserSerializer
from .models import ModifiedUser
from .permissions import IsLoggedIn
from .pagination import TenEntriesPage

from django.contrib.auth import authenticate

from rest_framework.views import APIView
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework.throttling import UserRateThrottle
from rest_framework.pagination import PageNumberPagination
from rest_framework.mixins import ListModelMixin
from rest_framework.generics import ListAPIView
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token

from .serializers import SignupSerializer, LoginSerializer
    
    
class UserRegistration(APIView):
    def post(self, request):
        ser = SignupSerializer(data=request.data)
        if ser.is_valid():
            email = ser.validated_data.get('email')
            password = ser.validated_data.get('password')
            first_name = ser.validated_data.get('first_name')
            last_name = ser.validated_data.get('last_name')
            full_name = first_name + " " + last_name
            username = first_name.lower() + "." + last_name.lower()
        
            user_exists = ModifiedUser.objects.filter(email=email).exists()
            if user_exists:
                return Response({'msg': 'User exists'})
            
            user = ModifiedUser.objects.create(email=email,
                                        password=password,
                                        first_name=first_name,
                                        last_name=last_name,
                                        name=full_name,
                                        username=username)
            user.set_password(password)
            user.save()
            print(user)
            return Response({'msg': f'User {user} registered'})
        else:
            return Response({'msg': 'Please enter first name, last name, email and password'})
        

class Login(APIView):
    def post(self, request):
        ser = LoginSerializer(data=request.data)
        if ser.is_valid():
            email = ser.validated_data['email']
            password = ser.validated_data['password']
            print(email)
            print(password)
            user = authenticate(email=email,
                                password=password)
            print(user)
            if user:
                token, _ = Token.objects.get_or_create(user=user)
                request.session['token'] = token.key
                request.session['user_id'] = user.id
                return Response({'msg': f'{user} is logged in'})
            else:
                return Response({'msg': 'Check the credentials'})
            
        else:
            return Response({'msg': 'Please enter email and password'})
        
        
class Logout(APIView):
    permission_classes = [IsLoggedIn]
    
    def get(self, request):
        token = Token.objects.filter(key=request.session['token'])
        user = ModifiedUser.objects.get(id=token[0].user_id)
        token.delete()
        del request.session['token']
        del request.session['user_id']
        return Response({'msg': f'{user} is logged out'})

    
    
class GetAllUsers(ListAPIView):
    permission_classes = [IsLoggedIn]
    pagination_class = TenEntriesPage
    serializer_class = UserSerializer
    
    def get_queryset(self):
        users = ModifiedUser.objects.all().order_by('id')
        users = self.filter_queryset(users)
        return users
    
    def filter_queryset(self, queryset):
        name = self.request.query_params.get('name')
        email = self.request.query_params.get('email')
        if name:
            queryset = queryset.filter(name__icontains=name)
        elif email:
            queryset = queryset.filter(email__icontains=email)
        return queryset
    
    def get(self, request):
        # users = ModifiedUser.objects.all().order_by('id')
        # name = request.query_params.get('name')
        # email = request.query_params.get('email')
        # if name:
        #     users = users.filter(name__icontains=name)
        # elif email:
        #     users = users.filter(email__icontains=email)
        # page = PageNumberPagination()
        # page.page_size = 10
        # users = page.paginate_queryset(users, request)
        # ser = UserSerializer(users, many=True)
        # response = page.get_paginated_response(ser.data)
        # return response
        return self.list(request)
        
    
    

        
    
            




from .serializers import UserSerializer
from .models import ModifiedUser
from .permissions import IsLoggedIn

from rest_framework.views import APIView
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework.throttling import UserRateThrottle
from rest_framework.pagination import PageNumberPagination
from rest_framework.mixins import ListModelMixin
from rest_framework.generics import ListAPIView
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token


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
        
        
class Login(ObtainAuthToken):
    
    def post(self, request):
        ser = self.serializer_class(data=request.data,
                                    context={'request': request})
        ser.is_valid(raise_exception=True)
        user = ser.validated_data.get('user')
        print(user.id)
        token, _ = Token.objects.get_or_create(user=user)
        print(token.key)
        self.request.session['token'] = token.key
        self.request.session['user_id'] = user.id
        # self.request.user = 
        
        return Response({'msg': 'User is logged in'})
        
        
        
class Logout(APIView):
    permission_classes = [IsLoggedIn]
    
    def post(self, request):
        Token.objects.get(key=request.session['token']).delete()
        del request.session['token']
        return Response({'msg': 'Token deleted'})
    
    
class GetAllUsers(APIView):
    permission_classes = [IsLoggedIn]
    
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
    
    

        
    
            




from .serializers import UserSerializer
from .models import ModifiedUser
from .permissions import IsLoggedIn
from .pagination import TenEntriesPage

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
            return Response({'msg': f'User {u} is created'})
        else:
            return Response({'msg': 'Please fill name, username, email and password'})    
        
        
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
        
        return Response({'msg': f'{user} is logged in'})
        
        
        
class Logout(APIView):
    permission_classes = [IsLoggedIn]
    
    def post(self, request):
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
        
    
    

        
    
            




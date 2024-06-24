from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token
from . import views


urlpatterns = [
    path('', views.GetAllUsers.as_view()),
    path('registration/', views.UserRegistration.as_view()),
    path('login/', views.Login.as_view()),
    path('logout/', views.Logout.as_view()),
]

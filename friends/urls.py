from django.urls import path
from . import views


urlpatterns = [
    path('', views.Friends.as_view()),
    path('requests/', views.GetPendingFriendRequests.as_view()),
    path('requests/send/', views.SendFriendRequest.as_view()),
    path('requests/manage/', views.ManageFriendRequest.as_view()),
]

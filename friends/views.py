from rest_framework.views import APIView
from rest_framework.response import Response

from users.models import ModifiedUser
from users.permissions import IsLoggedIn
from .models import FriendRequests
from .serializers import FriendsSerializer, UserSerializer
from .throttlers import UserLevelThrottle


class SendFriendRequest(APIView):
    permission_classes = [IsLoggedIn]
    throttle_classes = [UserLevelThrottle]
    
    def post(self, request):
        me = ModifiedUser.objects.get(id=request.session['user_id'])
        they = ModifiedUser.objects.get(id=request.data.get('who'))
        
        FriendRequests.objects.create(sender_id=me,
                                        status='pending',
                                        receiver_id=they)
        
        return Response({'msg': 'Friend request sent'})
    
    
class GetPendingFriendRequests(APIView):
    permission_classes = [IsLoggedIn]
    
    def get(self, request):
        me = ModifiedUser.objects.get(id=request.session['user_id'])
        frnd_requests = FriendRequests.objects.filter(receiver_id=me, status='pending')
        ser = FriendsSerializer(frnd_requests, many=True)
        return Response(ser.data)
    
    
class ManageFriendRequest(APIView):
    permission_classes = [IsLoggedIn]
    
    def post(self, request):
        me = ModifiedUser.objects.get(id=request.session['user_id'])
        they = ModifiedUser.objects.get(id=request.data.get('who'))
        action = request.data.get('action')
        
        if action == 'accept':
            FriendRequests.objects.filter(receiver_id=me,
                                          sender_id=they).update(status='accepted')
        elif action == 'reject':
            FriendRequests.objects.filter(receiver_id=me,
                                          sender_id=they).update(status='rejected')
        
        return Response({'msg': 'Friend request action is done'})
    
    
class Friends(APIView):
    permission_classes = [IsLoggedIn]
    
    def get(self, request):
        me = ModifiedUser.objects.get(id=request.session['user_id'])
        print(me)
        sent_reqs = FriendRequests.objects.filter(sender_id=me,
                                                status='accepted').values_list('receiver_id', flat=True)
        print(sent_reqs)
        received_reqs = FriendRequests.objects.filter(receiver_id=me,
                                                    status='accepted').values_list('sender_id', flat=True)
        print(received_reqs)
        friend_ids = sent_reqs.union(received_reqs)
        queryset = ModifiedUser.objects.filter(id__in=friend_ids)
        ser = UserSerializer(queryset, many=True)
        return Response(ser.data)

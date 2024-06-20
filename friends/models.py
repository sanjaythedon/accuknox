from django.db import models
from users.models import ModifiedUser


class FriendRequests(models.Model):
    sender_id = models.ForeignKey(ModifiedUser, on_delete=models.CASCADE, related_name='sender_id')
    status = models.CharField(max_length=100)
    receiver_id = models.ForeignKey(ModifiedUser, on_delete=models.CASCADE, related_name='receiver_id')

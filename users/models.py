from django.db import models
from django.contrib.auth.models import User


class ModifiedUser(User):
    name = models.CharField(max_length=100)
    
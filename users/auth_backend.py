from typing import Any
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
from django.http.request import HttpRequest
from django.contrib.auth.models import AbstractBaseUser

        
class EmailBackend(ModelBackend):
    def authenticate(self, request: HttpRequest, username: str | None = ..., password: str | None = ..., email: str | None = ..., **kwargs: Any) -> AbstractBaseUser | None:
        user_model = get_user_model()
        try:
            user = user_model.objects.get(email=email)
        except user_model.DoesNotExist:
            return None
        
        if user.check_password(password):
            return user
        return None
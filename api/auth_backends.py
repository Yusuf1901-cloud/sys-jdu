from django.contrib.auth.hashers import check_password
from django.contrib.auth.backends import ModelBackend
from .models import JduUser


class JduUserAuthenticationBackend(ModelBackend):
    def authenticate(self, request, jdu_id=None, password=None, **kwargs):
        try:
            user = JduUser.objects.get(jdu_id=jdu_id)
        except JduUser.DoesNotExist:
            return None

        if check_password(password, user.password):
            return user

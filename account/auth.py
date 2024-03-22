from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model


class PhoneModelBackend(ModelBackend):
    def authenticate(self, request, phone_number=None):
        User = get_user_model()
        try:
            user = User.objects.get(phone_number=phone_number)
            return user
        except User.DoesNotExist:
            return None

    def get_user(self, user_id):
        User_model=get_user_model()
        try:
            return User_model.objects.get(pk=user_id)
        except User_model.DoesNotExist:
            return None
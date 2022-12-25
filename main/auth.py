from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model

from main.manager import UserManager

UserModel = get_user_model()


class UserAuthBackend(ModelBackend):
    def authenticate(self, request, phone_number=None, password=None, **kwargs):
        if phone_number is None or password is None:
            return
        phone_number = UserModel.normalize_username(phone_number)
        try:
            user = UserModel._default_manager.get_by_natural_key(phone_number)
        except UserModel.DoesNotExist:
            UserModel().set_password(password)

        else:
            if user.check_password(password):
                return user


class UserAuthUsernameIsPhone(UserAuthBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        return super().authenticate(request, phone_number=username, password=password)

from django.contrib.auth.backends import BaseBackend
from django.contrib.auth import get_user_model

from main.manager import UserManager

UserModel = get_user_model()


class UserAuthBackend(BaseBackend):
    def authenticate(self, request, phone_number=None, password=None):
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

    def get_user(self, user_id):
        try:
            user = UserManager.get(pk=user_id)
        except UserModel.DoesNotExist:
            return None
        return user

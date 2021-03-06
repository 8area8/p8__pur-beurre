"""Custom authentitace with email.

Add in settings.py :
AUTHENTICATION_BACKENDS = ['path.to.class.EmailAuthenticate']
"""

from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model


class EmailAuthenticate(ModelBackend):
    """Extended backend."""

    def authenticate(self, request, username=None, password=None, **kwargs):
        """Authenticate method."""
        UserModel = get_user_model()
        if username is None:
            username = kwargs.get(UserModel.USERNAME_FIELD)
        try:
            if '@' in username:
                UserModel.USERNAME_FIELD = 'email'
            else:
                UserModel.USERNAME_FIELD = 'username'

            user = UserModel._default_manager.get_by_natural_key(username)
        except UserModel.DoesNotExist:
            UserModel().set_password(password)
        else:
            if user.check_password(password):
                if self.user_can_authenticate(user):
                    if user.is_active:
                        return user

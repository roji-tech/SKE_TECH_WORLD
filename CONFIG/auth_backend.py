from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.backends import BaseBackend
from django.contrib.auth import get_user_model

from main.models.models import School
from main.models.users import User

UserModel: User = get_user_model()


class SchoolEmailBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        school: School = request.school  # Extract school from request

        print(kwargs, UserModel.USERNAME_FIELD)
        print("========SchoolEmailBackend=========")
        if username is None:
            # username = kwargs.get(UserModel.USERNAME_FIELD)
            username = kwargs.get("email")

        print(kwargs, username, password, school, request.school_code)

        if username is None or password is None or school is None:
            return

        print("login", username, password)

        try:
            if school:
                login_email = f"{username}{UserModel.ES_Sep}{school.id}"
            else:
                login_email = f"{username}"

            print("login email", username, password, login_email)
            user = UserModel.objects.get(login_email=login_email)
            # user = UserModel._default_manager.get_by_natural_key(username)
            print(user)
            if user.check_password(password):
                return user
        except UserModel.DoesNotExist as e:
            UserModel().set_password(password)
            print(e)
            return None

        else:
            print("else part of SchoolEmailBackend")
            if user.check_password(password) and self.user_can_authenticate(user):
                return user
        return None

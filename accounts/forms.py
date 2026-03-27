from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserChangeForm, BaseUserCreationForm

UserModel = get_user_model()


class AppUserCreationForm(BaseUserCreationForm):
    class Meta:
        model = UserModel
        fields = ["email"]


class AppUserChangeForm(UserChangeForm):
    class Meta(UserChangeForm.Meta):
        model = UserModel


from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User

UserModel = get_user_model()

class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']

class SetUnusablePasswordForm(forms.Form):
    user = forms.ModelChoiceField(
        queryset=UserModel.objects.order_by('username'),
        label="Потребител",
    )
from django.contrib.auth.forms import BaseUserCreationForm, UserChangeForm

from .models import User


class AdminUserCreationForm(BaseUserCreationForm):
    class Meta:
        model = User
        fields = ("email", "phone", "name", "surname")


class AdminUserChangeForm(UserChangeForm):
    class Meta:
        model = User
        fields = "__all__"
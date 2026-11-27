from django import forms
from django.contrib.auth.forms import (
    BaseUserCreationForm,
    UserChangeForm,
    AuthenticationForm,
)

from .models import User


class UserCreationForm(BaseUserCreationForm):
    class Meta:
        model = User
        fields = ("email", "phone", "name", "surname")


class AdminUserChangeForm(UserChangeForm):
    class Meta:
        model = User
        fields = "__all__"


class LoginForm(AuthenticationForm):
    username = forms.EmailField(label="Email")


class ProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ("name", "surname", "email", "avatar", "about", "phone", "github_url")
        widgets = {"about": forms.Textarea(attrs={"rows": 4})}

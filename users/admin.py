from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin

from .forms import AdminUserChangeForm, AdminUserCreationForm
from .models import User


@admin.register(User)
class UserAdmin(DjangoUserAdmin):
    add_form = AdminUserCreationForm
    form = AdminUserChangeForm
    list_display = ("email", "phone", "name", "surname", "is_active", "is_staff")
    list_filter = ("is_active", "is_staff", "is_superuser")
    search_fields = ("email", "phone", "name", "surname")
    ordering = ("-date_joined", "-id")
    readonly_fields = ("last_login", "date_joined")
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        ("Профиль", {
            "fields": ("name", "surname", "avatar", "phone", "github_url", "about"),
        }),
        ("Права доступа", {
            "fields": (
                "is_active", "is_staff", "is_superuser", "groups", "user_permissions",
            ),
        }),
        ("Даты", {"fields": ("last_login", "date_joined")}),
    )
    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": ("email", "phone", "name", "surname", "password1", "password2"),
        }),
    )
    filter_horizontal = ("groups", "user_permissions")

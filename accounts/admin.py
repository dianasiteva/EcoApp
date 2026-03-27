from django.contrib import admin
from django.contrib.admin import ModelAdmin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.admin import GroupAdmin as BaseGroupAdmin
from django.contrib.auth.forms import AdminPasswordChangeForm
from django.contrib.auth.models import Group, User
from django.utils.translation import gettext_lazy as _
from accounts.forms import AppUserChangeForm, AppUserCreationForm

UserModel = get_user_model()

admin.site.unregister(Group)


@admin.register(UserModel)
class UserAdmin(UserAdmin):
    form = AppUserChangeForm
    add_form = AppUserCreationForm
    change_password_form = AdminPasswordChangeForm

    fieldsets = (
        (None, {"fields": ("password",)}),
        (_("Personal info"), {"fields": ("email",)}),
        (
            _("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
        (_("Important dates"), {"fields": ("last_login",)}),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("email", "usable_password", "password1", "password2"),
            },
        ),
    )
    list_display = ("email", "is_staff")
    list_filter = ("is_staff", "is_superuser", "is_active", "groups")
    search_fields = ("email",)
    ordering = ("email",)


@admin.register(Group)
class GroupAdmin(BaseGroupAdmin, ModelAdmin):
    pass
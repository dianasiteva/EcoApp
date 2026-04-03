from django.contrib import admin
from django.contrib.admin import ModelAdmin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.admin import GroupAdmin as BaseGroupAdmin
from django.contrib.auth.forms import AdminPasswordChangeForm
from django.contrib.auth.models import Group
from django.utils.translation import gettext_lazy as _
from accounts.forms import AppUserChangeForm, AppUserCreationForm

UserModel = get_user_model()

admin.site.unregister(Group)


@admin.register(UserModel)
class UserAdmin(UserAdmin):
    form = AppUserChangeForm
    add_form = AppUserCreationForm
    change_password_form = AdminPasswordChangeForm

    readonly_fields = ('last_login', 'date_joined')

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
        (_("Important dates"), {"fields": ("last_login", "date_joined")}),
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
    list_display = ("email", "get_groups", "is_staff", "is_superuser", "is_active","date_joined")
    list_filter = ("is_staff", "is_superuser", "is_active", "groups", "date_joined")
    search_fields = ("email",)
    ordering = ("email",)

    def get_groups(self, obj):
        return ", ".join([g.name for g in obj.groups.all()])

    get_groups.short_description = "Групи"



@admin.register(Group)
class GroupAdmin(BaseGroupAdmin, ModelAdmin):
    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

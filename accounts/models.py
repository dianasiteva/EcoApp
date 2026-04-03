from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import User, PermissionsMixin
from django.db import models


from accounts.managers import AppUserManager


class AppUser(AbstractBaseUser, PermissionsMixin):
    USERNAME_FIELD = "email"

    email = models.EmailField(
        unique=True,
    )

    is_active = models.BooleanField(
        default=True,
    )

    is_staff = models.BooleanField(
        default=False,
    )

    date_joined = models.DateTimeField(auto_now_add=True)

    objects = AppUserManager()

    class Meta:
        verbose_name = "Регистриран потребител"
        verbose_name_plural = "Потребители"

    def __str__(self) -> str:
        return self.email
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

from caldy.models.base import BaseIDModel


class UserManager(BaseUserManager):
    def create_superuser(self, email, full_name, password):
        user = self.model(
            email=self.normalize_email(email),
            full_name=full_name
        )
        user.set_password(password)
        user.is_superuser = True
        user.save(using=self._db)

        return user


class User(BaseIDModel, AbstractBaseUser):
    email = models.EmailField(unique=True)
    full_name = models.CharField(max_length=128, blank=True, null=True)
    is_superuser = models.BooleanField(default=False)

    ID_PREFIX = "usr"
    REQUIRED_FIELDS = ["full_name"]
    USERNAME_FIELD = "email"

    objects = UserManager()

    class Meta:
        db_table = "users"

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_superuser

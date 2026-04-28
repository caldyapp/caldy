from django.core.exceptions import ValidationError
from django.db import models
from django.conf import settings

from caldy.models.base import BaseIDModel


class Account(BaseIDModel):
    handle = models.SlugField(max_length=128, unique=True)
    owner_user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name="owned_accounts",
    )
    owner_org = models.ForeignKey(
        "caldy.Organization",
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name="owned_accounts",
    )
    display_name = models.CharField(max_length=128, blank=True)
    location = models.CharField(max_length=256, blank=True, null=True)
    is_public = models.BooleanField(default=True)
    avatar_url = models.URLField(blank=True, null=True)

    ID_PREFIX = "acc"

    class Meta:
        db_table = "accounts"
        constraints = [
            models.CheckConstraint(
                condition=(
                    models.Q(owner_user__isnull=False, owner_org__isnull=True)
                    | models.Q(owner_user__isnull=True, owner_org__isnull=False)
                ),
                name="account_owner_exactly_one",
            )
        ]

    def clean(self):
        if bool(self.owner_user_id) == bool(self.owner_org_id):
            raise ValidationError("An account must have exactly one owner: a user or an organization.")

    @property
    def owner(self):
        return self.owner_user or self.owner_org

    @property
    def owner_type(self):
        if self.owner_user_id:
            return "user"
        if self.owner_org_id:
            return "organization"
        return None

from django.db import models
from django.conf import settings

from caldy.models.base import BaseIDModel


class MembershipRoleChoice(models.TextChoices):
    OWNER = ("owner", "Owner")
    ADMIN = ("admin", "Admin")
    STAFF = ("staff", "Staff")


class Organization(BaseIDModel):
    name = models.CharField(max_length=256)
    website = models.URLField(blank=True, null=True)
    about = models.TextField(blank=True, null=True)

    members = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        through="OrganizationMembership",
        related_name="organizations",
    )

    ID_PREFIX = "org"

    class Meta:
        db_table = "organizations"


class OrganizationMembership(BaseIDModel):
    organization = models.ForeignKey(
        "caldy.Organization", on_delete=models.CASCADE, related_name="memberships"
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="org_memberships",
    )
    role = models.CharField(
        max_length=32,
        choices=MembershipRoleChoice.choices,
        default=MembershipRoleChoice.STAFF,
    )

    ID_PREFIX = "orgm"

    class Meta:
        db_table = "organization_memberships"
        constraints = [
            models.UniqueConstraint(
                fields=["organization", "user"], name="uniq_user_org_membership"
            )
        ]

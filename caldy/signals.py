from django.db.models.signals import post_save
from django.dispatch import receiver

from caldy.models.user import User


@receiver(post_save, sender=User)
def create_account_for_new_user(sender, instance, created, **kwargs):
    if not created:
        return

    from caldy.models.account import Account

    base_handle = instance.email.split("@")[0].lower()
    handle = base_handle
    suffix = 1

    while Account.objects.filter(handle=handle).exists():
        handle = f"{base_handle}{suffix}"
        suffix += 1

    Account.objects.create(
        owner_user=instance,
        handle=handle,
        display_name=instance.full_name or "",
    )

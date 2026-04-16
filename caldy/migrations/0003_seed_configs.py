from django.db import migrations


SEED_CONFIGS = [
    # -------------------------------------------------------------------------
    # site — general identity and contact info
    # -------------------------------------------------------------------------
    {
        "key": "SITE_NAME",
        "raw_value": "Caldy",
        "value_type": "str",
        "group": "site",
        "is_secret": False,
        "description": "Public display name of the application.",
    },
    {
        "key": "SITE_URL",
        "raw_value": "https://example.com",
        "value_type": "str",
        "group": "site",
        "is_secret": False,
        "description": "Canonical public URL (used in emails, links, etc.).",
    },
    {
        "key": "SUPPORT_EMAIL",
        "raw_value": "support@example.com",
        "value_type": "str",
        "group": "site",
        "is_secret": False,
        "description": "Email address shown to users for support requests.",
    },
    {
        "key": "CONTACT_EMAIL",
        "raw_value": "contact@example.com",
        "value_type": "str",
        "group": "site",
        "is_secret": False,
        "description": "General inbound contact email address.",
    },
    # -------------------------------------------------------------------------
    # auth — sign-up, login, and session policy
    # -------------------------------------------------------------------------
    {
        "key": "ALLOW_SIGN_UP",
        "raw_value": "true",
        "value_type": "bool",
        "group": "auth",
        "is_secret": False,
        "description": "Allow new users to self-register. Set to false to make the app invite-only.",
    },
    {
        "key": "EMAIL_VERIFICATION_REQUIRED",
        "raw_value": "true",
        "value_type": "bool",
        "group": "auth",
        "is_secret": False,
        "description": "Require users to verify their email before accessing the app.",
    },
    {
        "key": "PASSWORD_MIN_LENGTH",
        "raw_value": "8",
        "value_type": "int",
        "group": "auth",
        "is_secret": False,
        "description": "Minimum number of characters required for a password.",
    },
    {
        "key": "MAX_LOGIN_ATTEMPTS",
        "raw_value": "5",
        "value_type": "int",
        "group": "auth",
        "is_secret": False,
        "description": "Number of consecutive failed logins before an account is locked.",
    },
    {
        "key": "SESSION_TIMEOUT_MINUTES",
        "raw_value": "60",
        "value_type": "int",
        "group": "auth",
        "is_secret": False,
        "description": "Idle session timeout in minutes.",
    },
    # -------------------------------------------------------------------------
    # email — outbound mail transport
    # -------------------------------------------------------------------------
    {
        "key": "EMAIL_BACKEND",
        "raw_value": "django.core.mail.backends.console.EmailBackend",
        "value_type": "str",
        "group": "email",
        "is_secret": False,
        "description": "Django email backend class. Switch to smtp for production.",
    },
    {
        "key": "EMAIL_HOST",
        "raw_value": "localhost",
        "value_type": "str",
        "group": "email",
        "is_secret": False,
        "description": "SMTP server hostname.",
    },
    {
        "key": "EMAIL_PORT",
        "raw_value": "587",
        "value_type": "int",
        "group": "email",
        "is_secret": False,
        "description": "SMTP server port.",
    },
    {
        "key": "EMAIL_USE_TLS",
        "raw_value": "true",
        "value_type": "bool",
        "group": "email",
        "is_secret": False,
        "description": "Use TLS when connecting to the SMTP server.",
    },
    {
        "key": "EMAIL_HOST_USER",
        "raw_value": "",
        "value_type": "str",
        "group": "email",
        "is_secret": False,
        "description": "SMTP authentication username.",
    },
    {
        "key": "EMAIL_HOST_PASSWORD",
        "raw_value": "",
        "value_type": "str",
        "group": "email",
        "is_secret": True,
        "description": "SMTP authentication password.",
    },
    {
        "key": "DEFAULT_FROM_EMAIL",
        "raw_value": "noreply@example.com",
        "value_type": "str",
        "group": "email",
        "is_secret": False,
        "description": "Default sender address used for outgoing emails.",
    },
    # -------------------------------------------------------------------------
    # storage — file and media storage (S3 / django-storages)
    # -------------------------------------------------------------------------
    {
        "key": "AWS_ACCESS_KEY_ID",
        "raw_value": "",
        "value_type": "str",
        "group": "storage",
        "is_secret": True,
        "description": "AWS access key ID for S3 access.",
    },
    {
        "key": "AWS_SECRET_ACCESS_KEY",
        "raw_value": "",
        "value_type": "str",
        "group": "storage",
        "is_secret": True,
        "description": "AWS secret access key for S3 access.",
    },
    {
        "key": "AWS_STORAGE_BUCKET_NAME",
        "raw_value": "",
        "value_type": "str",
        "group": "storage",
        "is_secret": False,
        "description": "S3 bucket name for media and file storage.",
    },
    {
        "key": "AWS_S3_REGION_NAME",
        "raw_value": "us-east-1",
        "value_type": "str",
        "group": "storage",
        "is_secret": False,
        "description": "AWS region where the S3 bucket is located.",
    },
]


def seed_configs(apps, schema_editor):
    Config = apps.get_model("caldy", "Config")
    for data in SEED_CONFIGS:
        Config.objects.get_or_create(key=data["key"], defaults=data)


def unseed_configs(apps, schema_editor):
    Config = apps.get_model("caldy", "Config")
    keys = [d["key"] for d in SEED_CONFIGS]
    Config.objects.filter(key__in=keys).delete()


class Migration(migrations.Migration):

    dependencies = [
        ("caldy", "0002_config"),
    ]

    operations = [
        migrations.RunPython(seed_configs, reverse_code=unseed_configs),
    ]

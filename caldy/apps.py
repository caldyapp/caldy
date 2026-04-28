from django.apps import AppConfig


class CaldyConfig(AppConfig):
    name = "caldy"

    def ready(self):
        import caldy.signals  # noqa: F401

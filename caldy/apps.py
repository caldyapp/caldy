from django.apps import AppConfig


class CaldyConfig(AppConfig):
    name = "caldy"

    def ready(self):
        # Do NOT query the DB here — the ORM is not safely usable during
        # app initialisation and Django will emit a RuntimeWarning.
        # config._fetch_all() is lru_cache'd and runs lazily on first access,
        # which happens naturally during request/task handling after Django is
        # fully up.  Signal handlers below keep the cache fresh at runtime.
        self._connect_signals()

    def _connect_signals(self):
        from django.db.models.signals import post_delete, post_save

        from caldy.config import config
        from caldy.models.config import Config

        def on_config_change(sender, **kwargs):
            config.reload()

        post_save.connect(on_config_change, sender=Config, weak=False)
        post_delete.connect(on_config_change, sender=Config, weak=False)

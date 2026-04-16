"""
DB-backed config loader using Django's cache framework (Redis).

Usage:
    from caldy.config import config
    config.get("EMAIL_HOST", default="localhost")

All Config rows are stored as a single dict under CACHE_KEY.  Because Django's
cache backend is used, the cache is shared across all workers — unlike
lru_cache which is per-process.

Lifecycle:
  - config.get()      → cache hit: free.  cache miss: queries DB, fills cache.
  - config.invalidate() → deletes the cache key; next get() re-queries DB.
  - config.reload()   → invalidate + re-fetch + patch Django settings.
                        Called by post_save/post_delete signals on Config.

At settings.py import time Django's cache isn't ready, so config.get() falls
back to the supplied default silently.
"""

import logging

logger = logging.getLogger(__name__)

CACHE_KEY = "caldy:configs"

CACHE_TIMEOUT = 60 * 60 * 24 * 7  # 7 days

_BOOTSTRAP_KEYS = frozenset(
    {
        "SECRET_KEY",
        "DEBUG",
        "DATABASES",
        "CACHES",
        "INSTALLED_APPS",
        "MIDDLEWARE",
        "ALLOWED_HOSTS",
    }
)


def _fetch_all() -> dict:
    """Return {key: typed_value} for all Config rows.

    Checks Django's cache first.  On a miss, queries the DB and fills the
    cache.  Failures (cache or DB not ready) propagate to the caller so they
    are never silently cached.
    """
    from django.core.cache import cache

    cached = cache.get(CACHE_KEY)
    if cached is not None:
        return cached

    from caldy.models.config import Config

    data = {row.key: row.typed_value for row in Config.objects.all()}
    cache.set(CACHE_KEY, data, CACHE_TIMEOUT)
    return data


class DBConfig:
    def get(self, key: str, default=None):
        """Return the value for *key*, or *default* if missing or unavailable."""
        try:
            return _fetch_all().get(key, default)
        except Exception:
            logger.debug("Config cache/DB not available yet; using default for '%s'", key)
            return default

    def invalidate(self):
        """Delete the cache entry so the next get() re-queries the DB."""
        try:
            from django.core.cache import cache
            cache.delete(CACHE_KEY)
        except Exception:
            pass

    def reload(self):
        """Invalidate, re-fetch from DB, and patch Django settings.

        Called by signal handlers when a Config row changes.
        """
        from django.conf import settings as django_settings

        self.invalidate()

        try:
            all_settings = _fetch_all()
        except Exception:
            logger.warning("Config reload failed — cache/DB may not be ready.")
            return

        for key, value in all_settings.items():
            if key in _BOOTSTRAP_KEYS:
                continue
            setattr(django_settings, key, value)
            logger.debug("Config: applied %s to Django settings", key)


config = DBConfig()

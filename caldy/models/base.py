import uuid
from django.db import models


class BaseIDModel(models.Model):
    id = models.CharField(max_length=64, primary_key=True, editable=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    ID_PREFIX = None

    class Meta:
        abstract = True

    def __str__(self):
        return f"{self.__class__.__name__} <{self.pk or 'NA'}>"

    def save(self, *args, **kwargs):
        if self._state.adding:
            if not self.ID_PREFIX:
                raise ValueError(f"{self.__class__.__name__} needs to add ID PREFIX")
            if not self.id:
                self.id = f"{self.ID_PREFIX}_{uuid.uuid7().hex.lower()}"
        return super().save(*args, **kwargs)

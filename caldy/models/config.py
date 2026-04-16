import json

from django.db import models


class Config(models.Model):
    class ValueType(models.TextChoices):
        STR = ("str", "String")
        INT = ("int", "Integer")
        BOOL = ("bool", "Boolean")
        FLOAT = ("float", "Float")
        JSON = ("json", "JSON")

    key = models.CharField(max_length=255, primary_key=True)
    raw_value = models.TextField()
    value_type = models.CharField(
        max_length=10, choices=ValueType, default=ValueType.STR
    )
    group = models.CharField(max_length=100, blank=True, db_index=True)
    is_secret = models.BooleanField(default=False)
    description = models.TextField(blank=True, null=True)

    class Meta:
        db_table = "configs"
        ordering = ["group", "key"]

    def __str__(self):
        return f"{self.group}.{self.key}" if self.group else self.key

    @property
    def typed_value(self):
        if self.value_type == self.ValueType.INT:
            return int(self.raw_value)
        if self.value_type == self.ValueType.BOOL:
            return self.raw_value.strip().lower() in ("true", "1", "yes")
        if self.value_type == self.ValueType.FLOAT:
            return float(self.raw_value)
        if self.value_type == self.ValueType.JSON:
            return json.loads(self.raw_value)
        return self.raw_value

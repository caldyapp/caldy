from django.db import models

from caldy.models.base import BaseIDModel


class Weekday(models.IntegerChoices):
    MONDAY = (0, "Monday")
    TUESDAY = (1, "Tuesday")
    WEDNESDAY = (2, "Wednesday")
    THURSDAY = (3, "Thursday")
    FRIDAY = (4, "Friday")
    SATURDAY = (5, "Saturday")
    SUNDAY = (6, "Sunday")


class Schedule(BaseIDModel):
    account = models.ForeignKey(
        "caldy.Account",
        on_delete=models.CASCADE,
        related_name="schedules",
    )
    name = models.CharField(max_length=256)
    timezone = models.CharField(max_length=64, default="UTC")
    is_default = models.BooleanField(default=False)

    ID_PREFIX = "sch"

    class Meta:
        db_table = "schedules"
        constraints = [
            models.UniqueConstraint(
                fields=["account"],
                condition=models.Q(is_default=True),
                name="uniq_default_schedule_per_account",
            )
        ]

    def __str__(self):
        return f"{self.name} ({'default' if self.is_default else self.timezone})"


class ScheduleSlot(BaseIDModel):
    schedule = models.ForeignKey(
        "caldy.Schedule",
        on_delete=models.CASCADE,
        related_name="slots",
    )
    weekday = models.IntegerField(choices=Weekday.choices)
    start_time = models.TimeField()
    end_time = models.TimeField()

    ID_PREFIX = "schs"

    class Meta:
        db_table = "schedule_slots"
        ordering = ["weekday", "start_time"]

    def __str__(self):
        return f"{self.get_weekday_display()} {self.start_time}–{self.end_time}"

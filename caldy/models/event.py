from django.db import models

from caldy.models.base import BaseIDModel


class EventKind(models.TextChoices):
    MEETING = ("meeting", "Meeting")
    PUBLIC_EVENT = ("public_event", "Public Event")
    SERVICE = ("service", "Service")


class EventLocationType(models.TextChoices):
    IN_PERSON = ("in_person", "In Person")
    VIRTUAL = ("virtual", "Virtual")
    PHONE = ("phone", "Phone")


class EventInstanceStatus(models.TextChoices):
    SCHEDULED = ("scheduled", "Scheduled")
    CANCELLED = ("cancelled", "Cancelled")
    COMPLETED = ("completed", "Completed")


class Event(BaseIDModel):
    account = models.ForeignKey(
        "caldy.Account",
        on_delete=models.CASCADE,
        related_name="events",
    )
    title = models.CharField(max_length=256)
    description = models.TextField(blank=True, null=True)
    kind = models.CharField(
        max_length=32,
        choices=EventKind.choices,
        default=EventKind.MEETING,
    )
    duration = models.PositiveIntegerField(help_text="Duration in minutes")
    capacity = models.PositiveIntegerField(
        null=True,
        blank=True,
        help_text="Max attendees. Null means unlimited.",
    )
    location_type = models.CharField(
        max_length=32,
        choices=EventLocationType.choices,
        default=EventLocationType.IN_PERSON,
    )
    schedule = models.ForeignKey(
        "caldy.Schedule",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="events",
    )
    is_active = models.BooleanField(default=True)
    is_recurring = models.BooleanField(default=False)
    rrule = models.CharField(
        max_length=512,
        blank=True,
        null=True,
        help_text="iCal RRULE string. e.g. FREQ=WEEKLY;BYDAY=MO. Only set when is_recurring=True.",
    )
    starts_at = models.DateTimeField(
        null=True,
        blank=True,
        help_text="Start of the one-off event or the recurrence series.",
    )

    ID_PREFIX = "evt"

    class Meta:
        db_table = "events"

    def __str__(self):
        return f"{self.title} ({self.get_kind_display()})"


class EventInstance(BaseIDModel):
    event = models.ForeignKey(
        "caldy.Event",
        on_delete=models.CASCADE,
        related_name="instances",
    )
    status = models.CharField(
        max_length=32,
        choices=EventInstanceStatus.choices,
        default=EventInstanceStatus.SCHEDULED,
    )
    starts_at = models.DateTimeField()
    ends_at = models.DateTimeField()
    location = models.CharField(
        max_length=512,
        blank=True,
        null=True,
        help_text="Address or meeting link. Overrides event-level location if set.",
    )

    ID_PREFIX = "evti"

    class Meta:
        db_table = "event_instances"
        ordering = ["starts_at"]

    def __str__(self):
        return f"{self.event.title} @ {self.starts_at}"

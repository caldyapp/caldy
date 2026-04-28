import secrets
import string

from django.db import models
from django.utils.crypto import get_random_string
from caldy.models.base import BaseIDModel


class BookingStatus(models.TextChoices):
    PENDING = ("pending", "Pending")
    CONFIRMED = ("confirmed", "Confirmed")
    CANCELLED = ("cancelled", "Cancelled")
    NO_SHOW = ("no_show", "No Show")


class Booking(BaseIDModel):
    event_instance = models.ForeignKey(
        "caldy.EventInstance",
        on_delete=models.CASCADE,
        related_name="bookings",
    )
    status = models.CharField(
        max_length=32,
        choices=BookingStatus.choices,
        default=BookingStatus.PENDING,
    )
    reference = models.CharField(max_length=8, unique=True, blank=True, editable=False)
    guest_name = models.CharField(max_length=256)
    guest_email = models.EmailField()
    guest_phone = models.CharField(max_length=32, blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    booked_at = models.DateTimeField(auto_now_add=True)
    cancelled_at = models.DateTimeField(null=True, blank=True)

    ID_PREFIX = "bkg"

    class Meta:
        db_table = "bookings"
        ordering = ["-booked_at"]

    def save(self, *args, **kwargs):
        if self._state.adding:
            self.reference = get_random_string(8).upper()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.reference} — {self.guest_name}"

from django import forms
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.contrib.auth.models import Group
from django.core.exceptions import ValidationError

from caldy.models.user import User
from caldy.models.organization import Organization, OrganizationMembership
from caldy.models.account import Account
from caldy.models.schedule import Schedule, ScheduleSlot
from caldy.models.event import Event, EventInstance
from caldy.models.booking import Booking


# ── User ────────────────────────────────────────────────────────────

class UserCreationForm(forms.ModelForm):
    password1 = forms.CharField(label="Password", widget=forms.PasswordInput)
    password2 = forms.CharField(label="Password confirmation", widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ["email", "full_name"]

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = User
        fields = ["email", "full_name", "password", "is_superuser"]


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm
    list_display = ["email", "full_name", "is_superuser"]
    list_filter = ["is_superuser"]
    search_fields = ["email", "full_name"]
    ordering = ["email"]
    filter_horizontal = []
    fieldsets = [
        (None, {"fields": ["email", "password"]}),
        ("Personal info", {"fields": ["full_name"]}),
        ("Permissions", {"fields": ["is_superuser"]}),
    ]
    add_fieldsets = [
        (None, {"classes": ["wide"], "fields": ["email", "full_name", "password1", "password2"]}),
    ]


# ── Organization ────────────────────────────────────────────────────

class OrganizationMembershipInline(admin.TabularInline):
    model = OrganizationMembership
    extra = 0
    fields = ["user", "role"]


@admin.register(Organization)
class OrganizationAdmin(admin.ModelAdmin):
    list_display = ["name", "website", "created_at"]
    search_fields = ["name"]
    inlines = [OrganizationMembershipInline]


# ── Account ─────────────────────────────────────────────────────────

@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    list_display = ["handle", "display_name", "owner_type", "is_public", "location"]
    list_filter = ["is_public"]
    search_fields = ["handle", "display_name"]
    readonly_fields = ["owner_type"]


# ── Schedule ─────────────────────────────────────────────────────────

class ScheduleSlotInline(admin.TabularInline):
    model = ScheduleSlot
    extra = 1
    fields = ["weekday", "start_time", "end_time"]


@admin.register(Schedule)
class ScheduleAdmin(admin.ModelAdmin):
    list_display = ["name", "account", "timezone", "is_default"]
    list_filter = ["is_default"]
    search_fields = ["name", "account__handle"]
    inlines = [ScheduleSlotInline]


# ── Event ────────────────────────────────────────────────────────────

class EventInstanceInline(admin.TabularInline):
    model = EventInstance
    extra = 0
    fields = ["starts_at", "ends_at", "status", "location"]


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ["title", "account", "kind", "duration", "is_recurring", "is_active"]
    list_filter = ["kind", "is_recurring", "is_active", "location_type"]
    search_fields = ["title", "account__handle"]
    inlines = [EventInstanceInline]


@admin.register(EventInstance)
class EventInstanceAdmin(admin.ModelAdmin):
    list_display = ["event", "starts_at", "ends_at", "status"]
    list_filter = ["status"]
    search_fields = ["event__title"]
    ordering = ["starts_at"]


# ── Booking ──────────────────────────────────────────────────────────

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ["reference", "guest_name", "guest_email", "status", "booked_at"]
    list_filter = ["status"]
    search_fields = ["reference", "guest_name", "guest_email"]
    readonly_fields = ["reference", "booked_at"]
    ordering = ["-booked_at"]


admin.site.unregister(Group)

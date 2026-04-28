from django.contrib import admin
from django.urls import path

from caldy.views.accounts import LoginView, LogoutView, RegisterView
from caldy.views.home import HomeView
from caldy.views.manage.events import EventListView, EventNewView
from caldy.views.manage.schedules import ScheduleListView, ScheduleNewView
from caldy.views.manage.bookings import BookingListView

# fmt: off
manage_urlpatterns = [
    path("<slug:handle>/manage/events/",           EventListView.as_view(),    name="manage-event-list"),
    path("<slug:handle>/manage/events/new/",       EventNewView.as_view(),     name="manage-event-new"),
    path("<slug:handle>/manage/schedules/",        ScheduleListView.as_view(), name="manage-schedule-list"),
    path("<slug:handle>/manage/schedules/new/",    ScheduleNewView.as_view(),  name="manage-schedule-new"),
    path("<slug:handle>/manage/bookings/",         BookingListView.as_view(),  name="manage-booking-list"),
]

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", HomeView.as_view(), name="home"),
    path("accounts/login/", LoginView.as_view(), name="login"),
    path("accounts/register/", RegisterView.as_view(), name="register"),
    path("accounts/logout/", LogoutView.as_view(), name="logout"),
    *manage_urlpatterns,
]

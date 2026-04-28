from django.shortcuts import render
from django.views import View

from caldy.mixins import ManageBaseMixin


class ScheduleListView(ManageBaseMixin, View):
    def get(self, request, **kwargs):
        return render(request, "caldy/manage/schedules/schedule-list.html", self.get_context_data())


class ScheduleNewView(ManageBaseMixin, View):
    def get(self, request, **kwargs):
        return render(request, "caldy/manage/schedules/schedule-new.html", self.get_context_data())

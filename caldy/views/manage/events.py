from django.shortcuts import render
from django.views import View

from caldy.mixins import ManageBaseMixin


class EventListView(ManageBaseMixin, View):
    def get(self, request, **kwargs):
        return render(request, "caldy/manage/events/event-list.html", self.get_context_data())


class EventNewView(ManageBaseMixin, View):
    def get(self, request, **kwargs):
        return render(request, "caldy/manage/events/event-new.html", self.get_context_data())

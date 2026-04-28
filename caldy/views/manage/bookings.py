from django.shortcuts import render
from django.views import View

from caldy.mixins import ManageBaseMixin


class BookingListView(ManageBaseMixin, View):
    def get(self, request, **kwargs):
        return render(request, "caldy/manage/bookings/booking-list.html", self.get_context_data())

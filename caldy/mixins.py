from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404

from caldy.models import Account


class ManageBaseMixin(LoginRequiredMixin):
    def dispatch(self, request, *args, **kwargs):
        self.account = get_object_or_404(
            Account,
            handle=kwargs["handle"],
            owner_user=request.user,
        )
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        return {"account": self.account, **kwargs}

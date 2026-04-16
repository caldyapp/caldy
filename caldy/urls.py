from django.contrib import admin
from django.urls import path

from caldy.views.accounts import LoginView, LogoutView, RegisterView
from caldy.views.home import HomeView

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", HomeView.as_view(), name="home"),
    path("accounts/login/", LoginView.as_view(), name="login"),
    path("accounts/register/", RegisterView.as_view(), name="register"),
    path("accounts/logout/", LogoutView.as_view(), name="logout"),
]

from django.contrib import messages
from django.contrib.auth import login, logout
from django.shortcuts import redirect, render
from django.views import View

from caldy.forms import LoginForm, RegisterForm


class LoginView(View):
    template_name = "caldy/accounts/login.html"

    def get(self, request):
        if request.user.is_authenticated:
            return redirect("home")
        return render(request, self.template_name, {"form": LoginForm()})

    def post(self, request):
        form = LoginForm(request=request, data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            next_url = request.GET.get("next") or "home"
            return redirect(next_url if next_url.startswith("/") else "home")
        return render(request, self.template_name, {"form": form})


class RegisterView(View):
    template_name = "caldy/accounts/register.html"

    def get(self, request):
        if request.user.is_authenticated:
            return redirect("home")
        return render(request, self.template_name, {"form": RegisterForm()})

    def post(self, request):
        form = RegisterForm(data=request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "welcome to caldy.")
            return redirect("home")
        return render(request, self.template_name, {"form": form})


class LogoutView(View):
    def post(self, request):
        logout(request)
        return redirect("login")

    # Allow GET logout for convenience (nav link)
    def get(self, request):
        logout(request)
        return redirect("login")

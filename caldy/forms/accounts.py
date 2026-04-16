from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError

from caldy.models import User


class LoginForm(forms.Form):
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={"autofocus": True}),
    )
    password = forms.CharField(
        widget=forms.PasswordInput(),
        strip=False,
    )

    def __init__(self, request=None, *args, **kwargs):
        self.request = request
        self._user = None
        super().__init__(*args, **kwargs)

    def clean(self):
        cleaned = super().clean()
        email = cleaned.get("email")
        password = cleaned.get("password")

        if email and password:
            self._user = authenticate(self.request, username=email, password=password)
            if self._user is None:
                raise ValidationError("invalid email or password.")
            if not self._user.is_active:
                raise ValidationError("this account is inactive.")

        return cleaned

    def get_user(self):
        return self._user


class RegisterForm(forms.Form):
    full_name = forms.CharField(
        max_length=128,
        required=False,
        widget=forms.TextInput(),
    )
    email = forms.EmailField(
        widget=forms.EmailInput(),
    )
    password1 = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(),
        strip=False,
    )
    password2 = forms.CharField(
        label="Confirm password",
        widget=forms.PasswordInput(),
        strip=False,
    )

    def clean_email(self):
        email = self.cleaned_data["email"].lower()
        if User.objects.filter(email=email).exists():
            raise ValidationError("an account with this email already exists.")
        return email

    def clean(self):
        cleaned = super().clean()
        p1 = cleaned.get("password1")
        p2 = cleaned.get("password2")

        if p1 and p2 and p1 != p2:
            self.add_error("password2", "passwords do not match.")

        if p1:
            try:
                validate_password(p1)
            except ValidationError as e:
                self.add_error("password1", e)

        return cleaned

    def save(self):
        email = self.cleaned_data["email"]
        password = self.cleaned_data["password1"]
        full_name = self.cleaned_data.get("full_name", "")
        return User.objects.create_user(email=email, password=password, full_name=full_name)

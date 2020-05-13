from django import forms
from django.contrib.auth.models import User
from django.core.validators import RegexValidator
from django.contrib.auth.forms import AuthenticationForm


class UserLoginForm(AuthenticationForm):
    # personal_number = forms.CharField(
    #     widget=forms.TextInput(
    #         attrs={"class": "special", "placeholder": "S ומספר אישי"}
    #     ),
    #     max_length=8,
    #     validators=[(RegexValidator(r"s\d{7}"))],
    #     label="שם משתמש",
    # )
    # password = forms.CharField(widget=forms.PasswordInput, label="סיסמה")
    pass

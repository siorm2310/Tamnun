from django.shortcuts import render, HttpResponse
from .forms import UserLoginForm
from django.contrib.auth.forms import AuthenticationForm

# Create your views here.


def landing_page(request):
    if request.method == "POST":
        form = UserLoginForm(request.POST)
        if form.is_valid():
            return HttpResponse("Success")
    else:
        form = UserLoginForm()

    return render(request, "users/landing_page.html", {"form": form})

from django.shortcuts import render, HttpResponse
from .forms import UserLoginForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login

# Create your views here.


def landing_page(request):
    if request.method == "POST":
        form = UserLoginForm(request.POST)
        if form.is_valid():
            username = request.POST["username"]
            password = request.POST["password"]
            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                return HttpResponse("Success")

            else:
                return HttpResponse("Failure")
    else:
        form = UserLoginForm()
    return render(request, "users/landing_page.html", {"form": form})

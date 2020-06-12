from django.shortcuts import render
from .forms import UserForm, UserProfileInfoForm
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError

from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
# Create your views here.


@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def user_login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(username=username, password=password)

        if user:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect(reverse("index"))
            else:
                return HttpResponse("Account not active")
        else:
            print(f"{username} try to login in failed")
            return HttpResponse("Invalid login details supplied!")

    else:

        return render(request, "app1/login.html", {})


def index(request):
    return render(request, "app1/index.html")


def register(request):
    registered = False
    if request.method == "POST":
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileInfoForm(data=request.POST)

        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save(commit=False)
            try:
                validate_password(user.password, user)
            except ValidationError as e:
                user_form.add_error("password", e)
            else:
                user.set_password(user.password)
                user.save()

                profile = profile_form.save(commit=False)
                profile.user = user
                for i in request.FILES:
                    print(i)
                if "picture" in request.FILES:
                    profile.picture = request.FILES["picture"]
                profile.save()

                registered = True
        else:
            print(user_form.errors, profile_form.errors)
    else:
        user_form = UserForm()
        profile_form = UserProfileInfoForm()

    my_dict = {"user_form": user_form, "profile_form": profile_form, "registered": registered}
    return render(request, "app1/registraion.html", context=my_dict)


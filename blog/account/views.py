from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from .forms import RegisterForm,LoginForm
from django.contrib.auth import login, authenticate, logout
# Create your views here.



def register_user(request):
    form = RegisterForm()

    if request.method == "POST":
        form = RegisterForm(data=request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user, backend="account.authentication.EmailAuthBackend")
            return redirect("social:post_list")

    return render(request, "register.html", {"form":form})


def login_user(request):

    form = LoginForm()

    if request.method == "POST":
        form = LoginForm(data = request.POST)
        if form.is_valid():
            email = form.cleaned_data["email"]
            password = form.cleaned_data["password"]

            user = authenticate(request, username=email, password=password)

            if user:
                login(request, user)
                return redirect("social:post_list")
            else:
                form.add_error(None, "user does not exist")


    return render(request, "login.html", {"form":form})



def logout_user(request):
    logout(request)
    return redirect("account:login")
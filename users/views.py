from django.shortcuts import render, redirect
from users.forms import UserRegisterForm
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib import messages
from django.conf import settings

User = settings.AUTH_USER_MODEL
# Create your views here.

def register(request):
    if request.user.is_authenticated:
        return redirect("home")
    
    if request.method == "POST":
        form = UserRegisterForm(request.POST or None)
        if form.is_valid():
            new_user = form.save()
            username = form.cleaned_data.get("username")
            messages.success(request, f"Hey {username}, You account was successfully create")
            new_user = authenticate(username=form.cleaned_data['email'], password=form.cleaned_data['password1'])
            auth_login(request, new_user)
            return redirect("signin")
    else:
        form = UserRegisterForm
    context = {
        'form': form
    }
    return render(request, 'users/signup.html', context)

def login(request):
    if request.user.is_authenticated:
        messages.warning(request, f"Hey you are alraedy logged in")
        return redirect("home")
    
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")

        try:
            user = User.objects.get(email=email)
        except:
            messages.warning(request, f"user with {email} does not exist")

        user = authenticate(request, email=email, password=password)

        if user is not None:
            auth_login(request, user)
            messages.success(request, "You are logged in")
            return redirect("home")
        else:
            messages.warning(request, "User does not exist, Create new account") 
    context = {

    }

    return render(request, 'users/signin.html', context)


def logout(request):
    auth_logout(request)
    messages.success(request, "You have logged out!") 
    return redirect("signin")
from django.shortcuts import render, redirect
from .forms import LoginForm, RegisterForm
from django.contrib.auth import authenticate, login, logout
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User


def login_view(request):
    form = LoginForm(request.POST or None)

    if form.is_valid():
        email = form.cleaned_data.get('email')
        password = form.cleaned_data.get('password')
        user = authenticate(email=email, password=password)
        login(request, user)
        Token.objects.filter(user=user).update(key=Token.generate_key())
        return redirect('post:index')

    context = {
        'form': form,
        'title': 'Log In'
    }

    return render(request, "account/form.html", context)


def register_view(request):
    form = RegisterForm(request.POST or None)

    if form.is_valid():
        user = form.save(commit=False)
        password = form.cleaned_data.get('confirm_password')
        user.set_password(password)
        user.save()
        login_user = authenticate(email=user.email, password=password)
        login(request, login_user)
        return redirect('post:index')

    context = {
        'form': form,
        'title': 'Register'
    }

    return render(request, 'account/form.html', context)


def logout_view(request):
    logout(request)
    return redirect('post:index')

from django.shortcuts import redirect, render
from django.contrib.auth import logout as auth_logout
from payments.actions import generate_client_token


def home(request):
    return render(request, 'home.html')


def logout(request):
    auth_logout(request)
    return redirect('home')


def signup(request):
    return render(request, 'signup_form.html')


def cc_form(request):
    context = {
        'client_token': generate_client_token()
    }
    return render(request, 'cc_form.html', context=context)


def done(request):
    return render(request, 'done.html')

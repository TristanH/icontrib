from django.shortcuts import render_to_response, redirect, render
from django.contrib.auth import logout as auth_logout


def home(request):
    return render(request, 'home.html')

def logout(request):
    auth_logout(request)
    return redirect('home')

def signup(request):
    return render(request, 'signup_form.html')

def cc_form(request):
    return render(request, 'cc_form.html')

def done(request):
    return render(request, 'done.html')

from django.shortcuts import render_to_response, redirect, render
from django.contrib.auth import logout as auth_logout


def home(request):
    return render(request, 'home.html')

def logout(request):
    auth_logout(request)
    return redirect('home')

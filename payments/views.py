from django.shortcuts import HttpResponse, render
from payments.actions import generate_client_token


def client_token(request):
    token = generate_client_token()
    return HttpResponse(token)


def register(request):
    return render(request, 'done.html')
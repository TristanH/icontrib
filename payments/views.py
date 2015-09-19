from django.shortcuts import HttpResponse
from payments.actions import generate_client_token


def client_token(request):
    token = generate_client_token()
    return HttpResponse(token)

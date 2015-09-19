import braintree
from django.shortcuts import HttpResponse


def generate_client_token(request):
    token = braintree.ClientToken.generate()
    return HttpResponse(token)

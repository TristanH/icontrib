from django.shortcuts import HttpResponse, redirect
from payments.actions import generate_client_token, link_user_braintree


def client_token(request):
    token = generate_client_token()
    return HttpResponse(token)


def register(request):
    user_profile = request.user.userprofile
    if user_profile is None:
        raise ValueError("Must register with valid user")
    payment_method_nonce = request.POST['payment_method_nonce']
    link_user_braintree(user_profile, payment_method_nonce)
    return redirect('https://twitter.com/IWillContribute')

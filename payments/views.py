from django.shortcuts import HttpResponse, render
from icontrib.models import UserProfile
from payments.actions import generate_client_token, link_user_braintree


def client_token(request):
    token = generate_client_token()
    return HttpResponse(token)


def register(request):
    user_id = request.COOKIES['USER_ID']
    user_profile = UserProfile.objects.get(id=user_id)
    if user_profile is None:
        raise ValueError("Must provide valid USER_ID cookie")
    link_user_braintree(user_profile, request.POST['payment_method_nonce'])
    return render(request, 'done.html')

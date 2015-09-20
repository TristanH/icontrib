from twython import Twython
from django.conf import settings
from django.shortcuts import HttpResponse, redirect
from icontrib.models import Campaign
from icontrib.utils import charge_user
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
    campaign_id = request.POST['campaign_id']
    campaign = Campaign.objects.get(id=campaign_id)

    OAUTH_TOKEN = UserSocialAuth.objects.get(uid="3609988267").extra_data['access_token']['oauth_token']
    OAUTH_SECRET = UserSocialAuth.objects.get(uid="3609988267").extra_data['access_token']['oauth_token_secret']
    twitter = Twython(settings.SOCIAL_AUTH_TWITTER_KEY, settings.SOCIAL_AUTH_TWITTER_SECRET, OAUTH_TOKEN,
                      OAUTH_SECRET)

    charge_user(campaign, user, twitter)
    return redirect('https://twitter.com/IWillContribute')

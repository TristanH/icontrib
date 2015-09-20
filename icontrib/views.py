from decimal import Decimal

from django.shortcuts import redirect, render
from django.contrib.auth import logout as auth_logout
from django.core.urlresolvers import reverse
from icontrib.models import Campaign
from payments.actions import generate_client_token


def strip_spec_chars(s):
    assert len(s) != 0
    if s[0] in ('#', '$'):
        return s[1:]
    return s


def logout(request):
    auth_logout(request)
    return redirect('home')


def create_campaign(request):
    if request.method == 'GET':
        return render(request, 'create_campaign.html')

    hashtag = strip_spec_chars(request.POST['hashtag'])
    if Campaign.objects.filter(hashtag=hashtag).exists():
        return redirect("{}#step-campaign".format(reverse('home')))
    target_amount = Decimal(strip_spec_chars(request.POST['targetAmount']))
    contribution_amount = Decimal(strip_spec_chars(request.POST['contributionAmount']))
    campaign = Campaign.objects.create(
        hashtag=hashtag,
        target_amount=str(target_amount),
        contribution_amount=str(contribution_amount),
        organizer_profile_id=request.user.userprofile.id
    )
    tweet_text = "I just created a campaign: #{} Contribute ${} to it by retweeting or tagging @IWillContribute".format(campaign.hashtag)
    return campaign_created(request, hashtag, tweet_text)


def start(request):
    return redirect("{}?next=/setup_payment/".format(reverse('social:begin', args=['twitter'])))


def setup_payments(request):
    context = {
        'client_token': generate_client_token()
    }
    return render(request, 'setup_payment.html', context=context)


def campaign_created(request, hashtag, tweet_text):
    return render(request, 'campaign_created.html', context=dict(
        hashtag=hashtag,
        tweet_text=tweet_text
    ))

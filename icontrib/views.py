from unicodedata import decimal
from decimal import Decimal
from django.shortcuts import redirect, render
from django.contrib.auth import logout as auth_logout
from icontrib.models import Campaign
from payments.actions import generate_client_token


def home(request):
    return render(request, 'signup_form.html')


def logout(request):
    auth_logout(request)
    return redirect('home')


def create_campaign(request):
    if request.method == 'GET':
        return render(request, 'create_campaign.html')

    hashtag = request.POST['hashtag']
    if hashtag.startswith('#'):
        hashtag = hashtag[1:]
    target_amount = Decimal(request.POST['targetAmount'])
    contribution_amount = Decimal(request.POST['contributionAmount'])
    campaign = Campaign.objects.create(
        hashtag=hashtag,
        target_amount=str(target_amount),
        contribution_amount=str(contribution_amount),
        organizer_profile_id=request.user.userprofile.id
    )
    return redirect('view_campaign', campaign.hashtag)


def cc_form(request):
    context = {
        'client_token': generate_client_token()
    }
    return render(request, 'cc_form.html', context=context)


def done(request):
    return render(request, 'done.html')


def view_campaign(request, campaign_hashtag):
    campaign = Campaign.objects.get(hashtag=campaign_hashtag)
    context = dict(
        campaign=campaign
    )
    return render(request, 'campaign.html', context=context)

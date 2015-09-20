import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'icontrib.settings')
from django.conf import settings
import django
django.setup()

from social.apps.django_app.default.models import UserSocialAuth
from twython import TwythonStreamer, Twython

from icontrib.models import Campaign, Contribution
from icontrib.utils import charge_user
from payments.actions import execute_contribution

OAUTH_TOKEN = UserSocialAuth.objects.get(uid="3609988267").extra_data['access_token']['oauth_token']
OAUTH_SECRET = UserSocialAuth.objects.get(uid="3609988267").extra_data['access_token']['oauth_token_secret']


class MyStreamer(TwythonStreamer):
    def on_success(self, data):
        tweeter = data.get('user', {}).get('screen_name')
        if not tweeter:
            tweeter = data.get('source', {}).get('screen_name')

        if 'text' not in data or not tweeter or tweeter == "IWillContribute":
            return

        twitter = Twython(settings.SOCIAL_AUTH_TWITTER_KEY, settings.SOCIAL_AUTH_TWITTER_SECRET, OAUTH_TOKEN,
            OAUTH_SECRET)

        hashtags = data.get('entities', {}).get('hashtags', [])

        campaign_matches = []
        for hashtag_obj in hashtags:
            campaigns = Campaign.objects.filter(hashtag=hashtag_obj['text'])
            if campaigns.exists():
                campaign_matches.append(campaigns[0])

        if len(campaign_matches) != 1:
            # TODO: tweet here to let user know they mentioned multiple campaigns
            return
        campaign = campaign_matches[0]

        app_user = UserSocialAuth.objects.filter(uid=data['user']['id_str'])
        if not app_user.exists() or not app_user[0].user.userprofile.payment_verified:
            message = "@{0} Hey! You haven't signed up for iContrib yet. " \
                      "Make your contribution for #{1} here: " \
                      "icontrib.co/?c={2}".format(
                tweeter, campaign.hashtag, campaign.id
            )
            twitter.update_status(status=message, in_reply_to_status_id=data['id_str'])
        else:
            campaign = Campaign.objects.get(hashtag=campaign_hashtag)

            if campaign.organizer_profile == app_user[0].user.userprofile:
                return  # We don't want a campaign organizer to donate to their own campaign by tweeting

            charge_user(campaign, app_user[0].user, twitter)

    def on_error(self, status_code, data):
        print str(data)


def stream_mentions():
    stream = MyStreamer(settings.SOCIAL_AUTH_TWITTER_KEY, settings.SOCIAL_AUTH_TWITTER_SECRET, OAUTH_TOKEN,
        OAUTH_SECRET)
    stream.user()

while True:
    try:
        stream_mentions()
    except Exception as e:
        pass

import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'icontrib.settings')
from django.conf import settings
import django
django.setup()

import json
import requests

from social.apps.django_app.default.models import UserSocialAuth
from twython import TwythonStreamer, Twython

from icontrib.models import Campaign, Contribution
from icontrib.utils import charge_user

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
            hashtag_text = hashtag_obj['text'].lower()
            campaigns = Campaign.objects.filter(hashtag=hashtag_text)
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
                      "www.icontrib.co/?c={2}".format(
                tweeter, campaign.hashtag, campaign.id
            )
            twitter.update_status(status=message, in_reply_to_status_id=data['id_str'])
            requests.post("https://hooks.slack.com/services/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", data=json.dumps({'text': "Told {} to sign up for icontrib #{} successfully!".format(tweeter, campaign.hashtag), }))
        else:

            if campaign.organizer_profile == app_user[0].user.userprofile:
                return  # We don't want a campaign organizer to donate to their own campaign by tweeting

            was_charged = charge_user(campaign, app_user[0].user, twitter, data['id_str'])
            requests.post("https://hooks.slack.com/services/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", data=json.dumps({'text': "Ran charge_user for {} and #{}: charged: {} ".format(tweeter, campaign.hashtag, was_charged), }))

    def on_error(self, status_code, data):
        requests.post("https://hooks.slack.com/services/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", data=json.dumps({'text': "Error on twitter streamer: {}".format(status_code), }))
        self.disconnect()


def stream_mentions():
    stream = MyStreamer(settings.SOCIAL_AUTH_TWITTER_KEY, settings.SOCIAL_AUTH_TWITTER_SECRET, OAUTH_TOKEN,
        OAUTH_SECRET)
    stream.user()

while True:
    try:
        requests.post("https://hooks.slack.com/services/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", data=json.dumps({'text': "Starting stream_mentions" }))
        stream_mentions()
    except Exception as e:
        pass

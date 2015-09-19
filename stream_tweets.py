import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'icontrib.settings')

from django.conf import settings

from icontrib.models import Campaign

from social.apps.django_app.default.models import UserSocialAuth
from twython import TwythonStreamer, Twython


OAUTH_TOKEN = "3609988267-JYK9psor847UOYu64Tz35kg19OXLxrKoj8xKFZS"
OAUTH_SECRET = "9qtFLClQfYm7vNeH8jMfqGzHZt3JbNmhbKwWsSPCAxfiS"


class MyStreamer(TwythonStreamer):
    def on_success(self, data):
        tweeter = data.get('user', {}).get('screen_name')
        if not tweeter:
            tweeter = data.get('source', {}).get('screen_name')

        if 'text' not in data or not tweeter or tweeter == "IWillContribute":
            return

        twitter = Twython(settings.SOCIAL_AUTH_TWITTER_KEY, settings.SOCIAL_AUTH_TWITTER_SECRET, OAUTH_TOKEN, OAUTH_SECRET)

        hashtags = data.get('entities', {}).get('hashtags', [])

        campaign_matches = {}
        for hashtag_obj in hashtags:
            if Campaign.objects.filter(hashtag=hashtag_obj['text']).exists():
                campaign_matches.append(hashtag_obj['text'])

        # if len(campaign_matches) != 1:
        #     # TODO: tweet here to let user know they mentioned multiple campaigns
        #     return

        campaign_hashtag = "swagyolo"  # campaign_matches[0]

        app_user = UserSocialAuth.objects.filter(uid=data['id_str'])
        if app_user.exists():
            # If payment token ready and works:
              # Make payment
              # Update campaign, tweet about it!
            # Else:
              # Message user, tell them to update payment info

        else:

            message = "Hey @{0}! You haven't signed up for iContrib yet... make your contribution for #{1} here: http://icontrib.co/signup".format(tweeter, campaign_hashtag)

            if 'retweeted_status' in data:
                twitter.update_status(status=message)
            else:
                twitter.update_status(status=message, in_reply_to_status_id=data['id_str'])


    def on_error(self, status_code, data):
        print status_code

        # Want to stop trying to get data because of the error?
        # Uncomment the next line!
        # self.disconnect()


def stream_mentions():
    stream = MyStreamer(settings.SOCIAL_AUTH_TWITTER_KEY, settings.SOCIAL_AUTH_TWITTER_SECRET, OAUTH_TOKEN, OAUTH_SECRET)
    stream.user()

while True:
    try:
        stream_mentions()
    except Exception as e:
        pass
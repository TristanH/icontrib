import os
from payments.actions import execute_contribution

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'icontrib.settings')

from django.conf import settings

from icontrib.models import Campaign, Contribution

from social.apps.django_app.default.models import UserSocialAuth
from twython import TwythonStreamer, Twython

OAUTH_TOKEN = UserSocialAuth.objects.get(uid="3609988267").extra_data['access_token']['oauth_token']
OAUTH_SECRET = UserSocialAuth.objects.get(uid="3609988267").extra_data['access_token']['oauth_token_secret']
   

class MyStreamer(TwythonStreamer):
    def on_success(self, data):
        import pdb; pdb.set_trace()

        tweeter = data.get('user', {}).get('screen_name')
        if not tweeter:
            tweeter = data.get('source', {}).get('screen_name')

        if 'text' not in data or not tweeter or tweeter == "IWillContribute":
            return

        twitter = Twython(settings.SOCIAL_AUTH_TWITTER_KEY, settings.SOCIAL_AUTH_TWITTER_SECRET, OAUTH_TOKEN,
            OAUTH_SECRET)

        hashtags = data.get('entities', {}).get('hashtags', [])

        campaign_matches = {}
        for hashtag_obj in hashtags:
            if Campaign.objects.filter(hashtag=hashtag_obj['text']).exists():
                campaign_matches.append(hashtag_obj['text'])

        # if len(campaign_matches) != 1:
        #     # TODO: tweet here to let user know they mentioned multiple campaigns
        #     return

        campaign_hashtag = "swagyolo"  # campaign_matches[0]
        app_user = UserSocialAuth.objects.filter(uid=data.get['user']['id_str'])
        message = "ayy lmao"
        contribution = None
        if not app_user.exists() or not app_user.user.userprofile.payment_verified:
            message = "Hey @{0}! You haven't signed up for iContrib yet. " \
                      "Make your contribution for #{1} here: " \
                      "http://icontrib.co/signup".format(
                tweeter, campaign_hashtag
            )
        else:
            campaign = Campaign.objects.get(hashtag=campaign_hashtag)

            contribution = Contribution()
            contribution.amount = campaign.contribution_amount  # TODO: un-hardcode contrib amt
            contribution.profile = app_user.user.userprofile
            contribution.confirmed, errors = execute_contribution(contribution.profile, contribution.amount)
            if contribution.confirmed:
                # contribution was successful
                message = "Congrats! You contributed ${0} to #{1}".format(contribution.amount, campaign.hashtag)
            else:
                message = "Uh-oh! There was a problem with your contribution. " \
                          "Please make sure your payment info is correct."
                print "Error with transaction: {}".format(errors)
            contribution.save()

        if 'retweeted_status' in data:
            result = twitter.update_status(status=message)
        else:
            result = twitter.update_status(status=message, in_reply_to_status_id=data['id_str'])

        if contribution is not None:
            contribution.twitter_post_link = result.get('url')
            contribution.save()

    def on_error(self, status_code, data):
        print status_code
        import pdb; pdb.set_trace()

        # Want to stop trying to get data because of the error?
        # Uncomment the next line!
        # self.disconnect()


def stream_mentions():
    stream = MyStreamer(settings.SOCIAL_AUTH_TWITTER_KEY, settings.SOCIAL_AUTH_TWITTER_SECRET, OAUTH_TOKEN,
        OAUTH_SECRET)
    stream.user()

while True:
    try:
        stream_mentions()
    except Exception as e:
        pass

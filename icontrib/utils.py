from social.apps.django_app.default.models import UserSocialAuth


def charge_user(campaign, user, twitter):
    contribution = Contribution()
    contribution.amount = campaign.contribution_amount  # TODO: un-hardcode contrib amt
    contribution.profile = user.userprofile
    contribution.confirmed = execute_contribution(contribution.profile, contribution.amount)
    contribution.twitter_post_id = data['id_str']
    contribution.campaign = campaign

    tweeter = UserSocialAuth.objects.get(user=user).extra_data['access_token']['screen_name']

    if contribution.confirmed:
        contribution.save()
        # contribution was successful
        message = "Thanks @{} for contributing ${} to #{}, we've now raised ${} out of ${}!".format(
            tweeter, contribution.amount, campaign.hashtag, campaign.amount_raised, campaign.target_amount
        )
        twitter.update_status(status=message)
        return True
    else:
        contribution.save()
        message = "@{} Uh-oh! There was a problem with your contribution. " \
                  "Please make sure your payment info is correct.".format(tweeter)
        twitter.update_status(status=message, in_reply_to_status_id=data['id_str'])
        return False

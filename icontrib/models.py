from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.db.models import Sum


class UserProfile(models.Model):
    user = models.OneToOneField(User)

    braintree_customer_id = models.CharField(max_length=128, default="null")

    @property
    def payment_verified(self):
        return self.braintree_customer_id != 'null'


def create_user_profile(sender, instance, created, **kwargs):
    if created:
        profile, created = UserProfile.objects.get_or_create(user=instance)


post_save.connect(create_user_profile, sender=User)


class Contribution(models.Model):
    amount = models.DecimalField(max_digits=6, decimal_places=2)

    # Requires braintree implementation:
    # payment_info = ..... 

    campaign = models.ForeignKey('Campaign')

    profile = models.ForeignKey('UserProfile')

    twitter_post_link = models.CharField(max_length=256, null=False)

    confirmed = models.BooleanField(null=False, default=False)


class Campaign(models.Model):
    # Requires braintree implementation:
    # receiving_payment_info = ....

    hashtag = models.CharField(max_length=24, null=False, unique=True)

    organizer_profile = models.ForeignKey('UserProfile')

    target_amount = models.DecimalField(max_digits=6, decimal_places=2, null=False)

    contribution_amount = models.DecimalField(max_digits=6, decimal_places=2, null=False, default=1.00)

    @property
    def amount_raised(self):
        contributions = Contribution.objects.filter(campaign_id=self.id)

        amount = contributions.aggregate(Sum('amount'))

        return amount

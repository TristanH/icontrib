import braintree
from icontrib.models import Campaign, UserProfile


def create_customer(user, payment_method_nonce, extra_info):
    info = dict(
        payment_method_nonce=payment_method_nonce
    )
    info.update(extra_info)
    result = braintree.Customer.create(info)
    if result.is_success:
        user.braintree_customer_id = result.customer.id
    else:
        raise result.errors


def execute_transaction(from_user, to_campaign, amount=None):
    if amount is None:
        amount = to_campaign.contribution_amount


execute_transaction(UserProfile(), Campaign())

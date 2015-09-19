import braintree


def link_user_braintree(user_profile, payment_method_nonce):
    assert user_profile.braintree_customer_id == "null"
    info = dict(
        payment_method_nonce=payment_method_nonce
    )
    result = braintree.Customer.create(info)
    if result.is_success:
        user_profile.braintree_customer_id = result.customer.id
        user_profile.save()
    else:
        raise result.errors
    return result.is_success


def execute_contribution(from_user, contribution_amount):
    if from_user.braintree_customer_id == "null":
        raise ValueError("User for transaction must have a braintree_customer_id")
    result = braintree.Transaction.sale({
        "customer_id": from_user.braintree_customer_id,
        "amount": contribution_amount
    })
    if not result.is_success:
        raise result.errors
    return result.is_success


def generate_client_token():
    return braintree.ClientToken.generate()

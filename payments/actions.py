import braintree


def link_user_braintree(user_profile, payment_method_nonce):
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


def execute_contribution(from_user_profile, contribution_amount):
    if from_user_profile.braintree_customer_id == "null":
        raise ValueError("User for transaction must have a braintree_customer_id")
    result = braintree.Transaction.sale({
        "customer_id": from_user_profile.braintree_customer_id,
        "amount": contribution_amount
    })
    return result.is_success, result.errors


def generate_client_token():
    return braintree.ClientToken.generate()

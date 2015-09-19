import braintree


def create_customer(user, payment_method_nonce, extra_info):
    assert user.braintree_customer_id is None
    info = dict(
        payment_method_nonce=payment_method_nonce
    )
    info.update(extra_info)
    result = braintree.Customer.create(info)
    if result.is_success:
        user.braintree_customer_id = result.customer.id
        user.save()
    else:
        raise result.errors
    return result.is_success


def execute_contribution(from_user, contribution_amount):
    if from_user.braintree_customer_id is None:
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

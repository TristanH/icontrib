import braintree
import os

braintree.Configuration.configure(
    braintree.Environment.Sandbox,
    merchant_id=os.environ['BRAINTREE_MERCHANT'],
    public_key=os.environ['BRAINTREE_PUBLIC_KEY'],
    private_key=os.environ['BRAINTREE_PRIVATE_KEY']
)

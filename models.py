class StripeCustomer:
    def __init__(
        self,
        api_key,
        calls,
        number_of_payments,
        active,
        stripe_customer_id,
        customer_email,
        customer_name,
    ):
        self.api_key = api_key
        self.calls: int = calls
        self.number_of_payments: int = number_of_payments
        self.active = active
        self.stripe_customer_id = stripe_customer_id
        self.customer_email = customer_email
        self.customer_name = customer_name
